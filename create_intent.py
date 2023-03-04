import os
import json

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print(f"Intent created: {response}")

def main():
    load_dotenv()
    project_id = os.getenv('PROJECT_ID')

    with open("phrases.json", "r") as file:
        phrases_json = file.read()
    training_phrases = json.loads(phrases_json)
    
    display_name = "Устройство на работу"
    training_phrases_parts = training_phrases[display_name]["questions"]
    message_texts = training_phrases[display_name]["answer"]
    print(training_phrases_parts)
    print(message_texts)

    create_intent(project_id, display_name, training_phrases_parts, message_texts)


if __name__ == "__main__":
    main()
