from portfolio.models import Portfolio

def get_user_score(user, league):
    try:
        portfolio = Portfolio.objects.get(user=user, league=league)
        return portfolio.cash
    except Portfolio.DoesNotExist:
        return 0.0
