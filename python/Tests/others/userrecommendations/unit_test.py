# how to run: python -m unittest unit_test.py

import unittest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from python.others.UserRecommendations.UserRecommendations_pb2 import users_related_by_anime_Request
from python.Common.Anime_pb2 import Anime, AnimeGenre
from python.Common.User_pb2 import User

from python.others.UserRecommendations.user_recommendations import UserRecommendations_Service


class TestUserRecommendationsService(unittest.TestCase):

    def setUp(self):
        self.service = UserRecommendations_Service()
        self.service.stub = MagicMock()

    def test_get_users_related_by_anime(self):
        # Setup mock response from UserRepository
        self.service.stub.GetUsersThatWatchedAnime.side_effect = [
            MagicMock(users=[User(user_name="user1"), User(user_name="user2")]),
            MagicMock(users=[User(user_name="user2"), User(user_name="user3")])
        ]
        self.service.stub.GetUser.side_effect = [
            MagicMock(user=User(user_name="user2")),
            MagicMock(user=User(user_name="user1")),
            MagicMock(user=User(user_name="user3")),
        ]

        request = users_related_by_anime_Request(
            animes_watched=[
                Anime(name="Naruto"),
                Anime(name="One Piece"),
            ],
            animes_similar=[
                Anime(name="Bleach"),
                Anime(name="Dragon Ball"),
            ]
        )

        response = self.service.GetUsersRelatedByAnime(request, context=MagicMock())

        usernames = [user.user_name for user in response.users]
        self.assertIn("user1", usernames)
        self.assertIn("user2", usernames)
        self.assertIn("user3", usernames)
        self.assertEqual(len(usernames), 3)

if __name__ == '__main__':
    unittest.main()