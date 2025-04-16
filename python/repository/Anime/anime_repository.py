import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from concurrent import futures
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from python.repository.Anime.AnimeRepository_pb2_grpc import (
    AnimeRepositoryServicer,
    add_AnimeRepositoryServicer_to_server,
)
from python.repository.Anime.AnimeRepository_pb2 import (
    animes_Response,
    anime_by_name_Response,
    multiple_anime_by_name_Response,
    anime_by_genre_Response,
)

from python.Common.Anime_pb2 import (
    Anime,
    AnimeGenre,
)

from flask import Flask, request, abort
from google.cloud import bigquery
import json, os
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler()  # Output logs to the console
    ]
)

client = bigquery.Client(project="cn-fc58192", location="europe-west1")

print("===================== Anime Repository ====================")
print("Trying to start AnimeRepository service...")
print("=========================================================")

class AnimeRepository_Service(AnimeRepositoryServicer) : 

    # TODO: Implement database connection and queries to retrieve anime data

    Animes_Objects = [
        Anime(
            name="Naruto",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.DRAMA],
            episodes=220,
            score=8.5,
            aired="2002-2007",
            synopsis="A young ninja strives to become the Hokage."
        ),
        Anime(
            name="One Piece",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.COMEDY],
            episodes=1000,
            score=9.0,
            aired="1999-present",
            synopsis="A young pirate strives to become the Pirate King."
        ),
        Anime(
            name="Dragon Ball",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.FANTASY],
            episodes=153,
            score=8.5,
            aired="1986-1989",
            synopsis="A young warrior strives to become the strongest fighter."
        ),
        Anime(
            name="Attack on Titan",
            genres=[AnimeGenre.ACTION, AnimeGenre.THRILLER, AnimeGenre.DRAMA],
            episodes=75,
            score=9.2,
            aired="2013-present",
            synopsis="Humanity fights for survival against giant humanoid Titans."
        ),
        Anime(
            name="Demon Slayer",
            genres=[AnimeGenre.ACTION, AnimeGenre.FANTASY, AnimeGenre.DRAMA],
            episodes=26,
            score=8.7,
            aired="2019",
            synopsis="A young boy becomes a demon slayer to avenge his family."
        ),
        Anime(
            name="My Hero Academia",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.COMEDY],
            episodes=113,
            score=8.6,
            aired="2016-present",
            synopsis="A boy born without superpowers in a world where they are common."
        ),
        Anime(
            name="Death Note",
            genres=[AnimeGenre.MYSTERY, AnimeGenre.THRILLER, AnimeGenre.DRAMA],
            episodes=37,
            score=9.0,
            aired="2006-2007",
            synopsis="A high school student discovers a supernatural notebook."
        ),
        Anime(
            name="Bleach",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.FANTASY],
            episodes=366,
            score=8.1,
            aired="2004-2012",
            synopsis="A teenager becomes a Soul Reaper to protect the living and the dead."
        ),
        Anime(
            name="Fullmetal Alchemist: Brotherhood",
            genres=[AnimeGenre.ACTION, AnimeGenre.ADVENTURE, AnimeGenre.FANTASY],
            episodes=64,
            score=9.1,
            aired="2009-2010",
            synopsis="Two brothers use alchemy in their quest to restore their bodies."
        )
    ]

    # Map genre strings to AnimeGenre enum values
    GENRE_MAPPING = {
        "Action": AnimeGenre.ACTION,
        "Adventure": AnimeGenre.ADVENTURE,
        "Comedy": AnimeGenre.COMEDY,
        "Drama": AnimeGenre.DRAMA,
        "Fantasy": AnimeGenre.FANTASY,
        "Horror": AnimeGenre.HORROR,
        "Mystery": AnimeGenre.MYSTERY,
        "Romance": AnimeGenre.ROMANCE,
        "Sci-Fi": AnimeGenre.SCI_FI,
        "Thriller": AnimeGenre.THRILLER,
    }

    def map_genres_to_enum(self, genre_list):
        mapped_genres = []
        for genre in genre_list:
            if genre.strip() in self.GENRE_MAPPING:
                mapped_genres.append(self.GENRE_MAPPING[genre.strip()])
            else:
                logging.warning(f"Unknown genre: {genre.strip()}")  # Log and skip unknown genres
        return mapped_genres

    # Returns all animes
    def Animes(self, request, context):
        logging.info("Fetching all animes from BigQuery")

        # Query to fetch anime data
        query = "SELECT * FROM `cn-fc58192.vmcloud.anime-filtered`"
        query_job = client.query(query)
        result = query_job.result()

        # Transform query result into Anime objects
        animes = []
        for row in result:
            try:
                # Map genres to AnimeGenre enum, ignoring unknown genres
                genres = self.map_genres_to_enum(row["Genres"].split(","))

                # Convert episodes to an integer
                try:
                    episodes = int(row["Episodes"])
                except ValueError:
                    logging.error(f"Invalid episodes value for anime '{row['Name']}': {row['Episodes']}")
                    continue  # Skip this anime if episodes cannot be converted

                # Create an Anime object
                anime = Anime(
                    name=row["Name"],
                    genres=genres,  # Use the mapped genres
                    episodes=episodes,  # Convert to int
                    score=row["Score"],
                    aired=row["Aired"],
                    synopsis=row.get("Synopsis", "No synopsis available")  # Default if synopsis is missing
                )
                animes.append(anime)
            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        logging.info(f"Fetched {len(animes)} animes from BigQuery")

        # Return the transformed Anime objects
        return animes_Response(animes=animes)
    
    # Returns an anime by name
    def AnimeByName(self, request, context):
        AnimeName = request.anime_name
        logging.info(f"Searching for anime by name: {AnimeName}")

        # Use parameterized query to prevent SQL injection and syntax errors
        query = """
            SELECT * FROM `cn-fc58192.vmcloud.anime-filtered`
            WHERE Name = @AnimeName
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("AnimeName", "STRING", AnimeName)
            ]
        )
        query_job = client.query(query, job_config=job_config)
        result = query_job.result()

        # Check if the result is empty
        rows = list(result)
        if not rows:
            logging.warning(f"No anime found with name: {AnimeName}")
            raise NotFound("Anime not found")

        # Map genres to AnimeGenre enum, ignoring unknown genres
        genres = self.map_genres_to_enum(rows[0]["Genres"].split(","))

        # Convert episodes to an integer
        try:
            episodes = int(rows[0]["Episodes"])
        except ValueError:
            logging.error(f"Invalid episodes value for anime '{AnimeName}': {rows[0]['Episodes']}")
            raise ValueError("Invalid episodes value")

        # Create an Anime object
        anime = Anime(
            name=rows[0]["Name"],
            genres=genres,  # Use the mapped genres
            episodes=episodes,  # Convert to int
            score=rows[0]["Score"],
            aired=rows[0]["Aired"],
            synopsis=rows[0].get("Synopsis", "No synopsis available")
        )

        return anime_by_name_Response(anime=anime)
    
    def MultipleAnimeByName(self, request, context):
        print("Searching for multiple animes by name")
        result = []
        for anime in self.Animes_Objects:
            if anime.name in request.anime_names:
                result.append(anime)  # Use a list instead of a set
        return multiple_anime_by_name_Response(animes=result)
    
    def AnimeRelatedByGenre(self, request, context):
        logging.info("Searching for animes by genre")

        # Convert the requested genres (enum values as integers) to their string representations
        try:
            requested_genres = [AnimeGenre.Name(genre) for genre in request.anime_genres]
        except KeyError as e:
            logging.error(f"Invalid genre value in request: {e}")
            raise ValueError("Invalid genre value in request")

        logging.info(f"Requested genres: {requested_genres}")

        # Build the query to fetch animes that match the requested genres
        query = """
            SELECT * FROM `cn-fc58192.vmcloud.anime-filtered`
            WHERE ARRAY_LENGTH(ARRAY(
                SELECT genre
                FROM UNNEST(SPLIT(Genres, ',')) AS genre
                WHERE genre IN UNNEST(@requested_genres)
            )) > 0
        """

        # Configure the query with parameters
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter("requested_genres", "STRING", requested_genres)
            ]
        )

        # Execute the query
        query_job = client.query(query, job_config=job_config)
        result = query_job.result()

        # Transform query result into Anime objects
        animes = []
        for row in result:
            try:
                # Map genres to AnimeGenre enum, ignoring unknown genres
                genres = self.map_genres_to_enum(row["Genres"].split(","))

                # Convert episodes to an integer
                try:
                    episodes = int(row["Episodes"])
                except ValueError:
                    logging.error(f"Invalid episodes value for anime '{row['Name']}': {row['Episodes']}")
                    continue  # Skip this anime if episodes cannot be converted

                # Create an Anime object
                anime = Anime(
                    name=row["Name"],
                    genres=genres,  # Use the mapped genres
                    episodes=episodes,  # Convert to int
                    score=row["Score"],
                    aired=row["Aired"],
                    synopsis=row.get("Synopsis", "No synopsis available")  # Default if synopsis is missing
                )
                animes.append(anime)
            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        logging.info(f"Fetched {len(animes)} animes matching the genres from BigQuery")

        # Return the transformed Anime objects
        return anime_by_genre_Response(animes=animes)

# ----------------------------------------------------------------
# HTTP server for Kubernetes probes
class ProbeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/healthz", "/readiness", "/startup"]:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def start_http_server():
    http_server = HTTPServer(('0.0.0.0', 8080), ProbeHandler)
    print("HTTP server for probes started on port 8080")
    http_server.serve_forever()
# ----------------------------------------------------------------
        
def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_AnimeRepositoryServicer_to_server(
        AnimeRepository_Service(), server
    )
    server.add_insecure_port('[::]:50053')
    server.start()
    print("AnimeRepository Server started on port 50053")

    # -------------------------------------------------
    # Start the HTTP server for probes in a separate thread
    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()

    server.wait_for_termination()
    # --------------------------------------------------

    server.wait_for_termination()

if __name__ == '__main__':
    serve()
