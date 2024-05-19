from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import League, LeagueMembership
from portfolio.models import Portfolio
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .forms import CreateLeagueForm, JoinLeagueForm
import re

@login_required
def user_portal(request):
    return render(request, 'user_portal.html', {'username': request.user.username})




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

    if request.method == 'POST' and 'start_league' in request.POST:
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

    context = {
        'league': league,
        'is_owner': is_owner,
        'members': members,
        'started': league.started if league else False  # Add started status to context
    }
    return render(request, 'league.html', context)

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
