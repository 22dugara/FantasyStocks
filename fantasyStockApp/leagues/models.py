from django.db import models
from django.contrib.auth.models import User

class League(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_leagues')
    key = models.CharField(max_length=20, default = "")
    started = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class LeagueMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.league.name}"

class Matchup(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    week = models.IntegerField()
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matchup_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matchup_user2')
    user1_score = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    user2_score = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Week {self.week}: {self.user1.username} vs {self.user2.username} in {self.league.name}"
