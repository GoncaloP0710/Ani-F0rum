# how to run: python -m unittest discover tests

import pytest
from unittest import mock
from unittest.mock import MagicMock

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from python.repository.Topic.TopicRepository_pb2 import (
    GetTopicsResponse,
    CreateTopicResponse,
    GetTopicResponse,
)

from python.repository.Topic.topic import TopicService


@pytest.fixture
def topic_service():
    return TopicService()


@mock.patch("your_module_path.client.query")
def test_create_topic_success(mock_query, topic_service):
    mock_query.return_value.result.return_value = []

    request = MagicMock()
    request.topicname = "TestTopic"
    context = MagicMock()

    response = topic_service.CreateTopic(request, context)

    assert isinstance(response, CreateTopicResponse)
    assert response.topicname == "TestTopic"
    mock_query.assert_called_once()


@mock.patch("your_module_path.client.query")
def test_get_topics_empty(mock_query, topic_service):
    mock_query.return_value.result.return_value = []

    request = MagicMock()
    context = MagicMock()

    response = topic_service.GetTopics(request, context)

    assert isinstance(response, GetTopicsResponse)
    assert len(response.topics) == 0


@mock.patch("your_module_path.client.query")
def test_get_topic_single(mock_query, topic_service):
    def query_side_effect(query, job_config=None):
        class Result:
            def result(self):
                if "FROM `cn-fc58192.vmcloud.topics` t" in query and "WHERE t.topicname" in query:
                    return [{'topicname': 'TestTopic'}]
                elif "subscribers" in query:
                    return [{'topic_name': 'TestTopic', 'subscriber_name': 'User1'}]
                elif "messages" in query:
                    return [{
                        'topic_name': 'TestTopic',
                        'publication_name': 'Pub1',
                        'publication_topicname': 'TestTopic',
                        'message_username': 'User1',
                        'message_content': 'Hello'
                    }]
                elif "images" in query:
                    return [{
                        'topic_name': 'TestTopic',
                        'publication_name': 'Pub2',
                        'publication_topicname': 'TestTopic',
                        'image_name': 'img1.png',
                        'image_username': 'User2'
                    }]
                return []
        return Result()

    mock_query.side_effect = query_side_effect

    request = MagicMock()
    request.topicname = "TestTopic"
    context = MagicMock()

    response = topic_service.GetTopic(request, context)

    assert isinstance(response, GetTopicResponse)
    assert response.topic.topicname == "TestTopic"
    assert len(response.topic.subscribers) == 1
    assert len(response.topic.publications) == 2

# os restantes testes não foram incluídos pois na inserção, não retornam nada