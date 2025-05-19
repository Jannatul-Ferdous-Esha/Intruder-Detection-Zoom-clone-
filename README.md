Intruder Detection Zoom Clone
This project is a web-based video conferencing application inspired by Zoom, enhanced with an intruder detection feature. It allows users to create and join virtual meetings with added security measures.

Features
Video Calling: Real-time video communication between participants.

Meeting Rooms: Create and join meetings using unique room numbers.

Chat Functionality: Instant messaging within meeting rooms.

Intruder Detection: Monitors participants and captures images of unrecognized users.

Zoom Link Generation: Generate shareable links for meetings.

Demo
A demonstration video showcasing the application's features will be added here.

Installation
Prerequisites
Python 3.x

pip (Python package installer)

Virtual environment tool (optional but recommended)

Steps
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/Jannatul-Ferdous-Esha/Intruder-Detection-Zoom-clone-.git
cd Intruder-Detection-Zoom-clone-
Create a Virtual Environment (optional):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Apply Migrations:

bash
Copy
Edit
python manage.py migrate
Run the Development Server:

bash
Copy
Edit
python manage.py runserver
Access the Application:

Open your web browser and navigate to http://127.0.0.1:8000/.

Project Structure
php
Copy
Edit
Intruder-Detection-Zoom-clone-
├── meeting_app/              # Django app containing views, models, and templates
├── static/                   # Static files (CSS, JavaScript, images)
│   └── captured_photos/      # Stored images of detected intruders
├── zoom/                     # Project settings and URLs
├── db.sqlite3                # SQLite database
├── manage.py                 # Django's command-line utility
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
Usage
Creating a Meeting: Navigate to the homepage and click on "Create Meeting" to generate a new room.

Joining a Meeting: Enter the room number or use the provided link to join an existing meeting.

Chatting: Use the chat panel within the meeting room to send messages to other participants.

Intruder Detection: The application monitors participants and captures images of any unrecognized users, storing them in the static/captured_photos/ directory.
