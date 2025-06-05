# how to run: python -m unittest unit_test.py

import unittest
from unittest.mock import MagicMock
import grpc

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from python.Common.Topic_pb2 import Topic, Message, Image

from python.others.Publisher.Publisher_pb2 import (
    GetTopicsResponsePub,
    CreateTopicResponsePub,
    GetTopicResponsePub,
    PublishInTopicResponsePub,
    PublishInTopicRequestPub
)

from python.others.Publisher.publisher import PublishService


class TestPublishService(unittest.TestCase):
    def setUp(self):
        self.service = PublishService()
        self.service.stub = MagicMock()
        self.context = MagicMock()

    def test_GetTopics_success(self):
        topics = [Topic(topicname="anime"), Topic(topicname="games")]
        self.service.stub.GetTopics.return_value = MagicMock(topics=topics)

        response = self.service.GetTopics(None, self.context)

        self.assertIsInstance(response, GetTopicsResponsePub)
        self.assertEqual(len(response.topics), 2)
        self.assertEqual(response.topics[0].topicname, "anime")

    def test_CreateTopic_success(self):
        self.service.stub.CreateTopic.return_value = MagicMock(topicname="tech")

        mock_request = MagicMock(topicname="tech")
        response = self.service.CreateTopic(mock_request, self.context)

        self.assertIsInstance(response, CreateTopicResponsePub)
        self.assertEqual(response.topicname, "tech")

    def test_GetTopic_success(self):
        topic = Topic(topicname="science")
        self.service.stub.GetTopic.return_value = MagicMock(topic=topic)

        mock_request = MagicMock(topicname="science")
        response = self.service.GetTopic(mock_request, self.context)

        self.assertIsInstance(response, GetTopicResponsePub)
        self.assertEqual(response.topic.topicname, "science")

    def test_Publish_message_success(self):
        message = Message(username="user1", content="hello world")
        request = PublishInTopicRequestPub(
            topicname="tech",
            publicationname="pub1",
            message=message
        )

        self.service.stub.PublishMessage.return_value = MagicMock(publicationname="pub1")
        response = self.service.Publish(request, self.context)

        self.assertIsInstance(response, PublishInTopicResponsePub)
        self.assertEqual(response.publicationname, "pub1")
        self.service.stub.PublishMessage.assert_called_once()

    def test_Publish_invalid_content(self):
        request = PublishInTopicRequestPub(topicname="tech", publicationname="pub3")

        with self.assertRaises(TypeError):
            self.service.Publish(request, self.context)


if __name__ == '__main__':
    unittest.main()