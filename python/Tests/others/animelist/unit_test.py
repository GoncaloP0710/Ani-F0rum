# how to run: python -m unittest unit_test.py

import unittest
from unittest.mock import MagicMock, patch
import grpc

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from python.others.AnimeList.AnimeList_pb2 import (
    get_similar_anime_Request,
    get_anime_by_name_Response
)
from python.Common.Anime_pb2 import Anime, AnimeGenre
from python.repository.Anime import AnimeRepository_pb2

from python.others.AnimeList.anime_list import AnimeList_Service

class TestAnimeListService(unittest.TestCase):

    def setUp(self):
        self.service = AnimeList_Service()
        self.service.stub = MagicMock()

    def test_GetAllAnimes_success(self):
        mock_response = MagicMock()
        mock_response.animes = [Anime(name="Naruto"), Anime(name="One Piece")]
        self.service.stub.Animes.return_value = mock_response

        result = self.service.GetAllAnimes(None, MagicMock())
        self.assertEqual(len(result.animes), 2)
        self.assertEqual(result.animes[0].name, "Naruto")

    def test_GetAnimeByName_success(self):
        anime = Anime(
            name="Naruto",
            genres=[],
            episodes=220,
            score=8.5,
            aired="2002-2007",
            synopsis="A young ninja's journey."
        )

        mock_response = MagicMock()
        mock_response.anime = anime

        self.service.stub.AnimeByName.return_value = mock_response

        request = AnimeRepository_pb2.anime_by_name_Request(anime_name="Naruto")
        result = self.service.GetAnimeByName(request, MagicMock())

        self.assertEqual(result.anime.name, "Naruto")

    def test_GetMultipleAnimeByName_success(self):
        mock_response = MagicMock()
        mock_response.animes = [Anime(name="Naruto"), Anime(name="Bleach")]
        self.service.stub.MultipleAnimeByName.return_value = mock_response

        request = AnimeRepository_pb2.multiple_anime_by_name_Request(anime_names=["Naruto", "Bleach"])
        result = self.service.GetMultipleAnimeByName(request, MagicMock())
        self.assertEqual(len(result.animes), 2)

    def test_GetSimilarAnime_success(self):
        genres = [AnimeGenre.ACTION, AnimeGenre.DRAMA]
        anime = Anime(name="Naruto", genres=genres)
        self.service.stub.AnimeByName.return_value.anime = anime

        def fake_AnimeRelatedByGenre(req):
            return MagicMock(animes=[Anime(name="Bleach"), Anime(name="One Piece")])

        self.service.stub.AnimeRelatedByGenre.side_effect = fake_AnimeRelatedByGenre

        request = get_similar_anime_Request(anime_name="Naruto")
        result = self.service.GetSimilarAnime(request, MagicMock())
        self.assertGreaterEqual(len(result.animes), 1)
        self.assertTrue(all(isinstance(a, Anime) for a in result.animes))

    def test_get_combination_of_genres(self):
        genres = [AnimeGenre.ACTION, AnimeGenre.DRAMA, AnimeGenre.COMEDY]
        combinations = self.service.get_combination_of_genres(genres)
        self.assertIsInstance(combinations, list)
        self.assertTrue(all(isinstance(c, list) for c in combinations))


if __name__ == '__main__':
    unittest.main()