import pandas as pd
import sys
import os

from data.collector import NFLDataCollector
from features.qb_features import QBFeatureCreator
from features.rb_features import RBFeatureCreator
from features.wr_features import WRFeatureCreator
from features.combined_features import CombinedFeatureCreator
from utils.exploration import explore_nfl_features

def main():
  """Main execution function"""
  print("=== NFL PLAYER ARCHETYPE ANALYSIS ===")
  
  # Initialize collector
  collector = NFLDataCollector(season=2023)
  
  # Collect all data
  print("\n1. Collecting data...")
  raw_data = collector.collect_all_data()
  
  # Create position-specific features using separate feature creators
  print("\n2. Creating features...")
  qb_features = QBFeatureCreator.create_features(raw_data.get('passing', pd.DataFrame()))
  rb_features = RBFeatureCreator.create_features(raw_data.get('rushing', pd.DataFrame()))  
  wr_features = WRFeatureCreator.create_features(raw_data.get('receiving', pd.DataFrame()))
  
  # Create combined offensive dataset
  combined_offensive = CombinedFeatureCreator.create_combined_offensive_features(
    qb_features, rb_features, wr_features
  )
  
  # Save processed data
  print("\n3. Saving data...")
  if not qb_features.empty:
    qb_features.to_csv("nfl_qb_features_2023.csv", index=False)
    print(f"Saved QB features: {len(qb_features)} players")
  if not rb_features.empty:
    rb_features.to_csv("nfl_rb_features_2023.csv", index=False)
    print(f"Saved RB features: {len(rb_features)} players")
  if not wr_features.empty:
    wr_features.to_csv("nfl_wr_features_2023.csv", index=False)
    print(f"Saved WR features: {len(wr_features)} players")
  if not combined_offensive.empty:
    combined_offensive.to_csv("nfl_offensive_combined_2023.csv", index=False)
    print(f"Saved combined features: {len(combined_offensive)} players")
  
  # Explore the data
  print("\n4. Exploring data...")
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

if __name__ == "__main__":
  main()