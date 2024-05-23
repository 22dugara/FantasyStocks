from django.contrib import admin
from .models import League, LeagueMembership, Matchup

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'owner', 'key', 'started', 'draftDone', 'length', 'current_week', 'next_week_date')
    search_fields = ('name', 'owner__username')

@admin.register(LeagueMembership)
class LeagueMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'league', 'joined_at', 'wins', 'losses', 'ties')
    search_fields = ('user__username', 'league__name')

@admin.register(Matchup)
class MatchupAdmin(admin.ModelAdmin):
    list_display = ('league', 'week', 'user1', 'user2', 'user1_score', 'user2_score')
    search_fields = ('league__name', 'user1__username', 'user2__username')
