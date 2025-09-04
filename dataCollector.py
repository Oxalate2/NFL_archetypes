import pandas as pd
import numpy as np
import requests
import time
from typing import Dict, List, Optional
from bs4 import BeautifulSoup

class NFLDataCollector:
  def __init__(self, season: int = 2023):
    """
    Initialize NFL data collector
    Args:
      season: NFL season year (e.g., 2023)
    """
    self.season = season
    self.base_url = "https://www.pro-football-reference.com"
    self.session = requests.Session()
    self.session.headers.update({
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })

  def get_passing_stats(self) -> pd.DataFrame:
    """Get QB passing stats"""
    url = f"{self.base_url}/years/{self.season}/passing.htm"

    try:
      print("Fetching QB passing stats...")
      response = self.session.get(url)
      response.raise_for_status()

      tables = pd.read_html(response.content)
      df = tables[0] # 1st table is usually passing stats

      # Cleaning data
      df = self.clean_clean_passing_data(df)
      df['Position_Group'] = 'QB'

      return df
    
    except Exception as e:
      print(f"Error fetching passing stats: {e}")
      return pd.DataFrame()

  def get_rushing_stats(self) -> pd.DataFrame:
    """Get running back and rushing statistics"""
    url = f"{self.base_url}/years/{self.season}/rushing.htm"

    try:
      print("Fetching rushing stats...")
      response = self.session.get(url)
      response.raise_for_status()

      tables = pd.read_html(response.content)
      df = tables[0]

      df = self._clean_rushing_data(df)
      df['Position_Group'] = 'RB'

      return df
    
    except Exception as e:
      print(f"Error fetching rushing stats: {e}")
      return pd.DataFrame()
    
  def get_receiving_stats(self) -> pd.DataFrame:
    """Get WR and receiving stats"""
    url = f"{self.base_url}/years/{self.season}/receiving.htm"

    try:
      print("Fetching receiving stats...")
      response = self.session.get(url)
      response.raise_for_status()

      tables = pd.read_html(response.content)
      df = tables[0]

      df = self._clean_receiving_data(df)
      df['Position_Group'] = 'PASS_CATCHER'

      return df
    except Exception as e:
      print(f"Error fetching receiving stats: {e}")
      return pd.DataFrame()
    
  def get_defensive_stats(self) -> pd.DataFrame:
    """Get defensive player stats"""
    url = f"{self.base_url}/years/{self.season}/opp.htm"

    try:
      print("Fetching devensive stats...")
      response = self.session.get(url)
      response.raise_for_status()

      # Different approach for individual def stats
      def_url = f"{self.base_url}/years/{self.season}/defense.htm"
      response = self.session.get(def_url)

      tables = pd.read_html(response.content)
      df = tables[0]

      df = self._clean_defensive_data(df)
      df['Position_Group'] = 'DEFENSE'

      return df
    
    except Exception as e:
      print(f"Error fetching defensive stats: {e}")
      return pd.DataFrame()
    
  def _clean_passing_data(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean QB passing data"""
    # Remove heading rows
    df = df[df['Player'] != 'Player']

    # Convert numeric columns
    numeric_cols = ['Age', 'G', 'GS', 'Cmp', 'Att', 'Cmp%', 'Yds', 'TD', 'Int', 
                    'Rate', 'QBR', 'Sk', 'Yds.1', 'Y/A', 'AY/A', 'Y/C', 'Y/G', 
                    'QBrec', 'Lng']
    
    for col in numeric_cols:
      if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Player_Clean'] = df['Player'].str.replace('*', '', regex=False).str.replace('+', '', regex=False)

    return df

  def _clean_rushing_data(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean RB rushing data"""
    df = df[df['Player'] != 'Player']

    numeric_cols = ['Age', 'G', 'GS', 'Att', 'Yds', 'TD', 'Lng', 'Y/A', 'Y/G', 'Fmb']

    for col in numeric_cols:
      if col in df.columns:
        df[col] = pd.to_numeric(df[col], error='coerce')

    df['Player_Clean'] = df['Player'].str.replace('*', '', regex=False).str.replace('+', '', regex=False)

    return df
  
  def _clean_receiving_data(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean wide receiver receiving data"""
    df = df[df['Player'] != 'Player']
        
    numeric_cols = ['Age', 'G', 'GS', 'Tgt', 'Rec', 'Yds', 'Y/R', 'TD', 
                    'Lng', 'R/G', 'Y/G', 'Fmb', 'Y/Tgt', 'Rec%']
        
    for col in numeric_cols:
      if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    df['Player_Clean'] = df['Player'].str.replace('*', '', regex=False).str.replace('+', '', regex=False)
        
    return df

  def _clean_defensive_data(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean defensive player data"""
    df = df[df['Player'] != 'Player']

    numeric_cols = ['Age', 'G', 'GS', 'Int', 'Yds', 'TD', 'Lng', 'PD', 'FF', 
                    'Fmb', 'FR', 'Yds.1', 'TD.1', 'Sk', 'Comb', 'Solo', 'Ast']
    
    for col in numeric_cols:
      if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Player_Clean'] = df['Player'].str.replace('*', '', regex=False).str.replace('+', '', regex=False)
          
    return df

  def collect_all_data(self) -> Dict[str, pd.DataFrame]:
    """Collect comprehensive NFL dataset"""
    print(f"Starting comprehensive NFL data collection for {self.season} season...")

    data = {}

    # QB stats
    data['passing'] = self.get_passing_stats()
    time.sleep(2) # So you can't spam the server

    # RB stats
    data['rushing'] = self.get_rushing_stats()
    time.sleep(2)

    # WR stats
    data['receiving'] = self.get_receiving_stats
    time.sleep(2)

    # Def stats
    data['defense'] = self.get_defensive_stats()
    time.sleep(2)

    print("NFL data collection complete!")
    return data
  
  def create_qb_features(self, passing_df: pd.DataFrame) -> pd.DataFrame:
    """Create features specifically for QB archetypes"""
    if passing_df.empty:
      return pd.DataFrame()
    
    df = passing_df.copy()

    # Filter for a reasonable sample size (can change as needed)
    df = df[df['Att'] >= 100].copy() # At least 100 att for now

    print(f"Creating QB features for {len(df)} quaterbacks")

    # ACCURACY & EFFICIENCY
    df['Completion_Pct'] = df['Cmp%']
    df['Yards_Per_Attempt'] = df['Y/A']
    df['Adj_Yards_Per_Attempt'] = df['AY/A'] # Takes TDs and INTs into consideration
    df['Passer_Rating'] = df['Rate']

    # VOLUME & USAGE
    df['Pass_Attempts_Per_Game'] = df['Att'] / df['G']
    df['Pass_Yards_Per_Game'] = df['Y/G']

    # PLAYMAKING
    df['TD_Rate'] = df['TD'] / df['Att']
    df['INT_Rate'] = df['Int'] / df['Att']
    df['TD_INT_Ratio'] = df['TD'] / df['Int']
    df['TD_INT_Ratio'] = df['TD_INT_Ratio'].fillna(df['TD'])  # Handle division by zero
        
    # MOBILITY/PRESSURE
    df['Sack_Rate'] = df['Sk'] / (df['Att'] + df['Sk'])
    df['Yards_Per_Completion'] = df['Y/C']
     
    # QB STYLE INDICATORS
    df['Deep_Ball_Ability'] = df['Lng'] / df['Att']  # Proxy using longest completion
    df['Consistency'] = 1 / (df['INT_Rate'] + 0.001)  # Lower INT rate = more consistent

    # Chosen features for clustering
    qb_features = [
      'Completion_Pct', 'Yards_Per_Attempt', 'Adj_Yards_Per_Attempt', 'Passer_Rating',
      'Pass_Attempts_Per_Game', 'Pass_Yards_Per_Game', 'TD_Rate', 'INT_Rate',
      'TD_INT_Ratio', 'Sack_Rate', 'Yards_Per_Completion', 'Deep_Ball_Ability', 'Consistency'
    ]

    id_columns = ['Player_Clean', 'Tm', 'Age', 'G', 'GS']
    final_df = df[id_columns + qb_features].copy()
    final_df = final_df.fillna(0)

    return final_df
  
  def create_rb_features(self, rushing_df: pd.DataFrame) -> pd.DataFrame:
    """Create features for RB archetypes"""
    if rushing_df.empty:
      return pd.DataFrame()
    
    df = rushing_df.copy()
    df = df[df['Att'] >= 50].copy()  # At least 50 carries
        
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
    df['Explosive_Runs'] = df['Lng'] / df['Yds']  # Portion of yards from longest run
        
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
  
  def create_wr_features(self, receiving_df: pd.DataFrame) -> pd.DataFrame:
    """Create features for WR/TE archetypes"""
    if receiving_df.empty:
      return pd.DataFrame()
    
    df = receiving_df.copy()
    df = df[df['Tgt'] >= 30].copy() # At least 30 targets

    print(f"Creating WR/TE features for {len(df)} pass catchers")

    # RELAIBILITY & HANDS
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
    df['Explosive_Receptions'] = df['Lng'] / df['Yds']

    # USAGE & ROLE
    df['Target_Share_Proxy'] = df['Targets_Per_Game'] # Higher means more involved in offense
    df['Red_Zone_Target'] = df['TD'] / df['Yds'] * 1000 # TDs per 1000 yards

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

if __name__ == "__main__":
  # Initialize collector
  collector = NFLDataCollector(season=2023)
    
  # Collect all data
  raw_data = collector.collect_all_data()
    
  # Create position-specific features
  qb_features = collector.create_qb_features(raw_data.get('passing', pd.DataFrame()))
  rb_features = collector.create_rb_features(raw_data.get('rushing', pd.DataFrame()))  
  wr_features = collector.create_wr_features(raw_data.get('receiving', pd.DataFrame()))
    
  # Create combined offensive dataset
  combined_offensive = collector.create_combined_offensive_features(qb_features, rb_features, wr_features)
    
  # Save processed data
  if not qb_features.empty:
      qb_features.to_csv("nfl_qb_features_2023.csv", index=False)
  if not rb_features.empty:
      rb_features.to_csv("nfl_rb_features_2023.csv", index=False)
  if not wr_features.empty:
      wr_features.to_csv("nfl_wr_features_2023.csv", index=False)
  if not combined_offensive.empty:
      combined_offensive.to_csv("nfl_offensive_combined_2023.csv", index=False)
    
  # Explore the data
  explore_nfl_features(qb_features, rb_features, wr_features)
    
  print(f"\n=== READY FOR NFL OFFENSIVE ARCHETYPE ANALYSIS ===")
  print("Position groups ready for clustering:")
  print(f"- Quarterbacks: {len(qb_features)} players")
  print(f"- Running Backs: {len(rb_features)} players") 
  print(f"- Pass Catchers: {len(wr_features)} players")
  print(f"- Combined Offensive: {len(combined_offensive)} players")
  print("\nExpected QB archetypes: Elite pocket passers, mobile QBs, game managers, gunslingers")
  print("Expected RB archetypes: Power backs, speed backs, receiving backs, workhorses")
  print("Expected WR archetypes: Deep threats, possession receivers, slot specialists, red zone targets")
  print("Expected Combined archetypes: Elite playmakers, volume players, efficiency specialists, big-play threats")
        