import io
from datetime import datetime

import cv2
import numpy as np
import requests
import vk_api
from PIL import Image
from vk_api.longpoll import VkLongPoll, VkEventType

from face_finder.finder import find_face


class VkEventHandler:
    def __init__(self, vk_session, vk_session_group):
        self.vk_session = vk_session
        self.vk_session_group = vk_session_group
        self.vk_session_group_api = vk_session_group.get_api()
        self.vk_session_api = self.vk_session.get_api()

    def __call__(self, num_friend=100):
        self.num_friend = num_friend
        longpoll = VkLongPoll(self.vk_session_group)
        for event in longpoll.listen():
            self.react(event)

    def react(self, event):
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            self.vk_session_group_api.messages.send(
                user_id=event.user_id,
                random_id=self.get_random_id(),
                message="Отправь фото, и я постараюсь найти твоих друзей которые изображены на фото))",
            )

        elif event.type == VkEventType.MESSAGE_NEW and event.to_me:
            image = self.vk_session_group_api.messages.getById(
                message_ids=[event.message_id]
            )["items"][0]["attachments"]
            image_url = image[0]["photo"]["sizes"][5]["url"]
            response = requests.get(image_url)
            bytes_im = io.BytesIO(response.content)
            image = Image.open(bytes_im)
            self.vk_session_group_api.messages.send(
                user_id=event.user_id,
                random_id=self.get_random_id(),
                message=f"Фото получил, скачиваю информацию о твоих друзьях",
            )
            friends_images = self.get_friends_images(event.user_id, self.num_friend)
            self.vk_session_group_api.messages.send(
                user_id=event.user_id,
                random_id=self.get_random_id(),
                message=f"Начинаю поиск",
            )
            img = find_face(image, friends_images)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            tmp = f"./{self.get_random_id()}.png"
            cv2.imwrite(tmp, img)
            self.vk_session_group_api.messages.send(
                user_id=event.user_id,
                random_id=self.get_random_id(),
                message=f"Фото обработалось, и сохранилось в папке скрипта, имя файла:{tmp}",
            )

    def get_img_from_url(self, url):
        response = requests.get(url)
        bytes_im = io.BytesIO(response.content)
        image = np.array(Image.open(bytes_im))
        return image

    def get_friends_images(self, user_id, num_friends):
        friends = self.vk_session_api.friends.get(
            user_id=user_id, count=num_friends, fields=["crop_photo"]
        )["items"]
        friends = [
            (
                self.get_img_from_url(fr["crop_photo"]["photo"]["sizes"][5]["url"]),
                fr["first_name"],
            )
            for fr in friends
            if "crop_photo" in fr
        ]
        return friends

    def get_random_id(self):
        curr_dt = datetime.now()
        return int(round(curr_dt.timestamp()))
