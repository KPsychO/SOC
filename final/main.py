import re
import pandas as pd
from datetime import datetime
from chessdotcom import ChessDotComClient

client = ChessDotComClient(user_agent = "My app")

# ==========================================================================

#res = client.get_club_details()
#res = client.get_club_matches()
#res = client.get_club_members()
#res = client.get_country_clubs()
#res = client.get_country_details()
#res = client.get_country_players()
#res = client.get_current_daily_puzzle()
#res = client.get_leaderboards()
#res = client.get_player_current_games_to_move()
#res = client.get_player_team_matches()
#res = client.get_random_daily_puzzle()
#res = client.get_streamers()
#res = client.get_team_match()
#res = client.get_team_match_board()
#res = client.get_team_match_live()
#res = client.get_team_match_live_board()
#res = client.get_titled_players()
#res = client.get_tournament_details()
#res = client.get_tournament_round()
#res = client.get_tournament_round_group_details()
#res = client.is_player_online()

#res=client.get_player_profile()
#res=client.get_player_stats()
#res=client.get_player_clubs()
#res=client.get_player_game_archives()
#res=client.get_player_games_by_month()
#res=client.get_player_current_games()
#res=client.get_player_games_by_month_pgn()
#res=client.get_player_tournaments()

# ==========================================================================

def get_top_players_info():
    users_data_cols = ["player_id", "id", "url", "username", "followers", "country", "joined", "is_streamer", "verified", "fide"]
    top_users_data = pd.DataFrame()

    res = client.get_leaderboards(1)
    all = res.leaderboards.daily

    for i in range(0, len(all)):
        usnme = all[i].username
        res = client.get_player_profile(usnme)
        fide = client.get_player_stats(usnme).stats.fide
        info = [res.player.player_id, res.player.id, res.player.url, res.player.username, res.player.followers, res.player.country, datetime.fromtimestamp(res.player.joined), res.player.is_streamer, res.player.verified, fide]
        aux = pd.DataFrame([info], columns=users_data_cols)
        top_users_data = pd.concat([aux, top_users_data], ignore_index = True)

    return top_users_data

def get_country_clubs_data(country_code):

    regex = "https://api.chess.com/pub/club/(.*)"
    club_data_cols = ["id", "name", "club_id", "average_daily_rating", "members_count", "created"]

    country_clubs_data = pd.DataFrame()

    clubs = client.get_country_clubs(country_code, 1).clubs
    for c in clubs:
        club_name = re.findall(regex, c)[0]
        res = client.get_club_details(club_name)
        info = [res.club.id, res.club.name, res.club.club_id, res.club.average_daily_rating, res.club.members_count, datetime.fromtimestamp(res.club.created)]
        aux = pd.DataFrame([info], columns=club_data_cols)
        country_clubs_data = pd.concat([aux, country_clubs_data], ignore_index = True)

    return country_clubs_data

country_clubs_data = get_country_clubs_data("ES")   # TODO: Parametrizar el pais de los clubs a estudiar
print(country_clubs_data)

#top_users_data = get_top_players_info()
