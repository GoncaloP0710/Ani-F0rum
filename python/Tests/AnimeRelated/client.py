import requests

class AnimeClient:
    def __init__(self, base_url="http://localhost:50051/api"):
        self.base_url = base_url

    def get_all_animes(self):
        try:
            # Make a GET request to the /anime endpoint
            response = requests.get(f"{self.base_url}/anime")
            
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                return response.json()  # Return the list of animes as JSON
            else:
                print(f"Failed to fetch animes. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_anime_by_name(self, anime_name):
        try:
            # Make a GET request to the /anime/{name} endpoint
            response = requests.get(f"{self.base_url}/anime/anime_name/{anime_name}")
            
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                return response.json()  # Return the anime details as JSON
            elif response.status_code == 404:
                print(f"Anime '{anime_name}' not found.")
                return None
            else:
                print(f"Failed to fetch anime '{anime_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_similar_anime(self, anime_name):
        try:
            # Make a GET request to the /anime/similar/{name} endpoint
            response = requests.get(f"{self.base_url}/anime/anime_name/{anime_name}/related")
            
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                return response.json()  # Return the list of similar animes as JSON
            elif response.status_code == 404:
                print(f"Anime '{anime_name}' not found.")
                return None
            else:
                print(f"Failed to fetch similar animes for '{anime_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

# Example usage
if __name__ == "__main__":
    client = AnimeClient()

    # ============================== Get all animes ==============================
    animes = client.get_all_animes()
    if animes:
        print("List of Animes:")
        for anime in animes:
            print(anime)

    # ============================== Get anime by name ==============================
    anime_name = "Naruto"
    anime = client.get_anime_by_name(anime_name)
    if anime:
        print(f"\nDetails of Anime '{anime_name}':")
        print(anime)

    # ============================== Get similar anime ==============================
    similar_anime_name = "One Piece"
    similar_animes = client.get_similar_anime(similar_anime_name)
    if similar_animes:
        print(f"\nList of Animes similar to '{similar_anime_name}':")
        for anime in similar_animes:
            print(anime)