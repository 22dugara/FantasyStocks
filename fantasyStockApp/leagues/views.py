from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import League, LeagueMembership
from .forms import CreateLeagueForm, JoinLeagueForm
from portfolio.models import Portfolio

@login_required
def user_portal(request):
    return render(request, 'user_portal.html', {'username': request.user.username})

@login_required
def league_view(request):
    user_leagues = LeagueMembership.objects.filter(user=request.user)
    if user_leagues.exists():
        league = user_leagues.first().league
        context = {'in_league': True, 'league_name': league.name}
    else:
        context = {'in_league': False}
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
