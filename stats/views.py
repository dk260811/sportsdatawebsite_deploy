from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum, Case, When, Q
from django.http import JsonResponse
from django.template.loader import render_to_string
import numpy as np
from scipy import stats
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from collections import Counter
import json 
from django.core.serializers import serialize

import io
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Create your views here.

#def index(request):
#    return render(request, "stats/index.html")

#from django.shortcuts import render
from .models import Game

LEAGUE_MAPPING = {
    'E0': 'English Premier League',
    'B1': 'Belgian League',
    'SP1': 'La Liga',
    'D1': 'Bundesliga',
    'D2': 'Bundesliga 2',
    'E1': 'English Championship',
    'E2': 'League One',
    'E3': 'League Two',
    'F1': 'French League',
    'F2': 'French League Two',
    'G1': 'Greek League',
    'I1': 'Seria A',
    'I2': 'Seria B',
    'N1': 'Eredevise',
    'P1': 'Portugese League',
    'SC0': 'Scotish league',
    'SP2': 'Secunda Div',
    'T1': 'Turkish super league',
    # Add more league codes and names as needed
}

reverse_LEAGUE_MAPPING = {
    'English Premier League': 'E0',
    'Belgian League': 'B1',
    'La Liga': 'SP1',
    'Bundesliga': 'D1',
    'Bundesliga 2': 'D2',
    'English Championship': 'E1',
    'League One': 'E2',
    'League Two': 'E3',
    'French League': 'F1',
    'French League Two': 'F2',
    'Greek League': 'G1',
    'Seria A': 'I1',
    'Seria B': 'I2',
    'Eredevise': 'N1',
    'Portugese League': 'P1',
    'Scotish league': 'SC0',
    'Secunda Div': 'SP2',
    'Turkish super league': 'T1'
    # Add more league names and codes as needed
}



def index(request):

    # Get distinct seasons and leagues from the Game model
    seasons = Game.objects.values_list('season_ft', flat=True).distinct().order_by('season_ft')
    leagues = Game.objects.values_list('league', flat=True).distinct().order_by('league')
    teams = Game.objects.values_list('team_ft', flat=True).distinct().order_by('team_ft')

    leagues = [LEAGUE_MAPPING.get(code, code) for code in leagues]

    return render(request, 'stats/index.html', {'seasons': seasons, 'leagues': leagues, 'teams': teams})


def basic_table(request):

    # Get distinct seasons and leagues from the Game model
    seasons = Game.objects.values_list('season_ft', flat=True).distinct().order_by('season_ft')
    leagues = Game.objects.values_list('league', flat=True).distinct().order_by('league')
    teams = Game.objects.values_list('team_ft', flat=True).distinct().order_by('team_ft')

    leagues = [LEAGUE_MAPPING.get(code, code) for code in leagues]

    return render(request, 'stats/basic_table.html', {'seasons': seasons, 'leagues': leagues, 'teams': teams})


"""
def update_table(request):
    season = request.GET.get('season')
    league = request.GET.get('league')

    teams = Game.objects.filter(league=league, season_ft=season).values(
        'team_ft', 'season_ft', 'league'
    ).annotate(
        total_points=Sum('points_ft'),
        total_goals_scored=Sum('full_time_goals_scored_ft'),
        total_goals_conceded=Sum('full_time_goals_conceded_ft'),
        goal_difference=Sum('goal_difference_ft')
    ).order_by('-total_points')

    # Render the table template with the filtered data
    html_content = render_to_string('stats/basictable.html', {'teams': teams})

    # Return the HTML content as an HTTP response
    return HttpResponse(html_content)"""


def update_table(request):
    season = request.GET.get('season')
    league = request.GET.get('league')
    home_away = request.GET.get('homeAway', 'all')  # Default to 'all'
     # Get the full name of the league using the league code
    league = reverse_LEAGUE_MAPPING.get(league, league)

    if home_away == 'all':
        teams = Game.objects.filter(league=league, season_ft=season).values(
        'team_ft', 'season_ft', 'league'
    ).annotate(
        total_points=Sum('points_ft'),
        total_goals_scored=Sum('full_time_goals_scored_ft'),
        total_goals_conceded=Sum('full_time_goals_conceded_ft'),
        goal_difference=Sum('goal_difference_ft'),
        games_played=Sum('win_ft') + Sum('draw_ft') + Sum('loss_ft'),
        total_shots_recorded =Sum('team_shots_recorded_ft'),
        total_shots_conceded =Sum('team_shots_conceded_ft'),
        total_shots_OT_recorded =Sum('team_shots_on_target_recorded_ft'),
        total_shots_OT_conceded =Sum('team_shots_on_target_conceded_ft'),
        total_corners_recorded =Sum('team_corners_recorded_ft'),
        total_corners_conceded =Sum('team_corners_conceded_ft'),
        total_fouls =Sum('team_fouls_committed_recorded_ft'),
        total_yellow_cards =Sum('team_yellow_cards_recorded_ft'),
        total_red_cards =Sum('team_red_cards_recorded_ft'),
        #games_played=Sum('win_ft'+'draw_ft'+'loss_ft'),
    ).order_by('-total_points')
    elif home_away == 'Homegame':
        teams = Game.objects.filter(league=league, season_ft=season, home_ft='Homegame').values(
        'team_ft', 'season_ft', 'league'
    ).annotate(
        total_points=Sum('points_ft'),
        total_goals_scored=Sum('full_time_goals_scored_ft'),
        total_goals_conceded=Sum('full_time_goals_conceded_ft'),
        goal_difference=Sum('goal_difference_ft'),
        games_played=Sum('win_ft') + Sum('draw_ft') + Sum('loss_ft'),
        total_shots_recorded =Sum('team_shots_recorded_ft'),
        total_shots_conceded =Sum('team_shots_conceded_ft'),
        total_shots_OT_recorded =Sum('team_shots_on_target_recorded_ft'),
        total_shots_OT_conceded =Sum('team_shots_on_target_conceded_ft'),
        total_corners_recorded =Sum('team_corners_recorded_ft'),
        total_corners_conceded =Sum('team_corners_conceded_ft'),
        total_fouls =Sum('team_fouls_committed_recorded_ft'),
        total_yellow_cards =Sum('team_yellow_cards_recorded_ft'),
        total_red_cards =Sum('team_red_cards_recorded_ft'),
        #games_played=Sum('win_ft'+'draw_ft'+'loss_ft'),
    ).order_by('-total_points')
    else:
        teams = Game.objects.filter(league=league, season_ft=season, home_ft='Awaygame').values(
        'team_ft', 'season_ft', 'league'
    ).annotate(
        total_points=Sum('points_ft'),
        total_goals_scored=Sum('full_time_goals_scored_ft'),
        total_goals_conceded=Sum('full_time_goals_conceded_ft'),
        goal_difference=Sum('goal_difference_ft'),
        games_played=Sum('win_ft') + Sum('draw_ft') + Sum('loss_ft'),
        total_shots_recorded =Sum('team_shots_recorded_ft'),
        total_shots_conceded =Sum('team_shots_conceded_ft'),
        total_shots_OT_recorded =Sum('team_shots_on_target_recorded_ft'),
        total_shots_OT_conceded =Sum('team_shots_on_target_conceded_ft'),
        total_corners_recorded =Sum('team_corners_recorded_ft'),
        total_corners_conceded =Sum('team_corners_conceded_ft'),
        total_fouls =Sum('team_fouls_committed_recorded_ft'),
        total_yellow_cards =Sum('team_yellow_cards_recorded_ft'),
        total_red_cards =Sum('team_red_cards_recorded_ft'),
        #games_played=Sum('win_ft'+'draw_ft'+'loss_ft'),
    ).order_by('-total_points')

    """
    teams = Game.objects.filter(league=league, season_ft=season).values(
        'team_ft', 'season_ft', 'league'
    ).annotate(
        total_points=Sum('points_ft'),
        total_goals_scored=Sum('full_time_goals_scored_ft'),
        total_goals_conceded=Sum('full_time_goals_conceded_ft'),
        goal_difference=Sum('goal_difference_ft'),
        games_played=Sum('win_ft') + Sum('draw_ft') + Sum('loss_ft'),
        total_shots_recorded =Sum('team_shots_recorded_ft'),
        total_shots_conceded =Sum('team_shots_conceded_ft'),
        total_shots_OT_recorded =Sum('team_shots_on_target_recorded_ft'),
        total_shots_OT_conceded =Sum('team_shots_on_target_conceded_ft'),
        total_corners_recorded =Sum('team_corners_recorded_ft'),
        total_corners_conceded =Sum('team_corners_conceded_ft'),
        total_fouls =Sum('team_fouls_committed_recorded_ft'),
        total_yellow_cards =Sum('team_yellow_cards_recorded_ft'),
        total_red_cards =Sum('team_red_cards_recorded_ft'),
        #games_played=Sum('win_ft'+'draw_ft'+'loss_ft'),
    ).order_by('-total_points')
    """

    # Render the table template with the filtered data
    html_content = render_to_string('stats/basictable.html', {'teams': teams})

    # Return the HTML content with CSS included
    return HttpResponse(html_content)
 

def stat_analysis(request):
    
    games = Game.objects.all()
    seasons = Game.objects.values_list('season_ft', flat=True).distinct().order_by('season_ft')
    leagues = Game.objects.values_list('league', flat=True).distinct().order_by('league')
    teams = Game.objects.values_list('team_ft', flat=True).distinct().order_by('team_ft')

    leagues = [LEAGUE_MAPPING.get(code, code) for code in leagues]

    return render(request, 'stats/statanal.html', {'teams': teams, 'leagues': leagues, 'games':games, 'seasons':seasons})



def generate_histogram(request):
    if request.method == 'GET':
        league = request.GET.get('league')
        season = request.GET.get('season')
        stat_type = request.GET.get('stat')
        team = request.GET.get('team', 'all')
        seasons = Game.objects.values_list('season_ft', flat=True).distinct().order_by('season_ft')
        leagues = Game.objects.values_list('league', flat=True).distinct().order_by('league')
        league = reverse_LEAGUE_MAPPING.get(league, league)

        if not league or not season:
            return JsonResponse({'error': 'Missing required parameters: league and season'})

        # Map stat_type to the corresponding fields
        stat_fields_map = {
            'goals': ('full_time_goals_scored_ft', 'full_time_goals_conceded_ft'),
            'corners': ('team_corners_recorded_ft', 'team_corners_conceded_ft'),
            'shots': ('team_shots_recorded_ft', 'team_shots_conceded_ft'),
            'shots_on_target': ('team_shots_on_target_recorded_ft', 'team_shots_on_target_conceded_ft'),
            'fouls': ('team_fouls_committed_recorded_ft', 'team_fouls_committed_conceded_ft'),
            'yellow_cards': ('team_yellow_cards_recorded_ft', 'team_yellow_cards_conceded_ft'),
            'red_cards': ('team_red_cards_recorded_ft', 'team_red_cards_conceded_ft'),
        }

        # Get the corresponding fields for the chosen stat_type
        field_one, field_two = stat_fields_map[stat_type]

        # Filter games based on selected league and season
        #games = Game.objects.filter(league=league, season_ft=season)


        if team == 'all':

            # Calculate goals scored per team efficiently using aggregation
            goals_scored = Game.objects.filter(league=league, season_ft=season).values(
                'team_ft'
            ).annotate(total_goals_scored=Sum(field_one),
                    games_played=Sum('win_ft') + Sum('draw_ft') + Sum('loss_ft'),)

            games = Game.objects.filter(league=league, season_ft=season).values(
                'date_of_game_ft',field_one,field_two
            )

            games2 = Game.objects.filter(league=league, season_ft=season, home_ft = 'Homegame').values(
            field_one,field_two)

            games_data2 = list(games2.values(field_one,field_two))

            total_goals_of_games_scored = [entry[field_one] for entry in games_data2]  # Extract goal counts
            total_goals_of_games_conc = [entry[field_two] for entry in games_data2]  # Extract goal counts
            
            total_goals_of_games = [scored + conceded for scored, conceded in zip(total_goals_of_games_scored, total_goals_of_games_conc)]


        else:

            # Calculate goals scored per team efficiently using aggregation
            goals_scored = Game.objects.filter(league=league, season_ft=season, team_ft = team).values(
                'team_ft'
            ).annotate(total_goals_scored=Sum(field_one),
                    games_played=Sum('win_ft') + Sum('draw_ft') + Sum('loss_ft'),)

            games = Game.objects.filter(league=league, season_ft=season, team_ft = team).values(
                'date_of_game_ft',field_one,field_two
            )

            games2 = Game.objects.filter(league=league, season_ft=season, team_ft = team).values(
            field_one,field_two)

            games_data2 = list(games2.values(field_one,field_two))

            total_goals_of_games_scored = [entry[field_one] for entry in games_data2]  # Extract goal counts
            total_goals_of_games_conc = [entry[field_two] for entry in games_data2]  # Extract goal counts

            total_goals_of_games = [scored for scored in total_goals_of_games_scored]



        


        # Extract data for JavaScript
        teams = [goal['team_ft'] for goal in goals_scored]  # Extract team names
        goal_counts = [goal['total_goals_scored'] for goal in goals_scored]  # Extract goal counts
        games_played = [goal['games_played'] for goal in goals_scored]

         # Serialize games data to get dates and goals
        games_data = list(games.values('date_of_game_ft', field_one,field_two))

        dates_of_games = [entry['date_of_game_ft'].strftime('%Y-%m-%d') for entry in games_data]
        goals_of_games = [entry[field_one] for entry in games_data]  # Extract goal counts
        
        
        """
         # Compute statistical indicators
        mean_value = round(np.mean(total_goals_of_games), 1)
        median_value = round(np.median(total_goals_of_games), 1)
        mode_value = round(float(stats.mode(total_goals_of_games)[0]), 1)
        std_dev_value = round(np.std(total_goals_of_games), 1)
        variance_value = round(np.var(total_goals_of_games), 1)
        range_value = round(max(total_goals_of_games) - min(total_goals_of_games), 1)
        q1, q3 = np.percentile(total_goals_of_games, [25, 75])
        iqr_value = round(q3 - q1, 1)
        skewness_value = round(stats.skew(total_goals_of_games), 1)
        kurtosis_value = round(stats.kurtosis(total_goals_of_games), 1)
        """
        # Calculate statistical indicators if data is available
        if total_goals_of_games:
            mean_value = round(np.mean(total_goals_of_games), 1)
            median_value = round(np.median(total_goals_of_games), 1)
            mode_value = round(float(stats.mode(total_goals_of_games)[0]), 1)
            std_dev_value = round(np.std(total_goals_of_games), 1)
            variance_value = round(np.var(total_goals_of_games), 1)
            range_value = round(max(total_goals_of_games) - min(total_goals_of_games), 1)
            q1, q3 = np.percentile(total_goals_of_games, [25, 75])
            iqr_value = round(q3 - q1, 1)
            skewness_value = round(stats.skew(total_goals_of_games), 1)
            kurtosis_value = round(stats.kurtosis(total_goals_of_games), 1)
        else:
            mean_value = median_value = mode_value = std_dev_value = variance_value = range_value = iqr_value = skewness_value = kurtosis_value = "No stats available"

        #league = [LEAGUE_MAPPING.get(code, code) for code in league]
        league = LEAGUE_MAPPING.get(league, league)

        context = {
            'league': league,
            'season': season,
            'teams_json': json.dumps(teams),  # Now it will work!
            'goal_counts_json': json.dumps(goal_counts),
            'games_played': json.dumps(games_played),
            'dates_json': json.dumps(dates_of_games),  # Now it will work!
            'goals_json': json.dumps(goals_of_games),
            'total_goals_json': json.dumps(total_goals_of_games),
            'mean_value': mean_value,
            'median_value': median_value,
            'mode_value': mode_value,
            'std_dev_value': std_dev_value,
            'variance_value': variance_value,
            'range_value': range_value,
            'iqr_value': iqr_value,
            'skewness_value': skewness_value,
            'kurtosis_value': kurtosis_value,
            'teams': teams,
            'stat_type':stat_type,
            'seasons':season,
            'leagues':league,
            'team':team,
            
        }

        return render(request, 'stats/histogram.html', context)
    else:
        return JsonResponse({'error': 'Invalid request method'})



def all_games(request):

    seasons = Game.objects.values_list('season_ft', flat=True).distinct().order_by('season_ft')
    leagues = Game.objects.values_list('league', flat=True).distinct().order_by('league')

    leagues = [LEAGUE_MAPPING.get(code, code) for code in leagues]


    context = {
        'leagues': leagues,
        'seasons': seasons,
    }

    return render(request, 'stats/all_games.html', context)


def generate_games(request):
    if request.method == 'GET':
        league = request.GET.get('league')
        season = request.GET.get('season')
        startDate = request.GET.get('start_date')
        endDate = request.GET.get('end_date')
        team = request.GET.get('team','all')
        a = 'a'
        b = 'c'
        league = reverse_LEAGUE_MAPPING.get(league, league)

        if team == 'all' or team == "null":
            
            # Parse start and end dates to datetime objects
            start_date = datetime.strptime(startDate, '%Y-%m-%d')
            end_date = datetime.strptime(endDate, '%Y-%m-%d')

            # Filter games based on league, season, and date range
            #games3 = Game.objects.filter(league=league, season_ft=season, date_of_game_ft__range=(start_date, end_date), home_ft = 'Homegame').values()
            games3 = Game.objects.filter(league=league, season_ft=season, date_of_game_ft__range=(start_date, end_date), home_ft = 'Homegame').values().order_by('date_of_game_ft')
            
            a = 'c'
            teams = Game.objects.filter(league=league, season_ft=season, date_of_game_ft__range=(start_date, end_date)).values_list('team_ft', flat=True).distinct()
            #leagues = Game.objects.values_list('league', flat=True).distinct().order_by('league')
        else: 
            b = 'd'
            # Parse start and end dates to datetime objects
            start_date = datetime.strptime(startDate, '%Y-%m-%d')
            end_date = datetime.strptime(endDate, '%Y-%m-%d')

            # Filter games based on league, season, and date range
            games3 = Game.objects.filter(league=league, season_ft=season, date_of_game_ft__range=(start_date, end_date), team_ft = team).values().order_by('date_of_game_ft')
            teams = Game.objects.filter(league=league, season_ft=season, date_of_game_ft__range=(start_date, end_date)).values_list('team_ft', flat=True).distinct()
        
        #teams = Game.objects.filter(league=league, season_ft=season, date_of_game_ft__range=(start_date, end_date)).values().distinct()
        
        #league = [LEAGUE_MAPPING.get(code, code) for code in league]
        league = LEAGUE_MAPPING.get(league, league)

        context = {
            'games3':games3,
            'startdate': startDate,
            'enddate': endDate,
            'league':league,
            'season':season,
            'teams':teams,
            'team1':team,
            'a':a,
            'b':b


        }


    return render(request, 'stats/detail_games.html', context)


def correlation(request):

    games = Game.objects.all()
    seasons = Game.objects.values_list('season_ft', flat=True).distinct().order_by('season_ft')
    leagues = Game.objects.values_list('league', flat=True).distinct().order_by('league')
    teams = Game.objects.values_list('team_ft', flat=True).distinct().order_by('team_ft')

    leagues = [LEAGUE_MAPPING.get(code, code) for code in leagues]

    context = {'games': games,
               'seasons': seasons,
               'leagues': leagues,
               'teams': teams}


    return render(request, 'stats/correlation.html', context)


def generate_correl(request):

    league = request.GET.get('league')
    season = request.GET.get('season')
    league = reverse_LEAGUE_MAPPING.get(league, league)

    #seasons = Game.objects.values_list('season_ft', flat=True).distinct().order_by('season_ft')
        
    games = Game.objects.filter(league = league, season_ft = season).values()
    #goals_scored_obj = Game.objects.filter(league = league, season_ft = season).values_list('full_time_goals_scored_ft', flat=True)
    #corners_obj = Game.objects.filter(league = league, season_ft = season).values_list('team_corners_recorded_ft', flat=True)

    goals_scored_obj = Game.objects.filter(league=league, season_ft=season).values('full_time_goals_scored_ft')
    goals_conceded_obj = Game.objects.filter(league=league, season_ft=season).values('full_time_goals_conceded_ft')
    goals_scored_obj_FH = Game.objects.filter(league=league, season_ft=season).values('half_time_team_goals_scored_ft')
    goals_conceded_obj_FH = Game.objects.filter(league=league, season_ft=season).values('half_time_team_goals_conceded_ft')
    shots_obj = Game.objects.filter(league=league, season_ft=season).values('team_shots_recorded_ft')
    shots_conceded_obj = Game.objects.filter(league=league, season_ft=season).values('team_shots_conceded_ft')
    shots_OT_obj = Game.objects.filter(league=league, season_ft=season).values('team_shots_on_target_recorded_ft')
    shots_OT_conceded_obj = Game.objects.filter(league=league, season_ft=season).values('team_shots_on_target_conceded_ft')
    fouls_obj = Game.objects.filter(league=league, season_ft=season).values('team_fouls_committed_recorded_ft')
    fouls_against_obj = Game.objects.filter(league=league, season_ft=season).values('team_fouls_committed_conceded_ft')
    corners_obj = Game.objects.filter(league=league, season_ft=season).values('team_corners_recorded_ft')
    corners_conceded_obj = Game.objects.filter(league=league, season_ft=season).values('team_corners_conceded_ft')
    yellow_cards_obj = Game.objects.filter(league=league, season_ft=season).values('team_yellow_cards_recorded_ft')
    yellow_cards_against_obj = Game.objects.filter(league=league, season_ft=season).values('team_yellow_cards_conceded_ft')
    red_cards_obj = Game.objects.filter(league=league, season_ft=season).values('team_red_cards_recorded_ft')
    red_cards_against_obj = Game.objects.filter(league=league, season_ft=season).values('team_red_cards_conceded_ft')
    goal_difference_obj = Game.objects.filter(league=league, season_ft=season).values('goal_difference_ft')
    

    goals_scored = [entry['full_time_goals_scored_ft'] for entry in goals_scored_obj]
    goals_conceded = [entry['full_time_goals_conceded_ft'] for entry in goals_conceded_obj]
    goals_scored_FH = [entry['half_time_team_goals_scored_ft'] for entry in goals_scored_obj_FH]
    goals_conceded_FH = [entry['half_time_team_goals_conceded_ft'] for entry in goals_conceded_obj_FH]
    shots = [entry['team_shots_recorded_ft'] for entry in shots_obj]  
    shots_conceded = [entry['team_shots_conceded_ft'] for entry in shots_conceded_obj]
    shots_OT = [entry['team_shots_on_target_recorded_ft'] for entry in shots_OT_obj]
    shots_OT_conceded = [entry['team_shots_on_target_conceded_ft'] for entry in shots_OT_conceded_obj]
    fouls = [entry['team_fouls_committed_recorded_ft'] for entry in fouls_obj]
    fouls_against = [entry['team_fouls_committed_conceded_ft'] for entry in fouls_against_obj]
    corners = [entry['team_corners_recorded_ft'] for entry in corners_obj]
    corners_conceded = [entry['team_corners_conceded_ft'] for entry in corners_conceded_obj]
    yellow_cards = [entry['team_yellow_cards_recorded_ft'] for entry in yellow_cards_obj]
    yellow_cards_against = [entry['team_yellow_cards_conceded_ft'] for entry in yellow_cards_against_obj]
    red_cards = [entry['team_red_cards_recorded_ft'] for entry in red_cards_obj]
    red_cards_against = [entry['team_red_cards_conceded_ft'] for entry in red_cards_against_obj]
    goal_difference = [entry['goal_difference_ft'] for entry in goal_difference_obj]

    #league = [LEAGUE_MAPPING.get(code, code) for code in league]
    league = LEAGUE_MAPPING.get(league, league)

    context = {'league':league,
               'season':season,
               'games':games,
               'goals_scored': json.dumps(list(goals_scored)),
               'corners': json.dumps(list(corners)),
               'shots': json.dumps(list(shots)),
                'goals_conceded': json.dumps(list(goals_conceded)),
                'goals_scored_FH': json.dumps(list(goals_scored_FH)),
                'goals_conceded_FH': json.dumps(list(goals_conceded_FH)),
                'shots_conceded': json.dumps(list(shots_conceded)),
                'shots_OT': json.dumps(list(shots_OT)),
                'shots_OT_conceded': json.dumps(list(shots_OT_conceded)),
                'fouls': json.dumps(list(fouls)),
                'fouls_against': json.dumps(list(fouls_against)),
                'corners_conceded': json.dumps(list(corners_conceded)),
                'yellow_cards': json.dumps(list(yellow_cards)),
                'yellow_cards_against': json.dumps(list(yellow_cards_against)),
                'red_cards': json.dumps(list(red_cards)),
                'red_cards_against': json.dumps(list(red_cards_against)),
                'goal_difference': json.dumps(list(goal_difference))}
                
    return render(request, 'stats/generate_correl.html', context)

def betting_strategie(request):
    return render(request, 'stats/betting_strat.html')

def KPI_creation(request):
    return render(request, 'stats/KPI_creation.html')



############ me shtu
