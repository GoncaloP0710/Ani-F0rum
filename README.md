# Cloud Computing Project

# Authors

- André Reis - fc58192
- Daniel Nunes - fc58257
- Diogo Almeida - fc64854
- Gonçalo Pinto - fc58178

# Project overview

## Dataset

We will use the [MyAnimeList Dataset](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset) for this project. This dataset contains comprehensive information about various anime, including titles, genres, ratings, and more.

Each member of the group will work on different functionalities based on this dataset.

The dataset was created on 28/07/2023 and is composed by these next parts:
- anime-filtered.csv(9.72 MB)
- users-details-2023.csv(73.93 MB)
- users-score-2023.csv(1.16 GB)

## Business capabilities

- Create an anime forum with a built-in social network based on each user's topics of interest.
- Recommendation system for both single animes and the entire profile of a user.

## Use cases 

### André Reis

- account achievements.
- post related track records (ex: Github contribution graphs).
- general feed personalized by interests (ex: Twitter).
- interest topic analisys for users.
- Implement gRPC for efficient communication between microservices.

### Daniel Nunes

- Create a list of the most used topics for the user.
- "Karma" system per user like the "Reddit" application in which you receive points according to your contribution to the forum.
- Search anime by genre.
- Recommendation of anime based on the user's topics of interest analisys. 
- Implement authentication and authorization for secure access to the services.

### Diogo Almeida

- create topics that do not exist on the forum.
- publish a message or image in a specific topic.
- send the image for keyword generation.
- search image by keyword.
- dns lookup for the server.
- implement elasticity in the server microservice and label generation microservice.

### Goncalo Pinto

- link users based on their anime preferences. Using the data from the dataset.
- link users based on their messages. Using "keywords" to do such thing.
- recomendation system for a specific anime. Based on a anime, the app will generate a list of other tv shows with the samme style.
- notification system for different events of the application.
- Set up a message queue (e.g., RabitMQ or Kafka) for asynchronous processing.
