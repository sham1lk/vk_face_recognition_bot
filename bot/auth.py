import os

import vk_api


class VkAuthorization:
    def __init__(self):
        self.vk_session_group = self.get_session_by_token()
        self.vk_session = self.get_session_by_pass()

    def get_session_by_pass(self):
        vk_session = vk_api.VkApi(os.environ["LOGIN"], os.environ["PASSWORD"])
        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return
        return vk_session

    def get_session_by_token(self):
        token = os.environ["VK_TOKEN"]
        if not token:
            raise ValueError("VK_TOKEN variable should be provided in your environment")
        vk_session = vk_api.VkApi(token=token)
        return vk_session
