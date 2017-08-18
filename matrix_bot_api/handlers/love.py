import emoji

from matrix_bot_api.mregex_handler import MRegexHandler

from config import DISPLAYNAME

def love_callback(room, event):
    sender = room.client.api.get_display_name(event['sender'])
    resp = emoji.emojize("Awww, I love you too {}! :heart:", use_aliases=True)
    room.send_text(resp.format(sender))

_name_re = r""
for name in DISPLAYNAME.split():
    _name_re = _name_re + r"(?=.*{})".format(name.lower())

_love_re = r"^" + _name_re + r"(?=.*i)(?=.*love)(?=.*you).*$"
love_handler = MRegexHandler(_love_re,
                             love_callback,
                             case_sensitive=False)