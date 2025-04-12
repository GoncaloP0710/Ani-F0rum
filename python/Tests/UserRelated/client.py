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
            response = requests.get(f"{self.base_url}/user/{user_name}/top10anime")
            
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
            response = requests.get(f"{self.base_url}/user/all")
            
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

    def get_user_achievements(self, user_name):
        try:
            response = requests.get(f"{self.base_url}/user/{user_name}/achievements")
            
            if response.status_code == 200:
                return response.json()  # Return the user achievements as JSON
            elif response.status_code == 404:
                print(f"User '{user_name}' not found.")
                return None
            else:
                print(f"Failed to fetch achievements for user '{user_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_achievement(self, achievement_name):
        try:
            response = requests.get(f"{self.base_url}/user/achievement/{achievement_name}")

            if response.status_code == 200:
                return response.json()  # Return the user achievements as JSON
            elif response.status_code == 404:
                print(f"Achievement '{achievement_name}' not found.")
                return None
            else:
                print(f"Failed to fetch achievement '{achievement_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_user_feed(self, user_name):
        try:
            response = requests.get(f"{self.base_url}/user/{user_name}/get_feed")
            
            if response.status_code == 200:
                return response.json()  # Return the user feed as JSON
            elif response.status_code == 404:
                print(f"User '{user_name}' not found.")
                return None
            else:
                print(f"Failed to fetch feed for user '{user_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_user_feed_topic(self, user_name):
        try:
            response = requests.get(f"{self.base_url}/user/{user_name}/get_topic_feed")
            
            if response.status_code == 200:
                return response.json()  # Return the user feed topic as JSON
            elif response.status_code == 404:
                print(f"User '{user_name}' not found.")
                return None
            else:
                print(f"Failed to fetch feed topic for user '{user_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

if __name__ == "__main__":
    client = UserStatisticsClient()

    while True:
        print("\nChoose an option:")
        print("1. Get user karma")
        print("2. Get most used topics")
        print("3. Get user by name")
        print("4. Get all users")
        print("5. Get top 10 animes")
        print("6. Get user achievements")
        print("7. Get user feed")
        print("8. Get user feed topic")
        print("9. Get users related by anime")
        print("10. Get user achievements")
        print("11. Get one achievement")
        print("69. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_name = input("Enter the user name: ")
            karma = client.get_user_karma(user_name)
            print(karma)
        elif choice == "2":
            user_name = input("Enter the user name: ")
            most_used_topics = client.get_most_used_topics(user_name)
            print(most_used_topics)
        elif choice == "3":
            user_name = input("Enter the user name: ")
            user = client.GetUserByName(user_name)
            print(user)
        elif choice == "4":
            user_list = client.GetAllUsers()
            print(user_list)
        elif choice == "5":
            user_name = input("Enter the user name: ")
            top10_animes = client.get_top10_animes(user_name)
            print(top10_animes)
        elif choice == "6":
            user_name = input("Enter the user name: ")
            user_achievements = client.get_user_achievements(user_name)
            print(user_achievements)
        elif choice == "7":
            user_name = input("Enter the user name: ")
            user_feed = client.get_user_feed(user_name)
            print(user_feed)
        elif choice == "8":
            user_name = input("Enter the user name: ")
            user_feed_topic = client.get_user_feed_topic(user_name)
            print(user_feed_topic)
        elif choice == "9":
            user_name = input("Enter the user name: ")
            user_list = client.users_related_by_anime(user_name) 
            print (user_list)
        elif choice == "10":
            user_name = input("Enter the user name: ")
            ach_list = client.get_user_achievements(user_name) 
            print (ach_list)
        elif choice == "11":
            title = input("Enter the achievement name: ")
            ach = client.get_achievement(title) 
            print (ach)
        elif choice == "69":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


