from plexapi.server import PlexServer
import json
import os

# Load configuration from config.json
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

PLEX_URL = config["plex_url"]
PLEX_TOKEN = config["plex_token"]

# Connect to Plex server
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# Get all movies and TV shows
movies_section = plex.library.section('My Movies')
tv_shows_section = plex.library.section('My TV Shows')

# Fetch all unique years in the library
years = set()

# Get all movie years
for movie in movies_section.all():
    if movie.originallyAvailableAt:
        years.add(movie.originallyAvailableAt.year)

# Get all TV show years
for show in tv_shows_section.all():
    if show.originallyAvailableAt:
        years.add(show.originallyAvailableAt.year)

# If no years are found, exit
if not years:
    print("No valid content years found.")
    exit()

# Determine the range of decades
min_year = min(years)
max_year = max(years)

# Generate decade ranges dynamically
decades = [
    {"name": f"{start_year}s", "years": range(start_year, start_year + 10)}
    for start_year in range(min_year - (min_year % 10), max_year + 10, 10)
]

# Process each decade
for decade in decades:
    try:
        combined_items = []

        # Search for unwatched movies and TV episodes year by year and combine results
        for year in decade['years']:
            # Unwatched movies
            unwatched_movies = movies_section.search(unwatched=True, year=year)
            # Unwatched TV episodes
            unwatched_tv_episodes = tv_shows_section.searchEpisodes(unwatched=True, year=year)

            # Add movies and TV episodes to the combined list
            combined_items += unwatched_movies + unwatched_tv_episodes

        # Print summary
        print(f"Found {len(combined_items)} unwatched items for {decade['name']}")

        # Only create/update a playlist if there are items
        if combined_items:
            combined_items.sort(key=lambda x: x.originallyAvailableAt or x.addedAt)
            combined_playlist_name = f"{decade['name']} Unwatched Combined"

            # Check if the combined playlist exists
            try:
                combined_playlist = plex.playlist(combined_playlist_name)
                print(f"Updating existing playlist '{combined_playlist_name}'")

                # Determine which items need to be added or removed
                current_items = combined_playlist.items()
                items_to_add = [item for item in combined_items if item not in current_items]
                items_to_remove = [item for item in current_items if item not in combined_items]

                # Update the playlist
                if items_to_add:
                    combined_playlist.addItems(items_to_add)
                    print(f"Added {len(items_to_add)} items to '{combined_playlist_name}'")

                if items_to_remove:
                    combined_playlist.removeItems(items_to_remove)
                    print(f"Removed {len(items_to_remove)} items from '{combined_playlist_name}'")

            except:
                # If the playlist doesn't exist, create a new one
                print(f"Creating new playlist '{combined_playlist_name}'")
                plex.createPlaylist(title=combined_playlist_name, items=combined_items)
                print(f"Created combined playlist '{combined_playlist_name}' with {len(combined_items)} items.")

    except Exception as e:
        print(f"Failed to combine playlists for {decade['name']}: {e}")
