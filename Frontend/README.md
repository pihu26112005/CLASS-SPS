# Smart Parking System - Frontend

Modern, responsive web interface for parking management.

## Structure

```
frontend/
├── index.html          # Main HTML structure
├── styles.css          # Styling and animations
└── script.js           # Frontend logic and API integration
```

## Features

### **index.html**
- Semantic HTML5 structure
- SEO optimized with meta tags
- Accessible form elements
- Responsive layout structure

### **styles.css**
- Modern dark theme with glassmorphism
- CSS custom properties (variables)
- Smooth animations and transitions
- Fully responsive design
- Mobile-first approach

### **script.js**
- API integration with fetch
- Real-time updates (auto-refresh every 30s)
- Form validation and handling
- Toast notifications
- Loading states
- Error handling

## Running

### Option 1: Direct File
```bash
# Simply open index.html in your browser
open index.html
```

### Option 2: Python Server (Recommended)
```bash
cd frontend
python -m http.server 8000
# Visit http://localhost:8000
```

### Option 3: Node.js Server
```bash
cd frontend
npx http-server -p 8000
# Visit http://localhost:8000
```

## Configuration

Update API URL in `script.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```
