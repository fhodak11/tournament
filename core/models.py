from django.db import models

# Create your models here.
team_count_choices = (
    [
        (4, "Eight"),
        (8, "Sixteen")
    ]
)
class Tournament(models.Model):
    """Tournament model
    
    Arguments:
        models {Model} -- Django model

    Attributes:
        tournament {CharField} -- Name of the tournament
        team_count {IntegerField} -- Number of teams in the tournament
        tournament_date {DateField} -- Date of the tournament
    """
    tournament = models.CharField(max_length=100)
    game_count = models.IntegerField(choices=team_count_choices)
    tournament_date = models.DateField(auto_now=True)
    started = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Tournaments"
        verbose_name = "Tournament"

    def __str___(self):
        return self.tournament
    
class Team(models.Model):
    """
    Team model
    Attributes:
        tournament {ForeignKey} -- Foreign key to tournament model
        team_name {CharField} -- Name of the team
    """
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100, blank=True, null=True)
    opponent = models.CharField(max_length=100, null=True, blank=True)
    team_score = models.IntegerField(default=0)
    opponent_score = models.IntegerField(default=0)
    modified = models.BooleanField(default=False)
    score_modified = models.BooleanField(default=False)
    stage_modified = models.BooleanField(default=False) 
    win = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Teams"
        verbose_name = "Team"

    def __str__(self):
        return self.team_name

class Player(models.Model):
    """
    Player model
    Attributes:
        team {ForeignKey} -- Foreign key to team model
        player_name {CharField} -- Name of the player
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=100)

    # verbose
    class Meta:
        verbose_name_plural = "Players"
        verbose_name = "Player"

    def __str__(self):
        return self.player_name

class Quarters(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    # home_team = models.CharField(max_length=100, blank=True, null=True)
    opponent = models.CharField(max_length=100, null=True, blank=True)
    
    team_score = models.IntegerField(default=0)
    opponent_score = models.IntegerField(default=0)
    
    score_modified = models.BooleanField(default=False)
    
    
class Semi(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    # home_team = models.CharField(max_length=100, blank=True, null=True)
    opponent = models.CharField(max_length=100, null=True, blank=True)
    
    team_score = models.IntegerField(default=0)
    opponent_score = models.IntegerField(default=0)
    
    score_modified = models.BooleanField(default=False)
    
class PosThree(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    # home_team = models.CharField(max_length=100, blank=True, null=True)
    opponent = models.CharField(max_length=100, null=True, blank=True)
    
    team_score = models.IntegerField(default=0)
    opponent_score = models.IntegerField(default=0)
    
    score_modified = models.BooleanField(default=False)
    
class Finals(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    # home_team = models.CharField(max_length=100, blank=True, null=True)
    opponent = models.CharField(max_length=100, null=True, blank=True)
    
    team_score = models.IntegerField(default=0)
    opponent_score = models.IntegerField(default=0)
    
    score_modified = models.BooleanField(default=False)
    
class Ranking(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    # home_team = models.CharField(max_length=100, blank=True, null=True)
    opponent = models.CharField(max_length=100, null=True, blank=True)
    
    team_score = models.IntegerField(default=0)
    opponent_score = models.IntegerField(default=0)
    
    score_modified = models.BooleanField(default=False)