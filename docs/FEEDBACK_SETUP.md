# Feedback System Setup Guide

This guide explains how to set up and run the feedback collection system for the LLM Data Explorer page.

## 📋 Overview

The feedback system consists of:
- **Frontend**: HTML modal form that captures user feedback
- **Backend**: Flask API that receives and stores feedback
- **Database**: SQLite database that stores all responses anonymously

When users return to the page after downloading the file (5+ minutes later), they'll see a survey popup. Their responses are sent to the Flask API and stored in a local SQLite database.

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd docs
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Flask==3.0.0 flask-cors==4.0.0
```

### Step 2: Start the API Server

```bash
python3 feedback_api.py
```

You should see:
```
Database initialized at feedback.db
Starting Feedback API server...
Access the API at http://localhost:5000
Endpoints:
  POST /api/feedback - Submit feedback
  GET  /api/feedback - View all feedback
  GET  /api/feedback/stats - View statistics
  GET  /api/health - Health check
```

### Step 3: Open the Page

Open `index.html` in your browser. The page will automatically connect to the API running on `localhost:5000`.

### Step 4: Test the Feedback System

To test the modal during development, open browser console (F12) and run:

```javascript
localStorage.setItem('llm_explorer_downloaded', 'true');
localStorage.setItem('llm_explorer_download_time', Date.now() - (6 * 60 * 1000));
```

Then switch tabs and return - the modal should appear!

## 📊 Database Schema

The SQLite database (`feedback.db`) has a single table:

```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    satisfaction INTEGER NOT NULL,          -- 1-5 rating
    clarity INTEGER NOT NULL,               -- 1-5 rating
    llm_provider TEXT NOT NULL,             -- Which LLM they used
    questions_answered TEXT NOT NULL,       -- Yes/Partially/No/Haven't tried
    improvements TEXT,                      -- Optional text
    conversation TEXT,                      -- Optional LLM conversation
    user_agent TEXT,                        -- Browser info
    ip_address TEXT                         -- IP address (for abuse prevention)
);
```

## 🔌 API Endpoints

### POST /api/feedback
Submit new feedback.

**Request:**
```json
{
  "satisfaction": 5,
  "clarity": 4,
  "llm_provider": "Claude (Anthropic)",
  "questions_answered": "Yes",
  "improvements": "Would love more examples",
  "conversation": "Optional conversation text"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Feedback submitted successfully",
  "id": 1
}
```

### GET /api/feedback
Retrieve all feedback entries (admin use).

**Response:**
```json
{
  "success": true,
  "count": 10,
  "feedback": [
    {
      "id": 1,
      "timestamp": "2025-11-30 10:30:00",
      "satisfaction": 5,
      "clarity": 4,
      "llm_provider": "Claude (Anthropic)",
      "questions_answered": "Yes",
      "improvements": "Would love more examples",
      "conversation": "",
      "user_agent": "Mozilla/5.0...",
      "ip_address": "127.0.0.1"
    }
  ]
}
```

### GET /api/feedback/stats
Get aggregated statistics.

**Response:**
```json
{
  "success": true,
  "total_responses": 10,
  "average_satisfaction": 4.5,
  "average_clarity": 4.2,
  "llm_providers": [
    {"llm_provider": "Claude (Anthropic)", "count": 5},
    {"llm_provider": "ChatGPT (OpenAI)", "count": 3}
  ],
  "questions_answered": [
    {"questions_answered": "Yes", "count": 7},
    {"questions_answered": "Partially", "count": 2}
  ]
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-30T10:30:00"
}
```

## 📈 Viewing Feedback Data

### Option 1: Using the API

```bash
# View all feedback
curl http://localhost:5000/api/feedback

# View statistics
curl http://localhost:5000/api/feedback/stats
```

### Option 2: Query Database Directly

```bash
sqlite3 feedback.db
```

Then run SQL queries:
```sql
-- View all feedback
SELECT * FROM feedback ORDER BY timestamp DESC;

-- Count responses by LLM provider
SELECT llm_provider, COUNT(*) as count
FROM feedback
GROUP BY llm_provider
ORDER BY count DESC;

-- Average ratings
SELECT
    AVG(satisfaction) as avg_satisfaction,
    AVG(clarity) as avg_clarity
FROM feedback;

-- View recent improvements suggestions
SELECT timestamp, improvements
FROM feedback
WHERE improvements != ''
ORDER BY timestamp DESC
LIMIT 10;
```

### Option 3: Export to CSV

```bash
sqlite3 -header -csv feedback.db "SELECT * FROM feedback;" > feedback.csv
```

## 🔒 Privacy & Security

### Anonymous Collection
- No personally identifiable information is collected
- IP addresses are stored only for abuse prevention
- User agents help understand browser compatibility

### Data Retention
To delete old data:
```sql
DELETE FROM feedback WHERE timestamp < datetime('now', '-90 days');
```

### Rate Limiting (Optional)
For production, consider adding rate limiting:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/feedback', methods=['POST'])
@limiter.limit("5 per hour")  # Max 5 submissions per hour per IP
def submit_feedback():
    # ...
```

## 🌐 Production Deployment

### Option 1: Deploy on Same Server as Website

If hosting on a web server:

1. Update `API_BASE_URL` in `index.html`:
```javascript
const API_BASE_URL = 'https://yourdomain.com/api';
```

2. Use a production WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 feedback_api:app
```

3. Set up a reverse proxy (nginx example):
```nginx
location /api {
    proxy_pass http://localhost:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### Option 2: Deploy to Cloud

**Heroku:**
1. Create `Procfile`:
```
web: gunicorn feedback_api:app
```

2. Deploy:
```bash
git add .
git commit -m "Add feedback system"
heroku create your-app-name
git push heroku main
```

**Google Cloud Run / AWS Lambda / Azure Functions:**
See respective documentation for Flask deployment.

### Option 3: Use GitHub Pages + Serverless Function

Deploy the API as a serverless function:
- Vercel Functions
- Netlify Functions
- AWS Lambda

And update the `API_BASE_URL` accordingly.

## 🔧 Configuration Options

### Change when the survey appears

Edit line ~593 in `index.html`:
```javascript
const fiveMinutes = 5 * 60 * 1000; // Change 5 to desired minutes
```

### Disable time requirement (show immediately after download)

Edit line ~596 in `index.html`:
```javascript
// Remove "&& enoughTimePassed"
return hasDownloaded && !feedbackSubmitted && !feedbackShown;
```

### Change API URL

Edit line ~768 in `index.html`:
```javascript
const API_BASE_URL = 'http://your-api-url.com/api';
```

### Database Location

Edit line 11 in `feedback_api.py`:
```python
DATABASE = '/path/to/your/feedback.db'
```

## 🐛 Troubleshooting

### CORS Errors
If you see CORS errors in the browser console:
1. Make sure `flask-cors` is installed
2. Verify the API server is running
3. Check that `CORS(app)` is called in `feedback_api.py`

### Database Locked
If you get "database is locked" errors:
```bash
# Close any open connections
fuser feedback.db  # Linux
lsof feedback.db   # macOS

# Or simply restart the API server
```

### Modal Not Appearing
1. Check browser console for errors
2. Verify localStorage values:
```javascript
console.log(localStorage.getItem('llm_explorer_downloaded'));
console.log(localStorage.getItem('llm_explorer_download_time'));
```

3. Clear localStorage and test:
```javascript
localStorage.clear();
```

## 📝 Testing Commands

```bash
# Test health check
curl http://localhost:5000/api/health

# Submit test feedback
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "satisfaction": 5,
    "clarity": 4,
    "llm_provider": "Claude (Anthropic)",
    "questions_answered": "Yes",
    "improvements": "Test feedback",
    "conversation": ""
  }'

# View all feedback
curl http://localhost:5000/api/feedback

# View statistics
curl http://localhost:5000/api/feedback/stats
```

## 📧 Support

If you encounter issues:
1. Check the API server logs
2. Verify database permissions
3. Test API endpoints with curl
4. Check browser console for JavaScript errors

---

**Ready to go!** Start the API server and the feedback system will be fully operational. 🎉
