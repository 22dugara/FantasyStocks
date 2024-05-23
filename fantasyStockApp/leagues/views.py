from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from portfolio.models import *
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .forms import CreateLeagueForm, JoinLeagueForm
import re
import random
from datetime import datetime, timedelta
from .utils import get_user_score





def generate_matchups(league):
    members = list(LeagueMembership.objects.filter(league=league))
    num_members = len(members)
    num_weeks = league.length

    # Create a list of users
    users = [member.user for member in members]

    # If the number of members is odd, add a dummy user for byes
    if num_members % 2 == 1:
        users.append(None)
        num_members += 1

    matchups = []
    for week in range(1, num_weeks + 1):
        for i in range(num_members // 2):
            user1 = users[i]
            user2 = users[num_members - 1 - i]
            if user1 is not None and user2 is not None:
                matchups.append(Matchup(league=league, week=week, user1=user1, user2=user2))

        # Rotate users but keep the first one in place
        users = [users[0]] + [users[-1]] + [users[1:-1]]

    Matchup.objects.bulk_create(matchups)

def record_week_results(league):
    matchups = Matchup.objects.filter(league=league, week=league.current_week)
    for matchup in matchups:
        user1_score = get_user_score(matchup.user1, league)
        user2_score = get_user_score(matchup.user2, league)
        if user1_score > user2_score:
            LeagueMembership.objects.filter(user=matchup.user1, league=league).update(wins=models.F('wins') + 1)
            LeagueMembership.objects.filter(user=matchup.user2, league=league).update(losses=models.F('losses') + 1)
        elif user1_score < user2_score:
            LeagueMembership.objects.filter(user=matchup.user1, league=league).update(losses=models.F('losses') + 1)
            LeagueMembership.objects.filter(user=matchup.user2, league=league).update(wins=models.F('wins') + 1)
        else:
            LeagueMembership.objects.filter(user=matchup.user1, league=league).update(ties=models.F('ties') + 1)
            LeagueMembership.objects.filter(user=matchup.user2, league=league).update(ties=models.F('ties') + 1)

def update_current_week(league, force_update=False):
    today = datetime.now().date()
    if league.next_week_date is None:
        league.next_week_date = today + timedelta(days=7)
        league.save()

    if league.draftDone and (today >= league.next_week_date or force_update):
        # Record and update win-loss-tie records for the past week
        record_week_results(league)

        if league.current_week < league.length:
            league.current_week += 1
            league.next_week_date = today + timedelta(days=7)
            league.save()

@login_required
def league_view(request):
    try:
        league_membership = LeagueMembership.objects.get(user=request.user)
        league = league_membership.league
    except LeagueMembership.DoesNotExist:
        league = None

    if league:
        is_owner = league.owner == request.user
        members = LeagueMembership.objects.filter(league=league) if is_owner else []
    else:
        is_owner = False
        members = []

    if request.method == 'POST':
        if 'start_league' in request.POST:
            league.started = True
            league.save()

            channel_layer = get_channel_layer()
            sanitized_league_name = re.sub(r'[^a-zA-Z0-9_-]', '_', league.name)
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    f'league_{sanitized_league_name}',
                    {
                        'type': 'league_message',
                        'message': 'The league has started! You can now enter the draft.'
                    }
                )
            messages.success(request, 'League started successfully.')

        if 'end_draft' in request.POST:
            league.draftDone = True
            league.next_week_date = datetime.now().date() + timedelta(days=7)  # Set the next week date to 7 days from now
            league.save()
            generate_matchups(league)

            channel_layer = get_channel_layer()
            sanitized_league_name = re.sub(r'[^a-zA-Z0-9_-]', '_', league.name)
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    f'league_{sanitized_league_name}',
                    {
                        'type': 'league_message',
                        'message': 'The draft is done!'
                    }
                )
            messages.success(request, 'Draft ended successfully.')

    context = {
        'league': league,
        'is_owner': is_owner,
        'members': members,
        'started': league.started if league else False,
        'draftDone': league.draftDone if league else False
    }
    return render(request, 'league.html', context)

@login_required
def matchups_view(request):
    try:
        league_membership = LeagueMembership.objects.get(user=request.user)
        league = league_membership.league
    except LeagueMembership.DoesNotExist:
        league = None

    if not league or not league.draftDone:
        return redirect('league')

    # Update the current week based on the date
    update_current_week(league)

    if request.method == 'POST' and 'skip_week' in request.POST and league.owner == request.user:
        # Force update to the next week
        update_current_week(league, force_update=True)
        messages.success(request, 'Skipped to the next week.')

    matchups = Matchup.objects.filter(league=league, user1=request.user) | Matchup.objects.filter(league=league, user2=request.user)
    current_matchup = matchups.filter(week=league.current_week).first()

    if current_matchup:
        opponent = current_matchup.user1 if current_matchup.user2 == request.user else current_matchup.user2
        opponent_portfolio = Portfolio.objects.get(user=opponent, league=league)
        opponent_assets = PortfolioAsset.objects.filter(portfolio=opponent_portfolio)
    else:
        opponent = None
        opponent_assets = []

    user_record = {
        'wins': league_membership.wins,
        'losses': league_membership.losses,
        'ties': league_membership.ties,
    }

    context = {
        'league': league,
        'matchups': matchups.order_by('week'),
        'current_matchup': current_matchup,
        'opponent': opponent,
        'opponent_assets': opponent_assets,
        'user_record': user_record,
    }
    return render(request, 'matchups.html', context)





@login_required
def create_league(request):
    if request.method == 'POST':
        form = CreateLeagueForm(request.POST)
        if form.is_valid():
            league = form.save(commit=False)
            league.owner = request.user
            league.save()
            LeagueMembership.objects.create(user=request.user, league=league)
            Portfolio.objects.create(user=request.user, name=f"{league.name} Portfolio", league=league, cash=100000)
            return redirect('league')
    else:
        form = CreateLeagueForm()
    return render(request, 'create_league.html', {'form': form})

@login_required
def join_league(request):
    if request.method == 'POST':
        form = JoinLeagueForm(request.POST)
        if form.is_valid():
            league = form.cleaned_data['league']
            LeagueMembership.objects.create(user=request.user, league=league)
            Portfolio.objects.create(user=request.user, name=f"{league.name} Portfolio", league=league, cash=100000)
            return redirect('league')
    else:
        form = JoinLeagueForm()
    return render(request, 'join_league.html', {'form': form})


@login_required
def user_portal(request):
    return render(request, 'user_portal.html', {'username': request.user.username})