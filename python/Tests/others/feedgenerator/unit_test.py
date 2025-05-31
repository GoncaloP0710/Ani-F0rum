# how to run: python -m unittest unit_test.py

import unittest
from unittest.mock import MagicMock, patch
import grpc

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from python.others.FeedGenerator.FeedGenerator_pb2 import FeedResponse, TopicFeedResponse
from python.Common.User_pb2 import User
from python.Common.Topic_pb2 import Topic, Publication
from python.repository.User import UserRepository_pb2 as ur_pb2

from python.others.FeedGenerator.FeedGenerator import FeedGenerator


class TestFeedGenerator(unittest.TestCase):

    def setUp(self):
        self.feed_generator = FeedGenerator()
        self.feed_generator.user_stub = MagicMock()
        self.feed_generator.topic_stub = MagicMock()
        self.context = MagicMock()

    def test_GetFeed_success(self):
        user = User(user_name="john", topics_subscribed=["anime", "games"])
        publication1 = Publication(title="New Anime", content="Naruto Shippuden")
        publication2 = Publication(title="Game Release", content="Elden Ring")

        self.feed_generator.user_stub.GetUser.return_value = MagicMock(user=user)

        def fake_get_topic(req):
            if req.topicname == "anime":
                return MagicMock(topic=Topic(topicname="anime", publications=[publication1]))
            elif req.topicname == "games":
                return MagicMock(topic=Topic(topicname="games", publications=[publication2]))

        self.feed_generator.topic_stub.GetTopic.side_effect = fake_get_topic

        request = ur_pb2.get_user_Request(user_name="john")
        response = self.feed_generator.GetFeed(request, self.context)

        self.assertIsInstance(response, FeedResponse)
        self.assertEqual(len(response.feed), 2)
        self.assertEqual(response.feed[0].title, "New Anime")
        self.assertEqual(response.feed[1].title, "Game Release")

    def test_GetFeed_user_not_found(self):
        self.feed_generator.user_stub.GetUser.return_value = MagicMock(user=None)

        request = ur_pb2.get_user_Request(user_name="missing_user")
        with self.assertRaises(grpc.RpcError) as cm:
            self.feed_generator.GetFeed(request, self.context)

        self.assertTrue(self.context.abort.called)
        self.context.abort.assert_called_with(grpc.StatusCode.NOT_FOUND, "Topic not found")

    def test_GetTopicFeed_success(self):
        user = User(user_name="john", topics_subscribed=["anime", "tech"])
        topic1 = Topic(topicname="anime")
        topic2 = Topic(topicname="tech")

        self.feed_generator.user_stub.GetUser.return_value = MagicMock(user=user)

        def fake_get_topic(req):
            if req.topicname == "anime":
                return MagicMock(topic=topic1)
            elif req.topicname == "tech":
                return MagicMock(topic=topic2)

        self.feed_generator.topic_stub.GetTopic.side_effect = fake_get_topic

        request = ur_pb2.get_user_Request(user_name="john")
        response = self.feed_generator.GetTopicFeed(request, self.context)

        self.assertIsInstance(response, TopicFeedResponse)
        self.assertEqual(len(response.topic_feed), 2)
        self.assertEqual(response.topic_feed[0].topicname, "anime")
        self.assertEqual(response.topic_feed[1].topicname, "tech")

    def test_GetTopicFeed_topic_not_found(self):
        user = User(user_name="john", topics_subscribed=["missing_topic"])
        self.feed_generator.user_stub.GetUser.return_value = MagicMock(user=user)
        self.feed_generator.topic_stub.GetTopic.return_value = MagicMock(topic=None)

        request = ur_pb2.get_user_Request(user_name="john")
        with self.assertRaises(grpc.RpcError):
            self.feed_generator.GetTopicFeed(request, self.context)

        self.context.abort.assert_called_with(grpc.StatusCode.NOT_FOUND, "Topic not found")


if __name__ == '__main__':
    unittest.main()