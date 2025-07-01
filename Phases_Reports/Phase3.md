# Requisitios funcionais

## André Reis
### account achievements
### post related track records (ex: Github contribution graphs)
### general feed personalized by interests (ex: Twitter)
### interest topic analisys for users

## Daniel Nunes

### Create a list of the most used topics for the user
- Analyze user activity to determine the most frequently discussed topics.
- Generate a ranked list of topics based on usage metrics.

### "Karma" system per user like the "Reddit" application in which you receive points according to your contribution to the forum
- Assign points to users based on their contributions (posts)
- Display a user's total karma on their stats

### Search anime by genre
- Allow users to filter anime by specific genres.
- Retrieve a list of anime that matches the selected genre(s). 

### Recommendation of anime based on the user's topics of interest analisys
- Analyze user activity to identify topics of interest.
- Use the identified topics to recommend relevant anime.

## Diogo Almeida

### create topics that do not exist on the forum
- Add a new topic to the already existing topics
    - The system shall allow users to create a topic with a unique name.
    - The system shall prevent duplicate topic creation.
    - The system shall return an error if the topic name already exists.
- Get all the topics that exist
- Get a specific topic by its name
    - The system shall allow users to retrieve details of a specific topic using its name.
    - If the topic does not exist, the system shall return an appropriate error message.

### publish a message or image in a specific topic
- Add the publication to a specific topic
    - The system shall allow users to publish messages or images in a topic.
    - The system shall associate each publication with the corresponding topic.
- Subscribe a user to a topic
- Get all the subscribers from a specific topic

### send the image for keyword generation
- Discover Vision API features
- Use Vision API to generates keywords to a certain image

### search image by keyword
- Get image names by using a keyword

## Goncalo Pinto

### Link users based on their anime preferences. Using the data from the dataset
- Have a way to get the animes watched by a user.
- Have a way to get similar animes to the ones watched by the user.
- Get all the users that watched some of those animes.

### Link users based on their messages. Using "keywords" to do such thing
- Have a way to get the animes watched by a user.
- Have a way to get similar animes to the ones watched by the user.
- Get the feed of a user.
- Analyse all the messages on the user feed and return the most related users.

### Recomendation system for a specific anime. Based on a anime, the app will generate a list of other tv shows with the samme style.
- Get the genres of the anime.
- Produce multiple sub lists of those genres.
- Check all animes that have some of the genres in the lists generated.

### Notification system for different events of the application
- Create a observer for the logs repository.
- When a log related to the user apears, return a message to him.