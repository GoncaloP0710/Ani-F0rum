# how to run: python -m unittest unit_test.py

import unittest
from unittest.mock import MagicMock, patch
import grpc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from python.others.UserStatistics.UserStatistics import UserStatistics
from python.Common.Anime_pb2 import Anime
from python.Common.Topic_pb2 import Topic, Message, Publication
from python.Common.User_pb2 import User

class TestUserStatistics(unittest.TestCase):

    def setUp(self):
        self.service = UserStatistics()

        self.service.user_stub = MagicMock()
        self.service.anime_stub = MagicMock()
        self.service.topic_stub = MagicMock()
        self.context = MagicMock()

    def test_get_top10_success(self):
        user = User(user_name="test_user", animes_watched=["Naruto", "One Piece"], anime_watched_score=[9, 8])
        self.service.user_stub.GetUser.return_value = MagicMock(user=user)

        animes = [Anime(name="Naruto"), Anime(name="One Piece")]
        self.service.anime_stub.MultipleAnimeByName.return_value = MagicMock(animes=animes)

        request = MagicMock(user_name="test_user")

        response = self.service.GetTop10(request, self.context)

        self.assertEqual(response.animes, animes)

    def test_get_most_used_topics_success(self):
        pub1 = Publication(message=Message(username="test_user"))
        pub2 = Publication(images=Publication.Image(username="test_user"))

        topic1 = Topic(topicname="topic1", publications=[pub1, pub2])
        topic2 = Topic(topicname="topic2", publications=[pub1])

        user = User(user_name="test_user", topics_subscribed=["topic1", "topic2"])
        self.service.user_stub.GetUser.return_value = MagicMock(user=user)
        self.service.topic_stub.GetTopic.side_effect = [
            MagicMock(topic=topic1),
            MagicMock(topic=topic2)
        ]

        request = MagicMock(user_name="test_user")

        response = self.service.GetMostUsedTopics(request, self.context)

        self.assertEqual(len(response.most_used_topics), 2)
        self.assertEqual(response.most_used_topics[0].topicname, "topic1")

    def test_get_user_karma_success(self):
        user = User(user_name="test_user", karma=42)
        self.service.user_stub.GetUser.return_value = MagicMock(user=user)

        request = MagicMock(user_name="test_user")
        response = self.service.GetUserKarma(request, self.context)

        self.assertEqual(response.karma_Value, 42)

    def test_update_user_karma_success(self):
        self.service.user_stub.UpdateUserKarma.return_value = MagicMock(success=True)

        request = MagicMock(user_name="test_user", karma_value=99)
        response = self.service.UpdateUserKarma(request, self.context)

        self.assertTrue(response.success)

    def test_get_all_users_success(self):
        users = [User(user_name="user1"), User(user_name="user2")]
        self.service.user_stub.GetAllUsers.return_value = MagicMock(users=users)

        request = MagicMock()
        response = self.service.GetAllUsers(request, self.context)

        self.assertEqual(len(response.users), 2)

    def test_get_user_by_name_success(self):
        user = User(user_name="user1")
        self.service.user_stub.GetUser.return_value = MagicMock(user=user)

        request = MagicMock(user_name="user1")
        response = self.service.GetUserByName(request, self.context)

        self.assertEqual(response.user.user_name, "user1")

if __name__ == "__main__":
    unittest.main()