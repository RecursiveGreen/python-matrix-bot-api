from matrix_bot_api.mcommand_handler import MCommandHandler
from matrix_bot_api.media import prepare_image

from config import DANCE

def dance_callback(room, event):
    pic = prepare_image(room.client, DANCE)
    room.send_image(pic['uri'], pic['filename'], **pic['info'])

dance_handler = MCommandHandler("dance", dance_callback)