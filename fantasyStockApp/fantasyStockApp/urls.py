"""fantasyStockApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from dashboard import views as dashboard_views
from portfolio import views as portfolio_views
from leagues import views as leagues_views
from trading import views as trading_views
from education import views as education_views

urlpatterns = [
    path('admin/', admin.site.urls),
   
]
"""path('users/', user_views.user_dashboard, name='user_dashboard'),
    path('dashboard/', dashboard_views.dashboard_overview, name='dashboard_overview'),
    path('portfolio/', portfolio_views.portfolio_management, name='portfolio_management'),
    path('leagues/', leagues_views.league_management, name='league_management'),
    path('trading/', trading_views.trade_execution, name='trade_execution'),
    path('education/', education_views.educational_resources, name='educational_resources'),"""
