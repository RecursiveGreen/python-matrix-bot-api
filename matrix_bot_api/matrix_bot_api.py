import os
import re
import sys
import traceback

from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError

from .media import prepare_image

class MatrixBotAPI:

    # username - Matrix username
    # password - Matrix password
    # server   - Matrix server url : port
    # rooms    - List of rooms ids to operate in, or None to accept all rooms
    def __init__(self, username=None, password=None, server=None, rooms=None):
        # Load configuration variables
        self.config = dict(globals())
        with open(os.path.abspath("config.py"), "rb") as file:
            exec(compile(file.read(), os.path.abspath("config.py"), "exec"),
                 self.config)
        
        # Debugging will allow us to read events in realtime.
        self.debug = self.config.get('DEBUG', False)

        # Pull the username, password, and server variables from the config
        # file or from the function call. Otherwise, die with helpful message.
        self.username = self.config.get('USERNAME', username)
        if not self.username:
            print('ERROR: No username specified! Check the config.py!')
            sys.exit()

        self.password = self.config.get('PASSWORD', password)
        if not self.password:
            print('ERROR: No password specified! Check the config.py!')
            sys.exit()
        
        self.server = self.config.get('SERVER', server)
        if not self.server:
            print('ERROR: No server specified! Check the config.py!')
            sys.exit()

        # Authenticate with given credentials
        self.client = MatrixClient(self.server)
        try:
            self.client.login_with_password(self.username, self.password)
        except MatrixRequestError as e:
            print(e)
            if e.code == 403:
                print("Bad username/password")
        except Exception as e:
            print("Invalid server URL")
            traceback.print_exc()

        # Set profile defaults
        if self.config.get('AVATAR'):
            pic = prepare_image(self.client, self.config.get('AVATAR'))
            self.client.api.set_avatar_url(self.username, pic['uri'])
        
        if self.config.get('DISPLAYNAME'):
            self.client.api.set_display_name(self.username,
                                             self.config.get('DISPLAYNAME'))
        
        # Admins can invite the bot to various rooms.
        self.admins = self.config.get('ADMINS')

        # Store allowed rooms
        self.rooms = self.config.get('ROOMS')

        # Store empty list of handlers
        self.handlers = []

        # If rooms is None, we should listen for invites and automatically accept them
        if rooms is None:
            self.client.add_invite_listener(self.handle_invite)
            self.client.add_leave_listener(self.handle_leave)
            self.rooms = []

            # Add all rooms we're currently in to self.rooms and add their callbacks
            for room_id, room in self.client.get_rooms().items():
                room.add_listener(self.handle_message)
                self.rooms.append(room)
        else:
            # Add the message callback for all specified rooms
            for room in self.rooms:
                room.add_listener(self.handle_message)

    def add_handler(self, handler):
        self.handlers.append(handler)

    def handle_message(self, room, event):
        # if self.debug: print(event)
        
        # Make sure we didn't send this message
        if re.match(self.username, event['sender']):
            return

        # If we're the last one in the chat, then leave.
        if event['type'] == 'm.room.member':
            if event['membership'] == 'leave':
                joined = {j:k for j, k
                          in room.get_joined_members().items()
                          if j != self.username}
                if not joined:
                    if self.debug: print("Last one here. Leaving...")
                    room.leave()
                    return

        # Loop through all installed handlers and see if they need to be called
        for handler in self.handlers:
            if handler.test_callback(room, event):
                # This handler needs to be called
                handler.handle_callback(room, event)

    def handle_invite(self, room_id, state):
        if self.debug: print("Got invite to room: " + str(room_id))
        
        invite_event = [e for e
                        in state['events']
                        if e['type'] == 'm.room.member'
                           and e['content']['membership'] == 'invite'][0]
        
        # Only accept the invite if the sender is on the admin list
        if invite_event['sender'] in self.admins:
            if self.debug: print("Sender is an admin. Joining...")
            room = self.client.join_room(room_id)

            # Add message callback for this room
            room.add_listener(self.handle_message)

            # Add room to list
            self.rooms.append(room)
        else:
            if self.debug: print("Sender is NOT an admin. Ignoring...")
    
    def handle_leave(self, room_id, room):
        if self.debug: print("Left room: " + str(room_id))
        self.rooms = [r for r in self.rooms if r.room_id != room_id]

    def start_polling(self):
        # Starts polling for messages
        self.client.start_listener_thread()
