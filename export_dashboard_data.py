"""
Export data from COTA_Race_Story_Analysis.ipynb for dashboard use.
Run this script after executing all cells in the notebook.
"""

import pandas as pd
import json
from pathlib import Path

# This script should be run from within the notebook environment
# or after importing the notebook's namespace

def export_dashboard_data():
    """Export all dashboard-ready data structures to files."""
    
    # Check if variables exist (they should be in globals after running notebook)
    try:
        # Export position data
        if 'viz_position' in globals() and not viz_position.empty:
            viz_position.to_csv('dashboard_data/viz_position.csv', index=False)
            print("✓ Exported viz_position.csv")
        
        # Export sector data
        if 'viz_sectors' in globals() and not viz_sectors.empty:
            viz_sectors.to_csv('dashboard_data/viz_sectors.csv', index=False)
            print("✓ Exported viz_sectors.csv")
        
        # Export driver comparison
        if 'driver_comparison' in globals() and not driver_comparison.empty:
            driver_comparison.to_csv('dashboard_data/driver_comparison.csv', index=False)
            print("✓ Exported driver_comparison.csv")
        
        # Export key moments
        if 'key_moments' in globals() and not key_moments.empty:
            key_moments.to_csv('dashboard_data/key_moments.csv', index=False)
            print("✓ Exported key_moments.csv")
        
        # Export story texts
        if 'story_texts' in globals() and not story_texts.empty:
            story_texts.to_csv('dashboard_data/story_texts.csv', index=False)
            print("✓ Exported story_texts.csv")
        
        # Export protagonists
        if 'protagonists_df' in globals() and not protagonists_df.empty:
            protagonists_df.to_csv('dashboard_data/protagonists_df.csv', index=False)
            print("✓ Exported protagonists_df.csv")
        
        # Export turning points
        if 'turning_points_df' in globals() and not turning_points_df.empty:
            turning_points_df.to_csv('dashboard_data/turning_points_df.csv', index=False)
            print("✓ Exported turning_points_df.csv")
        
        # Export dashboard summary as JSON
        if 'dashboard_summary' in globals():
            with open('dashboard_data/dashboard_summary.json', 'w') as f:
                json.dump(dashboard_summary, f, indent=2)
            print("✓ Exported dashboard_summary.json")
        
        print("\n✅ All data exported successfully to 'dashboard_data/' directory!")
        
    except NameError as e:
        print(f"⚠️  Error: {e}")
        print("Please run all cells in COTA_Race_Story_Analysis.ipynb first!")
        print("Then run this script from within the notebook or import the namespace.")

if __name__ == "__main__":
    # Create dashboard_data directory
    Path('dashboard_data').mkdir(exist_ok=True)
    export_dashboard_data()

