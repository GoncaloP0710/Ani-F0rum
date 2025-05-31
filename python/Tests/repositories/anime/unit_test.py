# how to run: python -m unittest discover tests

import unittest
from unittest.mock import patch, MagicMock
from grpc_interceptor.exceptions import NotFound

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from python.repository.Anime.anime_repository import AnimeRepository_Service
from python.repository.Anime.AnimeRepository_pb2 import (
    anime_by_name_Request,
    multiple_anime_by_name_Response,
    anime_by_genre_Response,
)
from python.Common.Anime_pb2 import AnimeGenre

class TestAnimeRepositoryService(unittest.TestCase):

    def setUp(self):
        self.service = AnimeRepository_Service()
        self.context = MagicMock()

    @patch("python.repository.Anime.AnimeRepository.client.query")
    def test_anime_by_name_found(self, mock_query):
        mock_query.return_value.result.return_value = [{
            "Name": "Naruto",
            "Genres": "Action,Adventure,Drama",
            "Episodes": "220",
            "Score": 8.5,
            "Aired": "2002-2007",
            "Synopsis": "A ninja story"
        }]

        req = anime_by_name_Request(anime_name="Naruto")
        res = self.service.AnimeByName(req, self.context)

        self.assertEqual(res.anime.name, "Naruto")
        self.assertEqual(res.anime.episodes, 220)
        self.assertEqual(len(res.anime.genres), 3)

    @patch("python.repository.Anime.AnimeRepository.client.query")
    def test_anime_by_name_not_found(self, mock_query):
        mock_query.return_value.result.return_value = []
        req = anime_by_name_Request(anime_name="Inexistente")
        with self.assertRaises(NotFound):
            self.service.AnimeByName(req, self.context)

    @patch("python.repository.Anime.AnimeRepository.client.query")
    def test_animes_success(self, mock_query):
        mock_query.return_value.result.return_value = [
            {
                "Name": "Naruto",
                "Genres": "Action,Adventure",
                "Episodes": "220",
                "Score": 8.5,
                "Aired": "2002-2007",
                "Synopsis": "Shinobi story"
            },
            {
                "Name": "Death Note",
                "Genres": "Mystery,Thriller,Drama",
                "Episodes": "37",
                "Score": 9.0,
                "Aired": "2006-2007",
                "Synopsis": "Notebook story"
            }
        ]

        res = self.service.Animes(None, self.context)
        self.assertEqual(len(res.animes), 2)
        self.assertEqual(res.animes[0].name, "Naruto")
        self.assertEqual(res.animes[1].name, "Death Note")

    @patch("python.repository.Anime.AnimeRepository.client.query")
    def test_multiple_anime_by_name(self, mock_query):
        def side_effect(query, job_config=None):
            name = job_config.query_parameters[0].value
            if name == "Naruto":
                mock = MagicMock()
                mock.result.return_value = [{
                    "Name": "Naruto",
                    "Genres": "Action,Adventure",
                    "Episodes": "220",
                    "Score": 8.5,
                    "Aired": "2002-2007",
                    "Synopsis": "Shinobi story"
                }]
                return mock
            else:
                mock = MagicMock()
                mock.result.return_value = []
                return mock

        mock_query.side_effect = side_effect

        request = MagicMock()
        request.anime_names = ["Naruto", "Inexistente"]

        res: multiple_anime_by_name_Response = self.service.MultipleAnimeByName(request, self.context)
        self.assertEqual(len(res.animes), 1)
        self.assertEqual(res.animes[0].name, "Naruto")

    @patch("python.repository.Anime.AnimeRepository.client.query")
    def test_anime_related_by_genre(self, mock_query):
        mock_query.return_value.result.return_value = [
            {
                "Name": "One Piece",
                "Genres": "Action,Adventure,Comedy",
                "Episodes": "1000",
                "Score": 9.0,
                "Aired": "1999-present",
                "Synopsis": "Pirate story"
            }
        ]

        request = MagicMock()
        request.anime_genres = [AnimeGenre.ACTION, AnimeGenre.ADVENTURE]

        res: anime_by_genre_Response = self.service.AnimeRelatedByGenre(request, self.context)
        self.assertEqual(len(res.animes), 1)
        self.assertEqual(res.animes[0].name, "One Piece")