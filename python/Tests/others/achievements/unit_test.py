# how to run: python -m unittest unit_test.py

import unittest
from unittest.mock import MagicMock, patch

from grpc import ServicerContext
from grpc_interceptor.exceptions import NotFound

import sys
import os
print(os.path.dirname(__file__))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from python.others.Achievements.Achievements_pb2 import (
    AchievementListResponse,
    AchievementResponse,
    UpdateResponse
)

from python.Common.User_pb2 import Achievement

from python.repository.User import UserRepository_pb2 as ur_pb2

from python.others.Achievements.achievements import achievements


# class FakeContext(ServicerContext):
#     def abort(self, code, details):
#         raise NotFound(details)


class TestAchievementsService(unittest.TestCase):

    def setUp(self):
        self.service = achievements()
        self.service.stub = MagicMock()
        self.context = MagicMock() #FakeContext()

    def test_GetAchievementList_success(self):
        mock_response = ur_pb2.get_user_achievements_Response(
            achievements=[Achievement(title="Wow")]
        )
        self.service.stub.GetUserAchievements.return_value = mock_response

        request = MagicMock()
        request.user_name = "Crystal"

        response = self.service.GetAchivementList(request, self.context)

        self.assertIsInstance(response, AchievementListResponse)
        self.assertEqual(len(response.achievements), 1)
        self.assertEqual(response.achievements[0].title, "Wow")

    def test_GetAchievement_success(self):
        mock_response = ur_pb2.get_achievement_Response(
            achievement=Achievement(title="Wow")
        )
        self.service.stub.GetAchievement.return_value = mock_response

        request = MagicMock()
        request.title = "Wow"

        response = self.service.GetAchievement(request, self.context)

        self.assertIsInstance(response, AchievementResponse)
        self.assertEqual(response.item.title, "Wow")

    def test_UpdateAchievement_success(self):
        mock_response = ur_pb2.update_user_achievement_Response(success=True)
        self.service.stub.UpdateUserAchievement.return_value = mock_response

        request = MagicMock()
        request.title = "Wow"
        request.user_name = "Crystal"

        response = self.service.UpdateAchievement(request, self.context)

        self.assertIsInstance(response, UpdateResponse)
        self.assertTrue(response.success)


if __name__ == "__main__":
    unittest.main()