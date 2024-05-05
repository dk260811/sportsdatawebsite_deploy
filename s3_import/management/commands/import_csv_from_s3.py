import csv
from io import StringIO
from django.core.management.base import BaseCommand
from stats.models import Game
import boto3

class Command(BaseCommand):
    help = 'Import CSV file from S3 and save to Game model'

    def handle(self, *args, **options):
        # Configure AWS credentials
        aws_access_key_id = 'AKIA5FTZCF35QK2ZHU4L'
        aws_secret_access_key = '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'
        aws_region = 'eu-north-1'

        # Create S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )

        # S3 bucket and file details
        bucket_name = 'footwebbucket'
        key = 'summarize.csv'

        # Retrieve CSV file from S3
        response = s3.get_object(Bucket=bucket_name, Key=key)
        csv_data = response['Body'].read().decode('utf-8')

        # Parse CSV data
        csv_file = StringIO(csv_data)
        reader = csv.DictReader(csv_file)

        # Save data to Game model
        for row in reader:
            Game.objects.create(
                date_of_game_ft=row['date_of_game_ft'],
                time_ft=row['time_ft'],
                team_ft=row['team_ft'],
                opponent_ft=row['opponent_ft'],
                full_time_goals_scored_ft=row['full_time_goals_scored_ft'],
                full_time_goals_conceded_ft=row['full_time_goals_conceded_ft'],
                home_ft=row['home_ft'],
                game_outcome_ft=row['game_outcome_ft'],
                win_ft=row['win_ft'],
                draw_ft=row['draw_ft'],
                loss_ft=row['loss_ft'],
                points_ft=row['points_ft'],
                half_time_team_goals_scored_ft=row['half_time_team_goals_scored_ft'],
                half_time_team_goals_conceded_ft=row['half_time_team_goals_conceded_ft'],
                half_time_win_ft=row['half_time_win_ft'],
                half_time_draw_ft=row['half_time_draw_ft'],
                half_time_loss_ft=row['half_time_loss_ft'],
                referee_ft=row['referee_ft'],
                team_shots_recorded_ft=row['team_shots_recorded_ft'],
                team_shots_conceded_ft=row['team_shots_conceded_ft'],
                team_shots_on_target_recorded_ft=row['team_shots_on_target_recorded_ft'],
                team_shots_on_target_conceded_ft=row['team_shots_on_target_conceded_ft'],
                team_fouls_committed_recorded_ft=row['team_fouls_committed_recorded_ft'],
                team_fouls_committed_conceded_ft=row['team_fouls_committed_conceded_ft'],
                team_corners_recorded_ft=row['team_corners_recorded_ft'],
                team_corners_conceded_ft=row['team_corners_conceded_ft'],
                team_yellow_cards_recorded_ft=row['team_yellow_cards_recorded_ft'],
                team_yellow_cards_conceded_ft=row['team_yellow_cards_conceded_ft'],
                team_red_cards_recorded_ft=row['team_red_cards_recorded_ft'],
                team_red_cards_conceded_ft=row['team_red_cards_conceded_ft'],
                half_time_outcome_ft=row['half_time_outcome_ft'],
                season_ft=row['season_ft'],
                goal_difference_ft=row['goal_difference_ft'],
                league=row['league_ft'],
                more_corners_ft=row['more_corners_ft'],
                more_cards_ft=row['more_cards_ft'],
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
