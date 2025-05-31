# how to run: pytest unit_test.py -v

import unittest
from unittest.mock import patch, MagicMock
from grpc_interceptor.exceptions import NotFound

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from python.repository.User.user_repository import UserRepository_Service
from python.repository.User.UserRepository_pb2 import (
    get_user_Response,
    get_all_users_Response,
    get_users_that_watched_anime_Response,
    get_achievement_Response,
    get_user_achievements_Response,
    update_user_achievement_Response,
    update_user_karma_Response
)

class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.service = UserRepository_Service()
        self.context = MagicMock()

    @patch("user_repository.client.query")
    def test_get_user_success(self, mock_query):
        mock_query.side_effect = [
            MagicMock(result=MagicMock(return_value=[{"Username": "JohnDoe", "Location": "USA"}])),
            MagicMock(result=MagicMock(return_value=[{"karma": 150}])),
            MagicMock(result=MagicMock(return_value=[{
                "title": "Anime Enthusiast",
                "description": "Watched 100+ anime series",
                "date": "2025-03-26",
                "rarity": "EPIC"
            }])),
            MagicMock(result=MagicMock(return_value=[{"Anime Title": "Naruto", "rating": 9}]))
        ]

        request = MagicMock(user_name="JohnDoe")
        response = self.service.GetUser(request, self.context)

        self.assertIsInstance(response, get_user_Response)
        self.assertEqual(response.user.user_name, "JohnDoe")
        self.assertEqual(response.user.karma, 150)
        self.assertEqual(len(response.user.animes_watched), 1)

    @patch("user_repository.client.query")
    def test_get_user_not_found(self, mock_query):
        mock_query.return_value.result.return_value = []

        request = MagicMock(user_name="NotAUser")
        with self.assertRaises(NotFound):
            self.service.GetUser(request, self.context)

    @patch("user_repository.client.query")
    def test_get_all_users(self, mock_query):
        mock_query.side_effect = [
            MagicMock(result=MagicMock(return_value=[{"Username": "JohnDoe"}])),  # GetAll
            MagicMock(result=MagicMock(return_value=[{"Username": "JohnDoe", "Location": "USA"}])),
            MagicMock(result=MagicMock(return_value=[{"karma": 100}])),
            MagicMock(result=MagicMock(return_value=[])),
            MagicMock(result=MagicMock(return_value=[])),
        ]

        request = MagicMock()
        response = self.service.GetAllUsers(request, self.context)

        self.assertIsInstance(response, get_all_users_Response)
        self.assertEqual(len(response.users), 1)
        self.assertEqual(response.users[0].user_name, "JohnDoe")

    @patch("user_repository.client.query")
    def test_get_users_that_watched_anime(self, mock_query):
        mock_query.side_effect = [
            MagicMock(result=MagicMock(return_value=[{"Username": "JohnDoe"}])),
            MagicMock(result=MagicMock(return_value=[{"Username": "JohnDoe", "Location": "USA"}])),
            MagicMock(result=MagicMock(return_value=[{"karma": 100}])),
            MagicMock(result=MagicMock(return_value=[])),
            MagicMock(result=MagicMock(return_value=[])),
        ]

        request = MagicMock(anime_names=["Naruto"])
        response = self.service.GetUsersThatWatchedAnime(request, self.context)

        self.assertIsInstance(response, get_users_that_watched_anime_Response)
        self.assertEqual(len(response.users), 1)
        self.assertEqual(response.users[0].user_name, "JohnDoe")

    @patch("user_repository.client.query")
    def test_get_achievement_found(self, mock_query):
        mock_query.return_value.result.return_value = [{
            "title": "Anime Enthusiast",
            "description": "Watched 100+ anime series",
            "date": "2025-03-26",
            "rarity": "EPIC"
        }]

        request = MagicMock(title="Anime Enthusiast")
        response = self.service.GetAchievement(request, self.context)

        self.assertIsInstance(response, get_achievement_Response)
        self.assertEqual(response.achievement.title, "Anime Enthusiast")

    @patch("user_repository.client.query")
    def test_get_achievement_not_found(self, mock_query):
        mock_query.return_value.result.return_value = []

        request = MagicMock(title="NotRealAchievement")
        with self.assertRaises(NotFound):
            self.service.GetAchievement(request, self.context)

    @patch("user_repository.client.query")
    def test_get_user_achievements(self, mock_query):
        mock_query.return_value.result.return_value = [
            {
                "title": "Anime Enthusiast",
                "description": "Watched 100+ anime series",
                "date": "2025-03-26",
                "rarity": "EPIC"
            }
        ]

        request = MagicMock(user_name="JohnDoe")
        response = self.service.GetUserAchievements(request, self.context)

        self.assertIsInstance(response, get_user_achievements_Response)
        self.assertEqual(len(response.achievements), 1)
        self.assertEqual(response.achievements[0].title, "Anime Enthusiast")

    @patch("user_repository.client.query")
    def test_update_user_achievement_success(self, mock_query):
        mock_query.return_value.result.return_value = []
        request = MagicMock(user_name="JohnDoe", title="Anime Enthusiast")
        response = self.service.UpdateUserAchievement(request, self.context)

        self.assertIsInstance(response, update_user_achievement_Response)
        self.assertTrue(response.success)

    @patch("user_repository.client.query")
    def test_update_user_achievement_not_found(self, mock_query):
        request = MagicMock(user_name="JohnDoe", title="InvalidTitle")
        with self.assertRaises(NotFound):
            self.service.UpdateUserAchievement(request, self.context)

    @patch("user_repository.client.query")
    def test_update_user_karma_success(self, mock_query):
        mock_query.return_value.result.return_value = []
        request = MagicMock(user_name="JohnDoe", karma_value=10)
        response = self.service.UpdateUserKarma(request, self.context)

        self.assertIsInstance(response, update_user_karma_Response)
        self.assertTrue(response.success)