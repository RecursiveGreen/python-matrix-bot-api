import os
from random import randrange, seed
import re
from statistics import mean, median, stdev

from matrix_bot_api.mcommand_handler import MCommandHandler

seed(None)

def dice_callback(room, event):
    """ Handler for rolling dice """
    sender = room.client.api.get_display_name(event['sender'])
    
    args = event['content']['body'].split()
    args.pop(0)

    check = r"^([1-9]|1[0-9]|20)d([2-9]|[1-9][0-9]|100)$"
    found = re.search(check, args[0], re.IGNORECASE)

    if found:
        rolls = []
        num, sides = (int(found.group(1)), int(found.group(2)))
        
        room.send_emote('is rolling {} for {}...'.format(found.group(0), sender))

        for x in range(num):
            rolls.append(randrange(1, sides + 1))

        if num > 1:
            resp = "{}, here's what I rolled: {} (Avg: {}, Med: {}, StdDev: {})"
            room.send_text(resp.format(sender,
                                       rolls,
                                       mean(rolls),
                                       median(rolls),
                                       stdev(rolls)))
        else:
            room.send_text("{}, I rolled a {} ".format(sender, rolls[0]))

dice_handler = MCommandHandler("dice", dice_callback)
