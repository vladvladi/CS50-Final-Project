from flask import Flask , render_template , redirect
from flask_socketio import leave_room
import random
import string

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def generate_code(length=4):
    """Generate a random room code."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))


def check_code(code, rooms):
    """Check if room code exists."""
    return code in rooms


def clean_room(room, username, sid, rooms, socket_map):
    """Clean up room data when a user leaves."""
    leave_room(room)
    
    if room in rooms:
        rooms[room]['members'] -= 1
        rooms[room]['user_names'].remove(username)
        if rooms[room]['members'] == 0:
            del rooms[room]  # Delete empty room
            
    if sid in socket_map:
        del socket_map[sid]