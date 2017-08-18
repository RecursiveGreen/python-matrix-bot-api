from matrix_bot_api.mregex_handler import MRegexHandler

def hello_callback(room, event):
    # Somebody said hi, let's say Hi back
    sender = room.client.api.get_display_name(event['sender'])
    room.send_text("Hi, {}!".format(sender))

hello_handler = MRegexHandler(r"(^hi\b|^hello\b|^howdy\b)",
                              hello_callback,
                              case_sensitive=False)
    