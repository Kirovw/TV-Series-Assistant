"""
SeriesManager class - Manages a collection of TV series
"""

from series import Series
from json_storage import JSONStorage

class SeriesManager:
    """A class to manage multiple TV series"""
    
    def __init__(self, storage=None):
        """
        Initialize the SeriesManager
        
        Args:
            storage (JSONStorage): Optional storage handler for persistence
        """
        self.series_list = []
        self.storage = storage
    
    def add_series(self, name, total_episodes, genre="Unknown"):
        """
        Add a new series to the manager
        
        Args:
            name (str): The name of the series
            total_episodes (int): Total number of episodes
            genre (str): The genre of the series
        """
        # Check if series already exists
        if self.find_series(name):
            print(f"⚠️  '{name}' already exists in your list!")
            return False
        
        new_series = Series(name, total_episodes, genre)
        self.series_list.append(new_series)
        self._save()
        return True
    
    def find_series(self, name):
        """
        Find a series by name
        
        Args:
            name (str): The name of the series to find
            
        Returns:
            Series object if found, None otherwise
        """
        for series in self.series_list:
            if series.name.lower() == name.lower():
                return series
        return None
    
    def view_all_series(self):
        """Display all series in the list"""
        if not self.series_list:
            print("\n📭 Your series list is empty! Add a series to get started.")
            return
        
        print("\n" + "="*60)
        print("YOUR SERIES COLLECTION")
        print("="*60)
        
        for i, series in enumerate(self.series_list, 1):
            print(f"\n{i}. {series.name}")
            series.display_info()
        
        print("\n" + "="*60)
        print(f"Total series: {len(self.series_list)}")
        print("="*60)
    
    def update_episodes(self, name, episodes_watched):
        """
        Update the episodes watched for a series
        
        Args:
            name (str): The name of the series
            episodes_watched (int): Number of episodes watched
        """
        series = self.find_series(name)
        
        if not series:
            print(f"❌ Series '{name}' not found!")
            return False
        
        if series.update_episodes_watched(episodes_watched):
            print(f"✅ Updated '{name}': {episodes_watched}/{series.total_episodes} episodes watched")
            self._save()
            return True
        
        return False
    
    def delete_series(self, name):
        """
        Delete a series from the manager
        
        Args:
            name (str): The name of the series to delete
        """
        series = self.find_series(name)
        
        if not series:
            print(f"❌ Series '{name}' not found!")
            return False
        
        self.series_list.remove(series)
        print(f"✅ '{name}' has been deleted from your list.")
        self._save()
        return True
    
    def search_series(self, name):
        """
        Search for a series by name
        
        Args:
            name (str): The name (or partial name) to search for
        """
        results = []
        search_term = name.lower()
        
        for series in self.series_list:
            if search_term in series.name.lower():
                results.append(series)
        
        if not results:
            print(f"\n❌ No series found matching '{name}'")
            return
        
        print(f"\n🔍 Found {len(results)} series matching '{name}':")
        for series in results:
            series.display_info()
    
    def get_statistics(self):
        """Get statistics about the series collection"""
        if not self.series_list:
            return None
        
        total_series = len(self.series_list)
        completed = sum(1 for s in self.series_list if s.is_completed())
        total_episodes = sum(s.total_episodes for s in self.series_list)
        watched_episodes = sum(s.episodes_watched for s in self.series_list)
        
        return {
            'total_series': total_series,
            'completed_series': completed,
            'total_episodes': total_episodes,
            'watched_episodes': watched_episodes,
            'overall_progress': (watched_episodes / total_episodes * 100) if total_episodes > 0 else 0
        }
    
    def _save(self):
        """Save data to JSON file if storage is configured"""
        if self.storage:
            self.storage.save_series(self.series_list)
    
    def load_from_storage(self):
        """Load data from JSON file"""
        if self.storage:
            self.series_list = self.storage.load_series()

