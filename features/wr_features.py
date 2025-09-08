import pandas as pd
import sys

class WRFeatureCreator:
  @staticmethod
  def create_features(receiving_df: pd.DataFrame) -> pd.DataFrame:
    if receiving_df.empty:
      return pd.DataFrame()
    
    df = receiving_df.copy()
    df = df[df['Tgt'] >= 30].copy() # At least 30 targets

    print(f"Creating WR/TE features for {len(df)} pass catchers")

    # RELIABILITY & HANDS
    df['Catch_Rate'] = df['Rec%']
    df['Targets_Per_Game'] = df['Tgt'] / df['G']
    df['Receptions_Per_Game'] = df['R/G']

    # EFFICIENCY & PRODUCTIVITY
    df['Yards_Per_Reception'] = df['Y/R']
    df['Yards_Per_Target'] = df['Y/Tgt']
    df['Yards_Per_Game'] = df['Y/G']
    df['TD_Rate'] = df['TD'] / df['Rec']

    # BIG PLAY ABILITY
    df['Long_Reception_Ability'] = df['Lng'] / df['Rec']
    df['Explosive_Recptions'] = df['Lng'] / df['Yds']

    # USAGE & ROLE
    df['Target_Share_Proxy'] = df['Targets_Per_Game'] # Higher means more involved in offense
    df['Red_Zone_Threat'] = df['TD'] / df['Yds'] * 1000 # TDs per 1000 yds

    # SECURITY
    df['Fumble_Rate'] = df['Fmb'] / df['Rec']

    wr_features = [
      'Catch_Rate', 'Targets_Per_Game', 'Receptions_Per_Game', 'Yards_Per_Reception',
      'Yards_Per_Target', 'Yards_Per_Game', 'TD_Rate', 'Long_Reception_Ability',
      'Explosive_Receptions', 'Target_Share_Proxy', 'Red_Zone_Threat', 'Fumble_Rate'
    ]

    id_columns = ['Player_Clean', 'Tm', 'Pos', 'Age', 'G', 'GS']
    final_df = df[id_columns + wr_features].copy()
    final_df = final_df.fillna(0)

    return final_df