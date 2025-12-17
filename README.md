<div align="center">

# 💬 CS50 Chat
### Real-Time Anonymous Messaging

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![Socket.IO](https://img.shields.io/badge/Socket.IO-Real--time-orange.svg)

**[📹 Video Demo](INSERT_YOUR_VIDEO_URL_HERE)** | **[🚀 Quick Start](#-quick-start)** | **[📖 Documentation](#-project-structure)**

</div>

---

## 🌟 Overview

**CS50 Chat** is a privacy-first, real-time messaging platform where conversations live only in memory. No databases, no registration, no traces—just pure, ephemeral communication.

### ✨ Key Features

- **🔒 Zero Data Persistence** — Messages exist only in RAM and vanish when the session ends
- **👤 Complete Anonymity** — No sign-ups, no user tracking, no message history
- **⚡ Real-Time Communication** — Powered by WebSockets for instant message delivery
- **🎨 Discord-Inspired UI** — Modern dark mode interface with smooth UX
- **👥 Room Capacity Controls** — Create private rooms with custom user limits (2-4 people)
- **🛡️ Strict Mode Security** — Advanced synchronization prevents ghost users and state corruption

### 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python + Flask |
| Real-Time Engine | Socket.IO + Eventlet |
| Frontend | HTML5 + CSS3 + Vanilla JavaScript |
| Session Management | Flask-Session |
| Architecture | Event-Driven, In-Memory State |

---

## 🎯 Distinctiveness & Complexity

Unlike traditional CRUD-based Flask applications taught in CS50, **CS50 Chat** is a **fully event-driven application** built on stateful WebSocket connections. Here's what makes it unique:

### 🔌 WebSockets vs. Traditional HTTP

**The Challenge:** Traditional HTTP is stateless—the server forgets you after each request. This project required maintaining **persistent, bidirectional connections** for every active user.

**The Solution:** Implemented Socket.IO to handle real-time events:
- `connect` / `disconnect` — User lifecycle management
- `message` — Real-time message broadcasting
- `join` / `leave` — Dynamic room membership

This required careful orchestration of concurrent events that can fire at any moment, far beyond simple route handling.

### 💾 In-Memory State Management

**The Challenge:** Without a database, all data (rooms, messages, user lists) lives in Python dictionaries. No ACID guarantees, no automatic consistency.

**The Solution:** Built custom synchronization logic to handle:
- **Race Conditions** — Multiple users joining/leaving simultaneously
- **Atomic Updates** — Ensuring user counts remain accurate
- **Manual Validation** — Every state change requires explicit validation

This complexity far exceeds typical database-backed applications where the DB handles consistency.

### 🔄 Real-Time Synchronization

**The Challenge:** When a user disconnects, all other users must be notified instantly. When the last user leaves, the room must self-destruct to free memory.

**The Solution:** Implemented comprehensive garbage collection and state broadcasting:
- Instant notifications to all room participants
- Automatic room cleanup when empty
- Ghost user prevention through strict session management

This required deep understanding of concurrent programming and event-driven architectures.

---

## 📁 Project Structure

```
CS50-Chat/
├── 🐍 app.py                # Core application logic
├── 🔧 helpers.py            # Utility functions
├── 📋 requirements.txt      # Python dependencies
├── 📂 templates/
│   ├── layout.html         # Base template with metadata
│   ├── home.html           # Landing page
│   └── room.html           # Chat interface
├── 📂 static/
│   ├── css/
│   │   └── styles.css      # Discord-inspired dark theme
│   └── js/
│       └── room.js         # Client-side Socket.IO logic
└── 📂 flask_session/        # Session data storage
```

### 🔍 Key Components

#### [`app.py`](app.py) — Application Core

The heart of the application, orchestrating all backend logic:

| Component | Description |
|-----------|-------------|
| **HTTP Routes** | `GET /` — Landing page<br>`POST /chat` — Room validation & session creation |
| **Socket Events** | `connect`, `disconnect`, `message`, `join`, `leave` handlers |
| **Helper Functions** | `cleanup_room()` — Unified cleanup for disconnects and manual exits |
| **Data Structures** | `rooms{}` — Active chat sessions, messages, capacity limits<br>`socket_map{}` — Maps Socket IDs to usernames |

#### [`templates/layout.html`](templates/layout.html) — Base Template

Jinja2 foundation containing:
- Application metadata
- Socket.IO client library import
- Global CSS stylesheet link
---

## 🧠 Design Decisions

### 1️⃣ RAM vs. Database — Choosing Ephemerality

**The Decision:** Store all data in-memory using Python dictionaries instead of SQLite/PostgreSQL.

**Rationale:**

| Criterion | In-Memory | Database |
|-----------|-----------|----------|
| **Privacy** | ✅ Data vanishes on server restart/room closure | ❌ Persistent traces on disk |
| **Performance** | ✅ RAM I/O is orders of magnitude faster | ❌ Disk I/O latency |
| **Philosophy** | ✅ True ephemeral messaging | ❌ Contradicts temporary nature |

**Outcome:** Perfect alignment with the privacy-first philosophy—messages truly cease to exist.

---

### 2️⃣ Strict Mode — Preventing Ghost Users

**The Problem:** Page refreshes create a "refresh loop":
1. User refreshes → WebSocket disconnects
2. New socket connection established
3. Result: Duplicate user entries ("ghost users")

**The Solution:** **Session Ticket System**

```python
# On room entry
session['username'] = form_data['username']  # Store ticket
---
```

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Installation

```bash
# 1. Navigate to project directory
cd "d:\Programming\CS50x\Final Project"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
flask run
```

### Testing

Open the provided local URL (typically `http://127.0.0.1:5000`) in:
- **Two separate browser tabs**, OR
- **One normal + one incognito window**

This simulates multiple users for testing room functionality.

---

## 🎨 Features Showcase

### 🏠 Home Page
- Clean dual-panel layout
- Create custom rooms with capacity limits
- Join existing rooms via room ID

### 💬 Chat Interface
- Discord-inspired dark mode
- Real-time message delivery
- Live user count
- Smooth message bubbles (sent/received differentiation)

### 🔐 Security
- No user registration required
- Zero data persistence
- Ghost user prevention
- Session-based access control

---

## 📚 Learning Outcomes

Building **CS50 Chat** taught:
- **Event-Driven Architecture** — Managing asynchronous WebSocket events
- **Concurrent Programming** — Handling race conditions and state synchronization
- **Memory Management** — Manual garbage collection for in-memory data
- **UX Design** — Creating intuitive interfaces with defensive programming
- **Security Patterns** — Session management and ghost user prevention

---

## 📝 License

This project is part of CS50's Final Project requirement.

---

<div align="center">

**Built with 💙 for CS50x**

*Privacy-First • Real-Time • Ephemeral*

</div>

```python
def cleanup_room(sid, room_id):
    # Remove from socket_map
    # Decrement room count
    # Broadcast update to remaining users
    # Delete room if empty
```

**Benefits:**
- **DRY Compliance** — No code duplication
- **Consistency** — Identical behavior regardless of disconnect type
- **Maintainability** — Single source of truth for cleanup logic

---

### 4️⃣ Room Capacity Limits — Server Protection

**Implementation:** User-defined capacity (2-4 people) validated before room entry.

**Validation Logic:**
```python
if current_members < room_limit:
    allow_join()
else:
    reject_with_error()
```

**Benefits:**
- Prevents server overload
- Creates intimate chat environments
- Pre-join validation reduces wasted resources
#### 1. RAM vs. Database

One of the decisions I had to make was where to keep messages. I had to decide if I should use a database like sqlite3. I decided to use RAM, which's, like using Python Dictionaries for a couple of reasons:

* **Privacy:** The main idea of this project is to make messages that do not last long. I do this by keeping all the information in the computers memory. This means that if the server has to restart or the room is closed all the information is completely gone. There is no record of it, on the drive. This way the messages are really temporary like the project says and that is what I want for the messaging system. The messaging system is supposed to be ephemeral so I make sure that the messages are ephemeral too.

* **Performance:** Reading/Writing to memory is orders of magnitude faster than disk I/O, which is critical for a real-time chat experience.

#### 2. The "Strict Mode" Refresh Policy

So when you are using socket applications you will often have a problem called the Refresh Loop. This happens when a user of the socket app refreshes the page. When they do this the socket connection is. Then it opens again. This can cause some issues like making it seem like there are extra users, on the system or it can make duplicate entries of the same user. The socket app will show these users or entries even though they are not really there and that is why we call them "ghost" users.

To solve this problem I came up with an idea, which is a **Session Ticket System**. This **Session Ticket System** is what I think will work. I decided to use this **Session Ticket System** to fix the issue.

* When a user fills out the login form and submits it I put the users user_name in their Flask session.

* When the room loads I get this name by using `session.pop()` to retrieve it. I am talking about the name that is stored in the session and I use `session.pop()` to get the name.

* This works like a ticket that you can only use once. If you refresh the page your session is gone because the ticket is used up. Then the server sends you back to the Home page. This means that the chat is really temporary: you cannot get back, into a session by reloading the page you have to log in to the chat again. The chat is temporary so you have to log in to the chat if you want to use the chat.

#### 3. Handling "Disconnect" vs. "Leave"

I was thinking about how to handle the situation when a user closes the tab and when a user clicks the Leave button. At first I thought it would be an idea to have different rules, for each case.. Then I realized that this approach would mean I have to write similar code twice. This could cause problems and the room count might not be accurate. I did not want the room count to get out of sync. So I had to think of a way to handle the situation when a user closes the tab and when a user clicks the Leave button.

* **Decision:** I changed the code to use one helper function called `cleanup_room`. This way if a user clicks "Leave" or their internet connection goes down the same thing happens. The `cleanup_room` function removes the user, from the `socket_map`. Decreases the room count in a safe way. This makes sure that the same cleanup steps are taken every time whether the user leaves on purpose or their WiFi crashes.

#### 4. Room Capacity Limits

I added a thing to the rooms that people create. Now they can say how many people are allowed in the room. For example they can say 2 or 3 or 4 people. To make this work I had to add a check to see if there are already many people, in the room. I did this by adding a check (`if members < limit`) when someone tries to join the room. This check happens before the room even really opens up. This helps the server not get too busy. It makes the room feel more private.

### How to Run

1. Navigate to the project directory.

2. Install dependencies:

```bash

pip install -r requirements.txt

```

3. Run the Flask application:

```bash

flask run

```

4. Open the provided URL in two different browser tabs (or use Incognito mode) to simulate two different users.