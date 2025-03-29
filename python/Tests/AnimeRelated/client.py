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

# Example usage
if __name__ == "__main__":
    client = AnimeClient()
    animes = client.get_all_animes()
    if animes:
        print("List of Animes:")
        for anime in animes:
            print(anime)