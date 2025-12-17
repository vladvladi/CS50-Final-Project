from flask import Flask, redirect , render_template ,session, request, url_for
from flask_session import Session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from helpers import apology, generate_code, check_code, clean_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*") # Allow CORS for all origins for testing purposes

# Global rooms dictionary
rooms = {}

#socket map to keep track of users socket ids
socket_map = {}

@app.route('/')
def home():
    return render_template('home.html') # Render home page

@app.route('/chat', methods=["GET","POST"])
def chat():
    if request.method == "POST": # Handle form submission
        username = request.form.get("name")
        
        if not username:
            return apology('Please enter a name') # Apology if no name provided
        
        session["user_name"] = username
        
        action = request.form.get("action") # Determine if user wants to join or create a room
        
        if action == "join":
            code = request.form.get("code") # Get room code from form
            
            if not code:
                return apology('Please enter a room code') # Apology if no room code provided
            
            if(check_code(code, rooms)): # Check if room exists
                if rooms[code]["members"] < rooms[code]["limit"]: # Check if room is not full
                    return redirect(url_for('room', code=code)) # Render room page
                else:
                    return apology('Room is full', 403) # Apology if room is full
                
            else:
                return apology('Room does not exist', 404) # Apology if room does not exist
            
        elif action == "create":
            new_code = generate_code() # Generate a new room code
            
            while check_code(new_code, rooms): # Ensure the generated code is unique
                new_code = generate_code() # Generate a new room code if the previous one already exists
                
            capacity = request.form.get("room_size")
            if not capacity or not capacity.isdigit() or int(capacity) <= 0:
                return apology('Please enter a valid room size') # Apology if room size is invalid
            
            room_data = {"members": 0, "user_names": [], "limit": int(capacity), "messages": []} # Initialize room data
            rooms[new_code] = room_data # Store room data in global rooms dictionary
            return redirect(url_for('room', code=new_code)) # Render room page
        
    return redirect('/') # Redirect to home for GET requests

@app.route('/room/<code>')
def room(code):
    if not check_code(code, rooms):
        return apology('Room does not exist', 404) # Apology if room does not exist
    
    username = session.pop("user_name", None)  # Get the last added username for display
    
    if username is None:
        return redirect('/') # Kick to homepage on refresh
    
    capacity = rooms[code]["limit"]
    count = rooms[code]["members"]
    messages = rooms[code]["messages"]
    return render_template('room.html', code=code, room_size=capacity , user_name=username , members_count=count , messages=messages)

# SocketIO event handlers
@socketio.on('join')
def on_join(data):   
    username = data.get('username')
    room = data.get('room')
    
    if not room:
        return  # Early exit if data is missing
    if not username or not room:
        return  # Early exit if data is missing
    
    join_room(room)
    
    socket_map[request.sid] = {"username": username, "room": room}  # Map socket ID to username and room
    
    if room in rooms:
        rooms[room]['members'] += 1
        rooms[room]['user_names'].append(username)  

    emit('update_members', {'count': rooms[room]['members']}, to=room)  # Update member count in room
    emit('message', {'name': 'System', 'text': f' "{username}" has joined the room.'}, to=room)

@socketio.on('disconnect')
def on_disconnect():
    username = socket_map.get(request.sid)['username']
    room = socket_map.get(request.sid)['room']
    
    if not username or not room:
        return  # Early exit if data is missing
    
    clean_room(room, username, request.sid, rooms, socket_map)
    
    emit('update_members', {'count': rooms[room]['members'] if room in rooms else 0}, to=room)  # Update member count in room
    emit('message', {'name': 'System', 'text': f'{username} has left the room'}, to=room)
    emit('redirect', {'url': '/'}, to=request.sid)  # Send redirect only to leaving user
    
@socketio.on('leave')
def on_leave(data):
    username = data.get('username')
    room = data.get('room')
    
    clean_room(room, username, request.sid, rooms, socket_map)
    
    emit('update_members', {'count': rooms[room]['members'] if room in rooms else 0}, to=room)  # Update member count in room
    emit('message', {'name': 'System', 'text': f'{username} has left the room'}, to=room)
    emit('redirect', {'url': '/'}, to=request.sid)  # Send redirect only to leaving user

@socketio.on('message')
def handle_message(data):
    name = data.get('name')
    text = data.get('text')
    room = data.get('room')
    
    if not name or not text or not room:
        return  # Early exit if data is missing
    
    if room in rooms:
        rooms[room]['messages'].append({'name': name, 'text': text})  # Store message in room history
    
    emit('message', {'name': name, 'text': text}, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)