# LLM Data Explorer - Feedback System

## 📋 Quick Overview

This feedback system captures user satisfaction and usability data after users download and use the LLM context file.

### Components:
- **Frontend**: Modal popup in [index.html](index.html)
- **Backend**: Flask API in [feedback_api.py](feedback_api.py)
- **Database**: SQLite (`feedback.db`)
- **Admin Panel**: [admin_dashboard.html](admin_dashboard.html)

## 🚀 Quick Start (3 steps)

### 1. Install dependencies
```bash
cd docs
pip install -r requirements.txt
```

### 2. Start the API server
```bash
python3 feedback_api.py
```

### 3. Open the page
```bash
open index.html
```

That's it! The feedback system is now active.

## 📊 View Feedback Data

### Option 1: Admin Dashboard (Recommended)
```bash
open admin_dashboard.html
```

Beautiful web interface showing:
- Total responses and averages
- LLM provider distribution charts
- Questions answered breakdown
- Full feedback table
- CSV export button

### Option 2: Command Line
```bash
# View all feedback
curl http://localhost:5000/api/feedback

# View statistics
curl http://localhost:5000/api/feedback/stats
```

### Option 3: Direct Database Access
```bash
sqlite3 feedback.db "SELECT * FROM feedback ORDER BY timestamp DESC;"
```

## 🎯 How It Works

1. User downloads the LLM context file
2. Timestamp is stored in localStorage
3. User navigates away from the page
4. After 5+ minutes, when user returns, survey popup appears
5. User fills out the 6-question survey
6. Data is submitted to Flask API
7. API stores data in SQLite database
8. View results in admin dashboard

## 📝 Survey Questions

1. **Overall satisfaction** (1-5 stars) - Required
2. **Instruction clarity** (1-5 scale) - Required
3. **LLM provider used** (dropdown) - Required
4. **Did it answer questions?** (Yes/Partially/No) - Required
5. **What could be improved?** (text) - Optional
6. **Share LLM conversation** (text) - Optional

## 🗂️ Files

```
docs/
├── index.html              # Main page with feedback modal
├── feedback_api.py         # Flask API backend
├── admin_dashboard.html    # Admin panel to view feedback
├── requirements.txt        # Python dependencies
├── FEEDBACK_SETUP.md      # Detailed setup guide
└── feedback.db            # SQLite database (created on first run)
```

## 🔧 Configuration

### Change when survey appears
Edit `index.html` line ~593:
```javascript
const fiveMinutes = 5 * 60 * 1000; // Change 5 to desired minutes
```

### Change API URL (for production)
Edit `index.html` line ~768:
```javascript
const API_BASE_URL = 'https://yourdomain.com/api';
```

## 🌐 Production Deployment

See [FEEDBACK_SETUP.md](FEEDBACK_SETUP.md) for detailed deployment instructions including:
- Deploying to Heroku, AWS, Google Cloud
- Setting up reverse proxy with nginx
- Using serverless functions
- Security best practices

## 📊 Example Statistics

The admin dashboard shows:
- **Total Responses**: Count of all submissions
- **Average Satisfaction**: Mean star rating (1-5)
- **Average Clarity**: Mean clarity score (1-5)
- **LLM Provider Distribution**: Bar chart of which LLMs users prefer
- **Questions Answered**: Success rate chart
- **Recent Feedback**: Full table with all responses

## 🔒 Privacy

- All data is anonymous
- No user accounts or login required
- IP addresses stored only for abuse prevention
- Complies with privacy best practices

## 🐛 Troubleshooting

**Modal not appearing?**
```javascript
// Open browser console and run:
localStorage.setItem('llm_explorer_downloaded', 'true');
localStorage.setItem('llm_explorer_download_time', Date.now() - (6 * 60 * 1000));
// Then switch tabs and return
```

**API connection error?**
- Verify Flask server is running: `curl http://localhost:5000/api/health`
- Check CORS is enabled in `feedback_api.py`
- Look for errors in Flask console

**Database issues?**
- Check file permissions on `feedback.db`
- Restart the Flask server
- Database auto-initializes on first run

## 📚 More Info

For detailed setup, API documentation, and deployment guides, see:
- [FEEDBACK_SETUP.md](FEEDBACK_SETUP.md) - Complete setup guide

---

**Ready to collect feedback!** 🎉
