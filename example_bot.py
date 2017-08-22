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

from matrix_bot_api.handlers.dance import dance_handler
from matrix_bot_api.handlers.dice import dice_handler
from matrix_bot_api.handlers.echo import echo_handler
from matrix_bot_api.handlers.hello import hello_handler
from matrix_bot_api.handlers.love import love_handler

def main():
    # Create an instance of the MatrixBotAPI
    bot = MatrixBotAPI()

    # Add handlers
    bot.add_handler(dance_handler)
    bot.add_handler(dice_handler)
    bot.add_handler(echo_handler)
    bot.add_handler(hello_handler)
    bot.add_handler(love_handler)

    # Start polling
    bot.start_polling()

    # Allow for direct interaction
    current_room = None
    
    while True:
        if current_room:
            n = current_room.name if current_room.name else current_room.room_id
            prompt = n + ": "
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
                elif cmd['command'] == "deattach":
                    current_room = None
                elif cmd['command'] == "join":
                    r = cmd['args'].split()[0]
                    found = False
                    for room_id, room in bot.client.get_rooms().items():
                        if r == room_id or r in room.aliases:
                            print("ERROR: Already joined to this room.")
                            found = True
                    if not found:
                        new_room = bot.client.join_room(r)
                        current_room = new_room
                elif cmd['command'] == "joined":
                    for rid, room in bot.client.get_rooms().items():
                        print(rid)
                        print("    (Name: {}, Aliases: {})".format(room.name,
                                                                   room.aliases))
                elif cmd['command'] == 'leave':
                    current_room.leave()
                    current_room = None
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
