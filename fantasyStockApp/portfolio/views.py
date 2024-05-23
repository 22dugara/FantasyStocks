from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Portfolio, PortfolioAsset
from leagues.models import LeagueMembership

@login_required
def portfolio_management(request):
    # Check if the user has any portfolios
    portfolios = Portfolio.objects.filter(user=request.user)
    
    if not portfolios.exists():
        # Check if the user is in any leagues
        league_memberships = LeagueMembership.objects.filter(user=request.user)
        
        if league_memberships.exists():
            # Create a portfolio for each league the user is in
            for membership in league_memberships:
                league = membership.league
                Portfolio.objects.create(user=request.user, name=f"{league.name} Portfolio", league=league, cash=100000)
            
            # Refresh the portfolios queryset
            portfolios = Portfolio.objects.filter(user=request.user)
        else:
            # User is not in any leagues, render a message
            context = {
                'message': 'You need to join a league.',
            }
            return render(request, 'portfolio_management.html', context)
    
    # Assuming we want to display the first portfolio for now
    portfolio = portfolios.first()
    league = LeagueMembership.objects.filter(user=request.user)[0].league
    if league.draftDone == False:            
        context = {
                'message': 'League Draft has not been completed.',
            }
        return render(request, 'portfolio_management.html', context)

    assets = PortfolioAsset.objects.filter(portfolio=portfolio)
    context = {
        'assets': assets,
        'cash': portfolio.cash,
    }
    return render(request, 'portfolio_management.html', context)

