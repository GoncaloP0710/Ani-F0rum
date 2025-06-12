import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import connexion
import pathlib

basedir = pathlib.Path(__file__).parent.resolve()

print("===================== Entry point ====================")
print("base dir: " + str(basedir))
print("=========================================================")

connex_app = connexion.App(__name__, specification_dir=basedir)
connex_app.add_api(basedir / "swagger.yml")

import grpc
from python.Common import User_pb2 as Common_dot_User__pb2
from python.controller.Anime import anime_controller

import requests
#
def root():
    return {"status": "ok"}, 200

def all_anime():
    try:
        # Make a GET request to the /anime endpoint
        response = requests.get(f"http://anime-controller:50051/anime")

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

def get_anime(anime_name):
    try:
        # Make a GET request to the /anime/{name} endpoint
        response = requests.get(f"http://anime-controller:50051/anime/anime_name/{anime_name}")

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

def get_similar_anime(anime_name):
    try:
        # Make a GET request to the /anime/similar/{name} endpoint
        response = requests.get(f"http://anime-controller:50051/anime/anime_name/{anime_name}/related")

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

def get_similar_anime_list(user_name):
    try:
        # Make a GET request to the /anime/recomended/{name} endpoint
        response = requests.get(f"http://anime-controller:50051/anime/user/recomended/{user_name}")

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            return response.json()  # Return the list of recommended animes as JSON
        elif response.status_code == 404:
            print(f"User '{user_name}' not found.")
            return None
        else:
            print(f"Failed to fetch recommended animes for '{user_name}'. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_related_by_anime(user_name):
    try:
        response = requests.get(f"http://user-controller:50040/user/{user_name}/related_by_anime")

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            return response.json()  # Return the list of recommended animes as JSON
        elif response.status_code == 404:
            print(f"User '{user_name}' not found.")
            return None
        else:
            print(f"Failed to fetch recommended animes for '{user_name}'. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_user(user_name):
    try:
        response = requests.get(f"http://user-controller:50040/user/{user_name}")

        if response.status_code == 200:
            return response.json()
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


def all_users():
    logging.info("Fetching all users")
    try:
        response = requests.get(f"http://user-controller:50040/user")

        logging.info(f"Response: {response.text}")

        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Failed to fetch users. Status code: {response.status_code}")
            logging.error(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None

def get_karma(user_name):
    try:
        response = requests.get(f"http://user-controller:50040/user/{user_name}/karma")

        if response.status_code == 200:
            return response.json()
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

def update_user_karma(user_name, karma_value):
    try:
        response = requests.get(f"http://user-controller:50040/user/{user_name}/karma/{karma_value}")

        if response.status_code == 200:
            return response.json()
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

def GetAchievement(title):
    try:
        response = requests.get(f"http://user-controller:50040/user/achievement/{title}")

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Achievement '{title}' not found.")
            return None
        else:
            print(f"Failed to fetch achievement '{title}'. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def GetAchivementList(user_name):
    try:
        response = requests.get(f"http://user-controller:50040/user/{user_name}/achievements")

        if response.status_code == 200:
            return response.json()
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

def UpdateAchievement(user_name, title):
    try:
        response = requests.get(f"http://user-controller:50040/user/{user_name}/achievement/{title}")

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"User '{user_name}' not found.")
            return None
        else:
            print(f"Failed to fetch achievement '{title}' for user '{user_name}'. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def all_topics():

    try:
        # Make a GET request to the /topics endpoint
        response = requests.get(f"http://topics-controller:50060/topics")

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            return response.json()  # Return the list of topics as JSON
        else:
            print(f"Failed to fetch topics. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def create_topic(topic_name):

    try:
        # Make a GET request to the /topics/{topic_name}/create endpoint
        response = requests.get(f"http://topics-controller:50060/topics/{topic_name}/create")

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            return response.json()  # Return the created topic name
        else:
            print(f"Failed to create a topic. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_topic(topic_name):

    try:
        # Make a GET request to the /topics/{topic_name} endpoint
        response = requests.get(f"http://topics-controller:50060/topics/{topic_name}")

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            return response.json()  # Return the list of topics as JSON
        else:
            print(f"Failed to fetch a topic. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def publish(topic_name, body):
    try:
        # Make a POST request to the /topics/{topic_name} endpoint
        response = requests.post(
            url=f"http://topics-controller:50060/topics/{topic_name}",
            json=body
        )

        # Check if the response status code is 200 (OK)
        if response.status_code > 200 and response.status_code < 300:
            return response.json()  # Return the created topic name
        else:
            print(f"Failed to create a topic. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def healthz():
    return {"status": "ok"}, 200

def readiness():
    return {"status": "ready"}, 200

def startup():
    return {"status": "started"}, 200

if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=80)


