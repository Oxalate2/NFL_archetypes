import pandas as pd

def explore_nfl_features(qb_df: pd.DataFrame, rb_df: pd.DataFrame, wr_df: pd.DataFrame):
  """Explore the created NFL features"""
  print("\n=== NFL DATA EXPLORATION ===")

  if not qb_df.empty:
    print(f"\n--- QUARTERBACKS ({len(qb_df)} players) ---")
    print("Top 5 by Passer Rating:")
    top_qbs = qb_df.nlargest(5, 'Passer_Rating')[['Player_Clean', 'Passer_Rating', 'TD_INT_Ratio', 'Yards_Per_Attempt']]
    print(top_qbs)
        
  if not rb_df.empty:
    print(f"\n--- RUNNING BACKS ({len(rb_df)} players) ---")
    print("Top 5 by Yards Per Carry:")
    top_rbs = rb_df.nlargest(5, 'Yards_Per_Carry')[['Player_Clean', 'Yards_Per_Carry', 'Yards_Per_Game', 'Rush_TD_Rate']]
    print(top_rbs)
        
  if not wr_df.empty:
    print(f"\n--- PASS CATCHERS ({len(wr_df)} players) ---")
    print("Top 5 by Yards Per Game:")
    top_wrs = wr_df.nlargest(5, 'Yards_Per_Game')[['Player_Clean', 'Yards_Per_Game', 'Catch_Rate', 'Yards_Per_Reception']]
    print(top_wrs)