import pandas as pd
import sys

class RBFeatureCreator:
  @staticmethod
  def create_features(rushing_df: pd.DataFrame) -> pd.DataFrame:
    """Create features for RB archetypes"""
    if rushing_df.empty:
      return pd.DataFrame()
    
    df = rushing_df.copy()
    df = df[df['Att'] >= 50].copy() # At least 50 carries

    print(f"Creating RB features for {len(df)} running backs")

    # EFFICIENCY
    df['Yards_Per_Carry'] = df['Y/A']
    df['Yards_Per_Game'] = df['Y/G']
    df['Rush_TD_Rate'] = df['TD'] / df['Att']

    # VOLUME & USAGE
    df['Carries_Per_Game'] = df['Att'] / df['G']
    df['Total_Rushing_Yards'] = df['Yds']

    # BIG PLAY ABILITY
    df['Long_Run_Ability'] = df['Lng'] / df['Att']
    df['Explosive_Runs'] = df['Lng'] / df['Yds'] # Portion of yds from longest run

    # DURABILITY/USAGE
    df['Games_Started_Pct'] = df['GS'] / df['G']
    df['Fumble_Rate'] = df['Fmb'] / df['Att']

    rb_features = [
      'Yards_Per_Carry', 'Yards_Per_Game', 'Rush_TD_Rate', 'Carries_Per_Game',
      'Total_Rushing_Yards', 'Long_Run_Ability', 'Explosive_Runs', 
      'Games_Started_Pct', 'Fumble_Rate'
    ]

    id_columns = ['Player_Clean', 'Tm', 'Age', 'G', 'GS']
    final_df = df[id_columns + rb_features].copy()
    final_df = final_df.fillna(0)

    return final_df