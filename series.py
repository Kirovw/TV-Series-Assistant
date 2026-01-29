"""
Series class - Represents a single TV series
"""

class Series:
    """A class to represent a TV series"""
    
    def __init__(self, name, total_episodes, genre="Unknown"):
        """
        Initialize a Series object
        
        Args:
            name (str): The name of the series
            total_episodes (int): Total number of episodes in the series
            genre (str): The genre of the series
        """
        self.name = name
        self.total_episodes = total_episodes
        self.genre = genre
        self.episodes_watched = 0
    
    def get_progress(self):
        """Get the progress of watching the series"""
        if self.total_episodes == 0:
            return 0
        return (self.episodes_watched / self.total_episodes) * 100
    
    def update_episodes_watched(self, episodes):
        """
        Update the number of episodes watched
        
        Args:
            episodes (int): The number of episodes watched
        """
        if episodes < 0:
            print("❌ Episodes cannot be negative!")
            return False
        
        if episodes > self.total_episodes:
            print(f"⚠️  Warning: You've watched more episodes than available!")
            self.episodes_watched = episodes
            return True
        
        self.episodes_watched = episodes
        return True
    
    def is_completed(self):
        """Check if the series is fully watched"""
        return self.episodes_watched >= self.total_episodes
    
    def display_info(self):
        """Display information about the series"""
        progress = self.get_progress()
        status = "✅ COMPLETED" if self.is_completed() else "⏳ IN PROGRESS"
        
        print(f"\n📺 {self.name}")
        print(f"   Genre: {self.genre}")
        print(f"   Episodes: {self.episodes_watched}/{self.total_episodes}")
        print(f"   Progress: {progress:.1f}% {status}")
        print(f"   Remaining: {max(0, self.total_episodes - self.episodes_watched)} episodes")
