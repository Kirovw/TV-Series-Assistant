"""
TV Series Assistant - A simple tool to track and manage your favorite TV series
"""

from series_manager import SeriesManager
from json_storage import JSONStorage
from ai_recommender import AIRecommender

def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("📺 TV SERIES ASSISTANT 📺")
    print("="*50)
    print("1. Add a new series")
    print("2. View all series")
    print("3. Update episode watched")
    print("4. Delete a series")
    print("5. Search for a series")
    print("6. View statistics")
    print("7. Get AI recommendations")
    print("8. Exit")
    print("="*50)

def main():
    """Main function to run the TV series assistant"""
    # Initialize storage and manager with auto-save
    storage = JSONStorage("series_data.json")
    manager = SeriesManager(storage=storage)
    # Initialize AI recommender
    ai = AIRecommender(manager)
    
    while True:
        display_menu()
        choice = input("Choose an option (1-8): ").strip()
        if choice == '1':
            add_series(manager)
        elif choice == '2':
            manager.view_all_series()
        elif choice == '3':
            update_series(manager)
        elif choice == '4':
            delete_series(manager)
        elif choice == '5':
            search_series(manager)
        elif choice == '6':
            view_statistics(manager)
        elif choice == '7':
            ai_recommendations(ai)
        elif choice == '8':
            view_statistics(manager)
        elif choice == '7':
            print("\n👋 Thanks for using TV Series Assistant! Goodbye!")
            print("💾 Your data has been saved automatically.")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def add_series(manager):
    """Add a new series to the manager"""
    print("\n--- Add New Series ---")
    name = input("Enter series name: ").strip()
    
    if not name:
        print("❌ Series name cannot be empty!")
        return
    
    total_episodes = input("Enter total episodes: ").strip()
    try:
        total_episodes = int(total_episodes)
        if total_episodes <= 0:
            print("❌ Total episodes must be positive!")
            return
    except ValueError:
        print("❌ Please enter a valid number!")
        return
    
    genre = input("Enter genre (optional): ").strip() or "Unknown"
    
    manager.add_series(name, total_episodes, genre)
    print(f"✅ '{name}' added successfully!")

def update_series(manager):
    """Update episodes watched for a series"""
    print("\n--- Update Episodes ---")
    name = input("Enter series name: ").strip()
    
    episodes_watched = input("Enter episodes watched: ").strip()
    try:
        episodes_watched = int(episodes_watched)
        if episodes_watched < 0:
            print("❌ Episodes watched cannot be negative!")
            return
    except ValueError:
        print("❌ Please enter a valid number!")
        return
    
    manager.update_episodes(name, episodes_watched)

def delete_series(manager):
    """Delete a series from the manager"""
    print("\n--- Delete Series ---")
    name = input("Enter series name to delete: ").strip()
    manager.delete_series(name)

def search_series(manager):
    """Search for a series"""
    print("\n--- Search Series ---")
    name = input("Enter series name to search: ").strip()
    manager.search_series(name)

def view_statistics(manager):
    """View collection statistics"""
    print("\n--- Statistics ---")
    stats = manager.get_statistics()
    
    if not stats:
        print("❌ No series in your collection yet!")
        return
    
    print(f"📊 COLLECTION STATISTICS")
    print(f"   Total Series: {stats['total_series']}")
    print(f"   Completed: {stats['completed_series']}")
    print(f"   In Progress: {stats['total_series'] - stats['completed_series']}")
    print(f"   Total Episodes: {stats['total_episodes']}")
    print(f"   Episodes Watched: {stats['watched_episodes']}")
    print(f"   Overall Progress: {stats['overall_progress']:.1f}%")

def ai_recommendations(ai):
    """Get AI-powered series recommendations"""
    print("\n--- AI Recommendations ---")
    print("🤖 Analyzing your watching habits...")
    count = input("How many recommendations would you like? (default: 3): ").strip()
    
    try:
        count = int(count) if count else 3
        if count <= 0:
            print("❌ Please enter a positive number!")
            return
    except ValueError:
        print("❌ Please enter a valid number!")
        return
    
    ai.display_recommendations(count)

if __name__ == "__main__":
    main()
