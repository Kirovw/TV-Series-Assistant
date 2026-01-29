"""
AI Recommendations module for TV Series Assistant
Provides intelligent series recommendations based on watched series
"""

class AIRecommender:
    """AI-powered series recommender"""
    
    # Database of popular series by genre
    SERIES_DATABASE = {
        'Crime Drama': [
            ('Breaking Bad', 62, 'A chemistry teacher turned methamphetamine cook'),
            ('Better Call Saul', 61, 'The origin story of criminal lawyer Saul Goodman'),
            ('The Wire', 60, 'Baltimore\'s drug trade and criminal justice system'),
            ('Mindhunter', 19, 'FBI agents study criminal psychology'),
            ('Hannibal', 39, 'Psychological thriller about a cannibalistic psychiatrist'),
        ],
        'Drama': [
            ('Game of Thrones', 73, 'Fantasy epic with political intrigue'),
            ('The Crown', 50, 'British monarchy through decades'),
            ('Succession', 39, 'Family power struggle over a media empire'),
            ('The Last of Us', 9, 'Post-apocalyptic survival thriller'),
            ('Chernobyl', 5, 'The Chernobyl nuclear disaster'),
        ],
        'Sci-Fi': [
            ('Stranger Things', 42, 'Supernatural events in 1980s Indiana'),
            ('The Expanse', 62, 'Humanity\'s future in space'),
            ('Dark', 26, 'Time travel mystery in a German town'),
            ('Westworld', 34, 'AI consciousness in a robot theme park'),
            ('Altered Carbon', 10, 'Cyberpunk future with transferred consciousness'),
        ],
        'Comedy': [
            ('The Office', 201, 'Mockumentary about office workers'),
            ('Parks and Recreation', 125, 'Government workers in small-town Indiana'),
            ('Brooklyn Nine-Nine', 153, 'Police precinct comedy'),
            ('The Good Place', 50, 'Afterlife mystery comedy'),
            ('Schitt\'s Creek', 80, 'Wealthy family loses everything'),
        ],
        'Thriller': [
            ('True Detective', 24, 'Anthology crime thriller series'),
            ('Dexter', 96, 'Serial killer who works for police'),
            ('Peaky Blinders', 36, 'Post-WWI Birmingham gangsters'),
            ('The Sopranos', 86, 'New Jersey mob boss in therapy'),
            ('Killing Eve', 24, 'Cat-and-mouse between killer and investigator'),
        ],
        'Fantasy': [
            ('The Witcher', 8, 'Monster hunter in a fantasy world'),
            ('House of the Dragon', 10, 'Game of Thrones prequel'),
            ('Rings of Power', 8, 'Lord of the Rings prequel'),
            ('His Dark Materials', 16, 'Fantasy adventure with parallel worlds'),
            ('Arcane', 9, 'League of Legends adaptation'),
        ],
        'Adventure': [
            ('The Mandalorian', 16, 'Star Wars bounty hunter adventure'),
            ('Lupin', 10, 'French heist and adventure series'),
            ('Avatar: The Last Airbender', 61, 'Animated adventure in fantasy world'),
            ('Castlevania', 32, 'Gothic vampire adventure'),
            ('Vikings', 89, 'Norse mythology and exploration'),
        ],
    }
    
    def __init__(self, manager):
        """
        Initialize the recommender
        
        Args:
            manager (SeriesManager): The series manager instance
        """
        self.manager = manager
    
    def get_recommendations(self, count=3):
        """
        Get AI-powered series recommendations
        
        Args:
            count (int): Number of recommendations to return
            
        Returns:
            list: List of recommended (series_name, episodes, description) tuples
        """
        if not self.manager.series_list:
            return self._get_random_recommendations(count)
        
        # Analyze watched genres
        genres_watched = self._analyze_genres()
        
        # Get recommendations based on genres
        recommendations = self._recommend_by_genres(genres_watched, count)
        
        return recommendations
    
    def _analyze_genres(self):
        """
        Analyze genres of watched series
        
        Returns:
            dict: Genre frequency mapping
        """
        genre_count = {}
        
        for series in self.manager.series_list:
            genre = series.genre if series.genre != 'Unknown' else 'Drama'
            genre_count[genre] = genre_count.get(genre, 0) + 1
        
        # Sort by frequency
        return dict(sorted(genre_count.items(), key=lambda x: x[1], reverse=True))
    
    def _recommend_by_genres(self, genres_watched, count=3):
        """
        Recommend series based on watched genres
        
        Args:
            genres_watched (dict): Genres the user is watching
            count (int): Number of recommendations
            
        Returns:
            list: Recommended series
        """
        recommendations = []
        watched_names = {s.name.lower() for s in self.manager.series_list}
        
        # First, try primary genres
        for genre in genres_watched.keys():
            if genre in self.SERIES_DATABASE:
                for series in self.SERIES_DATABASE[genre]:
                    if series[0].lower() not in watched_names:
                        recommendations.append(series)
                        if len(recommendations) >= count:
                            return recommendations[:count]
        
        # If we need more, add from other genres
        for genre, series_list in self.SERIES_DATABASE.items():
            if genre not in genres_watched:
                for series in series_list:
                    if series[0].lower() not in watched_names:
                        recommendations.append(series)
                        if len(recommendations) >= count:
                            return recommendations[:count]
        
        return recommendations[:count]
    
    def _get_random_recommendations(self, count=3):
        """
        Get random recommendations for new users
        
        Args:
            count (int): Number of recommendations
            
        Returns:
            list: Random recommended series
        """
        import random
        
        all_series = []
        for series_list in self.SERIES_DATABASE.values():
            all_series.extend(series_list)
        
        return random.sample(all_series, min(count, len(all_series)))
    
    def display_recommendations(self, count=3):
        """Display recommendations in a formatted way"""
        recommendations = self.get_recommendations(count)
        
        if not recommendations:
            print("❌ No recommendations available at this time.")
            return
        
        print("\n" + "="*60)
        print("🤖 AI RECOMMENDATIONS FOR YOU")
        print("="*60)
        
        for i, (name, episodes, description) in enumerate(recommendations, 1):
            print(f"\n{i}. {name}")
            print(f"   📺 Episodes: {episodes}")
            print(f"   📝 {description}")
        
        print("\n" + "="*60)
    
    def get_series_info(self, series_name):
        """
        Get information about a series from the database
        
        Args:
            series_name (str): Name of the series
            
        Returns:
            tuple or None: (name, episodes, description) or None
        """
        series_lower = series_name.lower()
        
        for series_list in self.SERIES_DATABASE.values():
            for name, episodes, description in series_list:
                if name.lower() == series_lower:
                    return (name, episodes, description)
        
        return None
