import re
import os
import json
import pandas as pd
from datetime import datetime
from chessdotcom import ChessDotComClient

client = ChessDotComClient(user_agent="My app")
dir_cache = "cache/"
titles = ['GM', 'WGM', 'IM', 'WIM', 'FM', 'WFM', 'NM', 'WNM', 'CM', 'WCM']

# ==========================================================================

# res = client.get_club_details()
# res = client.get_club_matches()
# res = client.get_club_members()
# res = client.get_country_clubs()
# res = client.get_country_details()
# res = client.get_country_players()
# res = client.get_current_daily_puzzle()
# res = client.get_leaderboards()
# res = client.get_player_current_games_to_move()
# res = client.get_player_team_matches()
# res = client.get_random_daily_puzzle()
# res = client.get_streamers()
# res = client.get_team_match()
# res = client.get_team_match_board()
# res = client.get_team_match_live()
# res = client.get_team_match_live_board()
    # res = client.get_titled_players()
# res = client.get_tournament_details()
# res = client.get_tournament_round()
# res = client.get_tournament_round_group_details()
# res = client.is_player_online()

    # res=client.get_player_profile()
    # res=client.get_player_stats()
# res=client.get_player_clubs()
# res=client.get_player_game_archives()
# res=client.get_player_games_by_month()
# res=client.get_player_current_games()
# res=client.get_player_games_by_month_pgn()
# res=client.get_player_tournaments()

# ['GM', 'WGM', 'IM', 'WIM', 'FM', 'WFM', 'NM', 'WNM', 'CM', 'WCM']

# ==========================================================================

def getTitledPlayers():
    print("chess.com::getTitledPlayers")
    allTitledPlayersData = pd.DataFrame()
    for title in titles:
        titledUsersDataByTitle = pd.DataFrame()
        path = dir_cache + "chesscom_titledPlayers_" + title + "_.pkl"
        if os.path.exists(path):
            print("Reading " + title + " players...")
            titledUsersDataByTitle = pd.read_pickle(path)
        else:
            print("Processing " + title + " players...")
            users_data_cols = [
                "player_id",
                "id",
                "url",
                "username",
                "followers",
                "country",
                "joined",
                "is_streamer",
                "verified",
                "fide",
            ]

            res = client.get_titled_players(title).players
            for player in res:
                print(player)
                try:
                    pProfile = client.get_player_profile(player)
                    pFide = client.get_player_stats(player).stats.fide
                    pInfo = [
                        pProfile.player.player_id,
                        pProfile.player.id,
                        pProfile.player.url,
                        pProfile.player.username,
                        pProfile.player.followers,
                        pProfile.player.country,
                        str(datetime.fromtimestamp(pProfile.player.joined)),
                        pProfile.player.is_streamer,
                        pProfile.player.verified,
                        pFide,
                    ]
                    pData_df = pd.DataFrame([pInfo], columns=users_data_cols)
                    titledUsersDataByTitle = pd.concat([pData_df, titledUsersDataByTitle], ignore_index=True)
                except Exception as e:
                    print('Failed to process user %s. Account might be deleted' % (player))
                
            titledUsersDataByTitle.to_pickle(path)
        allTitledPlayersData = pd.concat([titledUsersDataByTitle, allTitledPlayersData], ignore_index=True)

    return allTitledPlayersData


def process_chesscom():
    print("chesscom::process_chesscom")
    
    allTitledPlayersData = getTitledPlayers()
    print(allTitledPlayersData)
