# Smart Parking System

A web-based Smart Parking System that detects available slots, prevents double bookings, and tracks parking history in real-time. Built with Python (Flask) and JavaScript.

## 🚀 Features

- **Real-Time Dashboard**: View live statistics for available, occupied, and total parking slots.
- **Slot Management**:
  - **Book Slot**: Assign a vehicle to a specific parking slot with validation.
  - **Release Slot**: Free up a slot when a vehicle leaves.
- **Vehicle Validation**: Ensures valid vehicle ID formats (e.g., MH-01-AB-1234).
- **Activity History**: Tracks recent parking actions (bookings and releases).
- **Responsive Design**: Works seamlessly across desktop and mobile devices.

## 🛠️ Tech Stack

### Backend
- **Language**: Python 3
- **Framework**: Flask (Web Framework)
- **Extensions**: Flask-CORS (Cross-Origin Resource Sharing)
- **Data Storage**: In-memory storage (reset on server restart)

### Frontend
- **Structure**: HTML5
- **Styling**: CSS3 (Custom responsive design)
- **Logic**: Vanilla JavaScript
- **Communication**: Fetch API

## 📂 Project Structure

```
CLASS-SPS/
├── Code/
│   ├── Backend/            # Python Flask Server
│   │   ├── app.py          # Application entry point
│   │   ├── routes.py       # API endpoints
│   │   ├── models.py       # Data models
│   │   ├── services.py     # Business logic
│   │   ├── config.py       # Configuration & Initial Data
│   │   └── requirements.txt # Python dependencies
│   └── Frontend/           # Client-side Application
│       ├── index.html      # Main dashboard
│       ├── styles.css      # Stylesheet
│       └── script.js       # Frontend logic
├── Documentation/          # Project documentation
└── README.md              # Project overview (this file)
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.x installed
- A modern web browser (Chrome, Firefox, Edge, etc.)

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd Code/Backend
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask server:
   ```bash
   python app.py
   ```
   *The server will start running at `http://localhost:5000`*

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd Code/Frontend
   ```

2. Open `index.html` in your web browser.
   - You can double-click the file, or use a live server extension.

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/status` | Get current status of all parking slots |
| `POST` | `/api/book` | Book a specific slot for a vehicle |
| `POST` | `/api/release` | Release a specific slot |
| `GET` | `/api/history` | Get recent booking/release history |

## ⚠️ Notes

- **Data Persistence**: This application uses **in-memory storage**. If you restart the backend server, all booking data and history will be reset to the initial state defined in `config.py`.
- **CORS**: Cross-Origin Resource Sharing is enabled to allow the frontend file (served from `file://` or a different port) to communicate with the backend.

## 👥 Team Roles

| Name | Role | 
| :--- | :--- | 
| **Piyush Kumar** | Project Manager | 
| **Nishant Nehra** | Requirements Engineer | 
| **Lavish Singal** | Backend Developer | 
| **Asif Hoda** | Frontend Developer | 
| **Kunal Jha** | Tester | 
| **Ankit** | Quality Assurance Engineer | 
| **Anshul Mendiratta** | Integration Specialist | 
| **Bhupesh Yadav** | Documentation Specialist | 
