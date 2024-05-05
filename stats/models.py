from django.db import models

# Create your models here.

class Game(models.Model):
    #id = models.AutoField(primary_key=True)
    date_of_game_ft = models.DateField()
    time_ft = models.TimeField()
    team_ft = models.CharField(max_length=100)
    opponent_ft = models.CharField(max_length=100)
    full_time_goals_scored_ft = models.IntegerField()
    full_time_goals_conceded_ft = models.IntegerField()
    #home_ft = models.BooleanField()
    home_ft = models.CharField(max_length=30)
    game_outcome_ft = models.CharField(max_length=20)
    #win_ft = models.BooleanField()
    #draw_ft = models.BooleanField()
    #loss_ft = models.BooleanField()
    win_ft = models.IntegerField(default=0)  # Defaulting to 0 instead of False
    draw_ft = models.IntegerField(default=0)
    loss_ft = models.IntegerField(default=0)
    points_ft = models.IntegerField()
    half_time_team_goals_scored_ft = models.IntegerField()
    half_time_team_goals_conceded_ft = models.IntegerField()
    half_time_win_ft = models.BooleanField()
    half_time_draw_ft = models.BooleanField()
    half_time_loss_ft = models.BooleanField()
    referee_ft = models.CharField(max_length=100)
    team_shots_recorded_ft = models.IntegerField()
    team_shots_conceded_ft = models.IntegerField()
    team_shots_on_target_recorded_ft = models.IntegerField()
    team_shots_on_target_conceded_ft = models.IntegerField()
    team_fouls_committed_recorded_ft = models.IntegerField()
    team_fouls_committed_conceded_ft = models.IntegerField()
    team_corners_recorded_ft = models.IntegerField()
    team_corners_conceded_ft = models.IntegerField()
    team_yellow_cards_recorded_ft = models.IntegerField()
    team_yellow_cards_conceded_ft = models.IntegerField()
    team_red_cards_recorded_ft = models.IntegerField()
    team_red_cards_conceded_ft = models.IntegerField()
    half_time_outcome_ft = models.CharField(max_length=20)
    season_ft = models.CharField(max_length=20)
    goal_difference_ft = models.IntegerField()
    league = models.CharField(max_length=100)
    more_corners_ft = models.BooleanField()
    more_cards_ft = models.BooleanField()

    #def __str__(self):
    #    return f"{self.team_ft} vs {self.opponent_ft} - {self.date_of_game_ft}"

    class Meta:
        # If your table has a specific name, specify it here
        #managed = False
        db_table = 'footdata2'

