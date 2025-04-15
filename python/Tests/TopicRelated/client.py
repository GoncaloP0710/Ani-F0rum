import requests

class TopicClient:
    def __init__(self, base_url="http://topics-controller:50060/"):
        self.base_url = base_url

    def get_topics(self):
        try:
            # Make a GET request to the /topics endpoint
            response = requests.get(f"{self.base_url}/topics")
            
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                return response.json()  # Return the list of animes as JSON
            else:
                print(f"Failed to fetch topics. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def create_topic(self):
        try:
            topic_name = input('Qual o nome do tópico?\n')

            print('make a create topic request to the controller')
            # Make a POST request to the /topics endpoint
            response = requests.post(f"{self.base_url}/topics", json={
                "name": topic_name
            })

            print('Got the response:')
            print(response)

            # Check if the response status code is 200 (OK)
            if response.status_code >= 200 or response.status_code < 300:
                return response.json()  # Return the anime details as JSON
            
            # TODO adicionar caso de erro de criação (e.g. já existe)
            #elif response.status_code == 400:
            #    print(f"Topic '{topic_name}' not found.")
            #    return None
            else:
                print(f"Failed to create '{topic_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_topic(self):
        try:
            topic_name = input('Qual o nome do tópico?')

            # Make a GET request to the /topics/{topicname} endpoint
            response = requests.get(f"{self.base_url}/topics/{topic_name}")
            
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                return response.json()  # Return the anime details as JSON
            elif response.status_code == 400:
                print(f"Topic '{topic_name}' not found.")
                return None
            else:
                print(f"Failed to fetch '{topic_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def publish(self):
        try:
            topic_name = input('Qual o nome do tópico?\n')
            publication_name = input('Qual o nome da publicação?\n')
            username = input('Qual o seu nome de usuário?\n')
            content_type = input('Qual o tipo de conteúdo? (e.g. imagem ou mensagem)\n')
            content = input('Qual o conteúdo da publicação? (e.g. nome da imagem ou conteúdo da mensagem)\n')

            response = None

            # Make a POST request to the /topics/{topicname} endpoint
            if content_type == 'imagem' or content_type == 'image':
                response = requests.post(f"{self.base_url}/topics/{topic_name}", json={
                    "name": publication_name,
                    "topic_name": topic_name,
                    "images": [{
                        "username": username,
                        "name": content
                    }]
                })
            else:
                response = requests.post(f"{self.base_url}/topics/{topic_name}", json={
                    "name": publication_name,
                    "topic_name": topic_name,
                    "message": {
                        "username": username,
                        "content": content
                    }
                })
            
            # Check if the response status code is 200 (OK)
            if response.status_code >= 200 and response.status_code < 300:
                print('Got the response:')
                return response.json()  # Return the anime details as JSON
            # TODO adicionar caso de erro de criação (e.g. já existe com este nome)
            #elif response.status_code == 400:
            #    print(f"Topic '{topic_name}' not found.")
            #    return None
            else:
                print(f"Failed to publish '{publication_name}'. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

# Example usage
if __name__ == "__main__":
    client = TopicClient()

    # ============================== Get all topics ==============================
    topics = client.get_topics()
    if topics:
        print("List of Topics:")
        for topic in topics:
            print(topic)

    # ============================== Get a topic ==============================
    topic = client.get_topic()
    if topic:
        print('Topic: ')
        print(topic)

    # From here it doesn't work due to the error identified in "/python/controller/Topics/topics.py"
    # ============================== Post a new topic ==============================
    response = client.create_topic()
    if response:
        print(f"\nCreated topic : '{response}'")
        print(response)
    
    # ============================== Post a publication ==============================
    response = client.publish()
    if response:
        print(f"\nPublished : '{response}'")