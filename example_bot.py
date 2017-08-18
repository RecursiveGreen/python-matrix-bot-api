"""
A test bot using the Python Matrix Bot API

Test it out by adding it to a group chat and doing one of the following:
1. Say "Hi"
2. Say !echo this is a test!
"""

from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_bot_api.mcommand_handler import MCommandHandler
from matrix_bot_api.cli import get_command

from config import *

def hi_callback(room, event):
    # Somebody said hi, let's say Hi back
    sender = room.client.api.get_display_name(event['sender'])
    room.send_text("Hi, {}!".format(sender))

def echo_callback(room, event):
    args = event['content']['body'].split()
    args.pop(0)

    # Echo what they said back
    room.send_text(' '.join(args))

def main():
    # Create an instance of the MatrixBotAPI
    bot = MatrixBotAPI(USERNAME, PASSWORD, SERVER, ROOMS, AVATAR, DISPLAYNAME)

    # Add a regex handler waiting for the word Hi
    hi_handler = MRegexHandler(r"(^hi\b|^hello\b|^howdy\b)",
                               hi_callback,
                               case_sensitive=False)
    bot.add_handler(hi_handler)

    # Add a regex handler waiting for the echo command
    echo_handler = MCommandHandler("echo", echo_callback)
    bot.add_handler(echo_handler)

    # Start polling
    bot.start_polling()

    # Allow for direct interaction
    current_room = None
    
    while True:
        if current_room:
            prompt = current_room.name + ": "
        else:
            prompt = "<" + bot.username + ">: "

        msg = input(prompt)
        cmd = get_command(msg)

        if msg:
            if cmd:
                if cmd['command'] == "attach":
                    rid = cmd['args'].split()[0]
                    found = False
                    for room_id, room in bot.client.get_rooms().items():
                        if room_id == rid:
                            current_room = room
                            found = True
                    if not found:
                        print("ERROR: Not joined to this room or invalid room id.")
                elif cmd['command'] == "joined":
                    for rid, room in bot.client.get_rooms().items():
                        print(rid)
                        print("    (Name: {}, Aliases: {})".format(room.name,
                                                                   room.aliases))
                elif cmd['command'] == "quit":
                    break
                else:
                    print("ERROR: Unknown command.")
            else:
                if current_room:
                    current_room.send_text(msg)
                else:
                    print("ERROR: Select room to send message to with /attach.")

if __name__ == "__main__":
    main()
