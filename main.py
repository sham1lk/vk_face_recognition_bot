from bot.auth import VkAuthorization
from bot.loop import VkEventHandler
from fire import Fire

if __name__ == "__main__":
    auth = VkAuthorization()
    event_handler = VkEventHandler(auth.vk_session, auth.vk_session_group)
    Fire(event_handler)
