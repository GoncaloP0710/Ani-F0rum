import requests

class UserStatisticsClient:
    def __init__(self, base_url="http://localhost:50040/api"):
        self.base_url = base_url

    def users_related_by_anime(self, user_name) :
        try:
            response = requests.get(f"{self.base_url}/user/{user_name}/related_by_anime")
            
            if response.status_code == 200:
                return response.json()  # Return the karma value as JSON
            elif response.status_code == 404:
                print(f"User '{user_name}' not found.")
                return None
            else:
                print(f"Failed to fetch user related list by animes watched for user '{user_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_user_karma(self, user_name):
        try:
            response = requests.get(f"{self.base_url}/user/{user_name}/karma")
            
            if response.status_code == 200:
                return response.json()  # Return the karma value as JSON
            elif response.status_code == 404:
                print(f"User '{user_name}' not found.")
                return None
            else:
                print(f"Failed to fetch karma for user '{user_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_most_used_topics(self, user_name):
        try:
            response = requests.get(f"{self.base_url}/user/{user_name}/most_used_topics")
            
            if response.status_code == 200:
                return response.json()  # Return the list of most used topics as JSON
            elif response.status_code == 404:
                print(f"User '{user_name}' not found.")
                return None
            else:
                print(f"Failed to fetch most used topics for user '{user_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_top10_animes(self, user_name):
        try:
            response = requests.get(f"{self.base_url}/user/{user_name}/recomended_animeList")
            
            if response.status_code == 200:
                return response.json()  # Return the top 10 animes as JSON
            elif response.status_code == 404:
                print(f"User '{user_name}' not found.")
                return None
            else:
                print(f"Failed to fetch top 10 animes for user '{user_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def GetAllUsers(self):
        try:
            response = requests.get(f"{self.base_url}/user")
            
            if response.status_code == 200:
                return response.json()  # Return the list of users as JSON
            else:
                print(f"Failed to fetch user list. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def GetUserByName(self, user_name):
        try:
            response = requests.get(f"{self.base_url}/user/{user_name}")
            
            if response.status_code == 200:
                return response.json()  # Return the user details as JSON
            elif response.status_code == 404:
                print(f"User '{user_name}' not found.")
                return None
            else:
                print(f"Failed to fetch user '{user_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

if __name__ == "__main__":
    client = UserStatisticsClient()

    # ============================= Related Users by Anime ============================

    user_name = "JohnDoe"
    user_list = client.users_related_by_anime(user_name) 
    print (user_list)

    # # ============================== Karma ============================
    # user_name = "JohnDoe"
    # karma = client.get_user_karma(user_name)
    # print (karma)

    # # ============================== Most Used Topics ============================
    # user_name = "JohnDoe"
    # most_used_topics = client.get_most_used_topics(user_name)
    # print (most_used_topics)

    


