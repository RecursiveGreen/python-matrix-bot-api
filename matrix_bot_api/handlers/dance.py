from matrix_bot_api.mcommand_handler import MCommandHandler
from matrix_bot_api.media import prepare_image

try:
    from config import DANCE
except ImportError:
    DANCE = None

def dance_callback(room, event):
    if DANCE:
        pic = prepare_image(room.client, DANCE)
        room.send_image(pic['uri'], pic['filename'], **pic['info'])
    else:
        resp = emoji.emojize("shakes his money-maker! :notes: :dancers: :notes:",
                             use_aliases=True)
        room.send_emote(resp)

dance_handler = MCommandHandler("dance", dance_callback)