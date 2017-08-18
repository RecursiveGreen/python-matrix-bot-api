from matrix_bot_api.mcommand_handler import MCommandHandler

def echo_callback(room, event):
    args = event['content']['body'].split()
    args.pop(0)

    # Echo what they said back
    room.send_text(' '.join(args))

echo_handler = MCommandHandler("echo", echo_callback)