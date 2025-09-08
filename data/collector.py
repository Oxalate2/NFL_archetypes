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
      df = tables[0] # 1st table usually where passing stats are

      # Cleaning data
      df = self._clean_passing_data(df) # Fixed method name
      df['Position_Group'] = 'QB'

      return df
    except Exception as e:
      print(f"Error fetching passing stats: {e}")
      return pd.DataFrame()
    
  def get_rushing_stats(self) -> pd.DataFrame:
    """Get RB and rushing stats"""
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
    """Get WR and TE receiving stats"""
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
        df[col] = pd.to_numeric(df[col], errors = 'coerce')

    df['Player_Clean'] = df['Player'].str.replace('*', '', regex=False).str.replace('+', '', regex=False)

    return df
  
  def _clean_rushing_data(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean RB rushing data"""
    df = df[df['Player'] != 'Player']

    numeric_cols = ['Age', 'G', 'GS', 'Att', 'Yds', 'TD', 'Lng', 'Y/A', 'Y/G', 'Fmb']

    for col in numeric_cols:
      if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Player_Clean'] = df['Player'].str.replace('*', '', regex=False).str.replace('+', '', regex=False)

    return df
  
  def _clean_receiving_data(self, df: pd.DataFrame) -> pd.DataFrame:
    """Clean WR and TE receiving data"""
    df = df[df['Player'] != 'Player']

    numeric_cols = ['Age', 'G', 'GS', 'Tgt', 'Rec', 'Yds', 'Y/R', 'TD', 
                    'Lng', 'R/G', 'Y/G', 'Fmb', 'Y/Tgt', 'Rec%']
    
    for col in numeric_cols:
      if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
            
    df['Player_Clean'] = df['Player'].str.replace('*', '', regex=False).str.replace('+', '', regex=False)

    return df
  def collect_all_data(self) -> Dict[str, pd.DataFrame]:
    """Collect comprehensive NFL offensive dataset"""
    print(f"Starting comprehensive NFL data collection for {self.season} season...")

    data = {}

    # QB stats
    data['passing'] = self.get_passing_stats()
    time.sleep(2) # So you can't spam the server

    # RB stats
    data['rushing'] = self.get_rushing_stats()
    time.sleep(2)

    # WR & TE stats
    data['receiving'] = self.get_receiving_stats()
    time.sleep(2)

    print("NFL offensive data collection complete!")
    return data