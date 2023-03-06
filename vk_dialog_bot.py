import random
import os

from dotenv import load_dotenv
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialog_flow import detect_intent_texts


def send_message(event, vk_api):
    if detect_intent_texts(event.text) != '<is_fallback>':
        vk_api.messages.send(
            user_id=event.user_id,
            message=detect_intent_texts(event.text),
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_message(event, vk_api)


if __name__ == "__main__":
    main()
