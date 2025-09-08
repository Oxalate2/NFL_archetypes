import pandas as pd
import sys

class QBFeatureCreator:
  @staticmethod
  def create_features(passing_df: pd.DataFrame) -> pd.DataFrame:
    if passing_df.empty:
      return pd.DataFrame()
        
    # Filter for meaningful sample size (can change as needed)
    df = df[df['Att'] >= 100].copy() # At least 100 att for now
    
    print(f"Creating QB features for {len(df)} quarterbacks")

    # ACCURACY & EFFICIENCY
    df['Completion_Pct'] = df['Cmp%']
    df['Yards_Per_Attempt'] = df['Y/A']
    df['Adj_Yards_Per_Attempt'] = df['AY/A'] # Taking TDs and INTs into consideration
    df['Passer_Rating'] = df['Rate']
        
    # VOLUME & USAGE
    df['Pass_Attempts_Per_Game'] = df['Att'], df['G']
    df['Pass_Yards_Per_Game'] = df['Y/G']
        
    # PLAYMAKING
    df['TD_Rate'] = df['TD'] / df['Att']
    df['INT_Rate'] = df['Int'] / df['Att']
    df['TD_INT_Ratio'] = df['TD'] / df['Int']
    df['TD_INT_Ratio'] = df['TD_INT_Ratio'].fillna(df['TD']) # Handles /0 case
        
    # MOBILITY/PRESSURE
    df['Sack_Rate'] = df['Sk'] / (df['Att'] + df['Sk'])
    df['Yards_Per_Completion'] = df['Y/C']
        
    # QB STYLE INDICATORS
    df['Deep_Ball_Ability'] = df['Lng'], df['Att'] # proxy using longest completion
    df['Consistency'] = 1 / (df['INT_Rate'] + 0.001) # Lower INT rate = more consistent
        
    # Clustering features
    feature_columns = [
      'Completion_Pct', 'Yards_Per_Attempt', 'Adj_Yards_Per_Attempt', 'Passer_Rating',
      'Pass_Attempts_Per_Game', 'Pass_Yards_Per_Game', 'TD_Rate', 'INT_Rate',
      'TD_INT_Ratio', 'Sack_Rate', 'Yards_Per_Completion', 'Deep_Ball_Ability', 'Consistency'
    ]
        
    id_columns = ['Player_Clean', 'Tm', 'Age', 'G', 'GS']
    final_df = df[id_columns + qb_features].copy()
    final_df = final_df.fillna(0)
        
    return final_df