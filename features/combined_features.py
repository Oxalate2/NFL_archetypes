import pandas as pd
import sys

class CombinedFeatureCreator:
  @staticmethod
  def create_combined_offensive_features(qb_df: pd.DataFrame, rb_df: pd.DataFrame, wr_df: pd.DataFrame) -> pd.DataFrame:
    """Combine all offsensive players into single dataset with normalized features"""
    combined_dfs = []

    if not qb_df.empty:
      qb_norm = qb_df.copy()
      qb_norm['Position_Group'] = 'QB'

      # Standardize column names for QBs
      qb_norm['Yards_Per_Game'] = qb_norm['Pass_Yards_Per_Game']
      qb_norm['Touches_Per_Game'] = qb_norm['Pass_Attempts_Per_Game']
      qb_norm['Efficiency'] = qb_norm['Passer_Rating'] / 100  # Normalize to 0-1 scale
      qb_norm['Big_Play_Ability'] = qb_norm['Deep_Ball_Ability']
      qb_norm['Turnover_Rate'] = qb_norm['INT_Rate']
      
      combined_dfs.append(qb_norm)

    if not rb_df.empty:
      rb_norm = rb_df.copy()
      rb_norm['Position_Group'] = 'RB'
      
      # Standardize column names for RBs
      rb_norm['Touches_Per_Game'] = rb_norm['Carries_Per_Game']
      rb_norm['Efficiency'] = rb_norm['Yards_Per_Carry'] / 10  # Normalize to similar scale
      rb_norm['Big_Play_Ability'] = rb_norm['Long_Run_Ability']
      rb_norm['Turnover_Rate'] = rb_norm['Fumble_Rate']
      
      combined_dfs.append(rb_norm)
        
    if not wr_df.empty:
      wr_norm = wr_df.copy()
      wr_norm['Position_Group'] = 'WR_TE'
      
      # Standardize column names for WRs
      wr_norm['Touches_Per_Game'] = wr_norm['Targets_Per_Game']
      wr_norm['Efficiency'] = wr_norm['Catch_Rate'] / 100  # Normalize to 0-1 scale
      wr_norm['Big_Play_Ability'] = wr_norm['Long_Reception_Ability']
      wr_norm['Turnover_Rate'] = wr_norm['Fumble_Rate']
      
      combined_dfs.append(wr_norm)

    if combined_dfs:
      # Find common columns across all positions
      common_cols = ['Player_Clean', 'Tm', 'Age', 'G', 'Position_Group', 
                      'Yards_Per_Game', 'Touches_Per_Game', 'Efficiency', 
                      'Big_Play_Ability', 'Turnover_Rate']
      
      # Only include columns that exist in all dataframes
      final_cols = []
      for col in common_cols:
        if all(col in df.columns for df in combined_dfs):
          final_cols.append(col)

      combined_data = []
      for df in combined_dfs:
        combined_data.append(df[final_cols])
        
      result = pd.concat(combined_data, ignore_index=True)
      result = result.fillna(0)
      
      print(f"Combined offensive dataset: {len(result)} total players")
      print(f"- QBs: {len(result[result['Position_Group'] == 'QB'])}")
      print(f"- RBs: {len(result[result['Position_Group'] == 'RB'])}")
      print(f"- WR/TEs: {len(result[result['Position_Group'] == 'WR_TE'])}")
      
      return result
    
    return pd.DataFrame()