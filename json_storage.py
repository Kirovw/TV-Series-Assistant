"""
JSON storage utility for saving and loading series data
"""

import json
import os
from series import Series

class JSONStorage:
    """Handle saving and loading series data from JSON files"""
    
    def __init__(self, filename="series_data.json"):
        """
        Initialize JSONStorage
        
        Args:
            filename (str): Name of the JSON file to store data
        """
        self.filename = filename
    
    def save_series(self, series_list):
        """
        Save all series to a JSON file
        
        Args:
            series_list (list): List of Series objects to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = []
            for series in series_list:
                series_data = {
                    'name': series.name,
                    'total_episodes': series.total_episodes,
                    'genre': series.genre,
                    'episodes_watched': series.episodes_watched
                }
                data.append(series_data)
            
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
            
            print(f"✅ Data saved to '{self.filename}'")
            return True
        
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def load_series(self):
        """
        Load all series from the JSON file
        
        Returns:
            list: List of Series objects, empty list if file doesn't exist
        """
        if not os.path.exists(self.filename):
            print(f"📭 No saved data found. Starting fresh!")
            return []
        
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            
            series_list = []
            for item in data:
                series = Series(
                    name=item['name'],
                    total_episodes=item['total_episodes'],
                    genre=item.get('genre', 'Unknown')
                )
                series.episodes_watched = item.get('episodes_watched', 0)
                series_list.append(series)
            
            print(f"✅ Loaded {len(series_list)} series from '{self.filename}'")
            return series_list
        
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return []
    
    def file_exists(self):
        """Check if the JSON file exists"""
        return os.path.exists(self.filename)
