# LLM Data Explorer for Overture Maps

**Empowering users to explore Overture Maps data through natural language using Large Language Models**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue)](https://project-terraforma.github.io/Ashwin-DaD/)

---

## 📋 Overview

While interactive dashboards are useful, they often fail to address the specific, nuanced questions individual users have about Overture's data. This project provides a **flexible and user-driven method** for data exploration by:

1. **Generating an LLM-ready context file** - A comprehensive text document containing statistics, schema descriptions, and pre-written prompts
2. **Providing a web interface** - Beautiful landing page for users to download and learn about the tool
3. **Collecting user feedback** - Anonymous feedback system to continuously improve the experience

Users can simply download the context file, paste it into their preferred LLM (ChatGPT, Claude, Gemini, etc.), and immediately start exploring Overture Maps data through natural language queries.

---

## 🌟 Features

### 🤖 LLM-Ready Data Context
- **Comprehensive statistics** for all 6 Overture themes (Addresses, Buildings, Places, Divisions, Transportation, Base)
- **Natural language schema descriptions** optimized for LLM understanding
- **Pre-written prompts** to guide data exploration
- **Compact format** (~22 KB, ~10K tokens) - fits in any LLM context window

### 🌐 Web Interface
- **Professional landing page** ([docs/index.html](docs/index.html)) with:
  - One-click file download
  - Clear usage instructions
  - Example queries
  - Technical specifications
- **Responsive design** matching Overture Maps branding
- **GitHub Pages ready** for instant deployment

### 📊 Feedback System
- **Anonymous survey** capturing user satisfaction and usability
- **Smart trigger** - Appears when users return after trying the tool (5 second delay)
- **Flask API backend** with SQLite database
- **Admin dashboard** with real-time statistics, charts, and CSV export

---

## 📁 Project Structure

```
Ashwin-DaD/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies for generator
│
├── generate_llm_context.py             # Main script - generates LLM context file
├── analyze_metrics.py                  # Helper script for metrics analysis
├── README_generation_output.txt        # Generated LLM-ready file (output)
│
├── Metrics/metrics/                    # Overture metrics data (by release)
│   └── 2025-09-24.0/                   # Latest release data
│       ├── addresses_*.csv
│       ├── buildings_*.csv
│       ├── places_*.csv
│       └── ...
│
└── docs/                               # Web interface & feedback system
    ├── index.html                      # Landing page (GitHub Pages)
    ├── admin_dashboard.html            # Feedback admin panel
    │
    ├── feedback_api.py                 # Flask API for feedback
    ├── requirements.txt                # API dependencies (Flask, CORS)
    ├── feedback.db                     # SQLite database (created on run)
    │
    ├── start_feedback_server.sh        # Quick start script (Mac/Linux)
    ├── start_feedback_server.bat       # Quick start script (Windows)
    │
    ├── README_FEEDBACK.md              # Feedback system quick start
    ├── FEEDBACK_SETUP.md               # Detailed setup guide
    ├── ARCHITECTURE.md                 # System architecture docs
```

---

## 🚀 Quick Start

### Option 1: Use the Live Website (Easiest)

Visit the live site: **https://project-terraforma.github.io/Ashwin-DaD/**

1. Click "Generate & Download"
2. Open the downloaded file
3. Copy contents into your LLM (ChatGPT, Claude, etc.)
4. Start asking questions!

### Option 2: Generate the File Locally

```bash
# 1. Clone the repository
git clone https://github.com/project-terraforma/Ashwin-DaD.git
cd Ashwin-DaD

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the LLM context file
python3 generate_llm_context.py

# 4. Use the generated file
# Copy README_generation_output.txt contents into your LLM
```

---

## 📊 Example Queries

Once you load the context file into your LLM, you can ask questions like:

| Category | Example Question |
|----------|------------------|
| **Geographic** | "Which countries have the highest concentration of Places data?" |
| **Data Quality** | "What proportion of places have high confidence scores (≥0.8)?" |
| **Categories** | "What are the top 10 most common building types globally?" |
| **Comparisons** | "How much data changed in this release vs the previous?" |
| **Statistics** | "What percentage of buildings are residential vs commercial?" |
| **Sources** | "Which data sources contribute most to the Places theme?" |

The LLM will use the statistics and schema information to provide accurate, data-driven answers.

---

## 🛠️ Development Setup

### Generate LLM Context File

```bash
# Install dependencies
pip install -r requirements.txt

# Run generator
python3 generate_llm_context.py
```

**What it does:**
- Analyzes all metrics CSV files from the latest release
- Extracts schema information and statistics
- Generates `README_generation_output.txt`
- Reports file size (~22 KB) and token count (~10K)

### Run Web Interface Locally

```bash
# Just open the HTML file
open docs/index.html

# Or serve with Python
cd docs
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Run Feedback System Locally

```bash
# Install API dependencies
cd docs
pip install -r requirements.txt

# Start Flask API (option 1: quick script)
./start_feedback_server.sh

# Start Flask API (option 2: manual)
python3 feedback_api.py

# Open admin dashboard
open admin_dashboard.html
```

The API runs on `http://localhost:5001` and the dashboard shows real-time feedback statistics.

---

## 🌐 Production Deployment

### Frontend (GitHub Pages)

Already configured! Just push to GitHub:

```bash
git add .
git commit -m "Update site"
git push origin main

# Enable GitHub Pages:
# Settings → Pages → Source: main branch → /docs folder → Save
```

Your site will be live at: `https://project-terraforma.github.io/Ashwin-DaD/`

### Backend API (Vercel - Recommended)

**Why Vercel?** No cold starts, instant response, 100% free.

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
cd docs
vercel --prod

# Your API is live at: https://ashwin-terraforma-d.vercel.app/api
```

**Alternative deployment options:**
- Railway.app (10-15 sec cold start)
- Render.com (30-60 sec cold start)
- Fly.io (5-10 sec cold start)

See [DEPLOY_PRODUCTION.md](docs/DEPLOY_PRODUCTION.md) for detailed instructions.

---

## 📈 Feedback System

The feedback system captures anonymous user satisfaction and usability data.

### How It Works

1. User downloads the LLM context file → timestamp stored
2. User navigates away (switches tab/window) → flag set
3. 5+ minutes pass → timer condition met
4. User returns to page → survey modal appears
5. User submits feedback → data stored in SQLite database

### Survey Questions

1. Overall satisfaction (1-5 stars)
2. Instruction clarity (1-5 scale)
3. LLM provider used (dropdown)
4. Did it answer questions? (Yes/Partially/No)
5. What could be improved? (optional text)
6. Share LLM conversation (optional text)

### View Feedback Data

**Option 1: Admin Dashboard** (Recommended)
```bash
open docs/admin_dashboard.html
```

**Option 2: Direct Database**
```bash
sqlite3 docs/feedback.db "SELECT * FROM feedback ORDER BY timestamp DESC;"
```

See [README_FEEDBACK.md](docs/README_FEEDBACK.md) for complete documentation.

---

## 🧪 Testing the Feedback Modal

To test the survey popup immediately:

```javascript
// Open browser console (F12) and run:
localStorage.setItem('llm_explorer_downloaded', 'true');
localStorage.setItem('llm_explorer_download_time', Date.now() - (6 * 60 * 1000));

// Show modal immediately
showFeedbackModal();
```

Or uncomment line 953 in `docs/index.html` to enable testing mode (shows after 2 seconds).

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README_FEEDBACK.md](docs/README_FEEDBACK.md) | Feedback system quick start guide |
| [FEEDBACK_SETUP.md](docs/FEEDBACK_SETUP.md) | Detailed feedback setup instructions |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture and data flow |
| [DEPLOY_PRODUCTION.md](docs/DEPLOY_PRODUCTION.md) | Production deployment guide |
| [DEPLOY_NOW.md](docs/DEPLOY_NOW.md) | Quick Vercel deployment |
| [CLAUDE.md](CLAUDE.md) | Project context and requirements |

---

## 🔒 Privacy & Security

- **Anonymous feedback collection** - No PII collected
- **CORS enabled** for browser access
- **Input validation** on all API endpoints
- **SQL injection prevention** via parameterized queries
- **Rate limiting ready** (optional Flask-Limiter integration)

---

## 🛣️ Roadmap

### Completed ✅
- [x] LLM context file generation
- [x] Web landing page
- [x] Feedback survey system
- [x] Flask API backend
- [x] SQLite database
- [x] Admin dashboard
- [x] Production deployment (Vercel)
- [x] GitHub Pages integration

### Future Enhancements 🚧
- [ ] Email notifications for new feedback
- [ ] Sentiment analysis on text responses
- [ ] Multiple export formats (Excel, JSON, PDF)
- [ ] User segmentation analytics
- [ ] A/B testing for survey questions
- [ ] Real-time dashboard updates (WebSockets)
- [ ] Admin authentication
- [ ] Integration with analytics platforms

---

## 🤝 Contributing

This is a personal project for Overture Maps Foundation. For questions or suggestions, please open an issue.

---

## 📄 License

This project is part of the Overture Maps Foundation initiative.

---

## 🙏 Acknowledgments

- **Overture Maps Foundation** for providing comprehensive geospatial data
- **GitHub Pages** for free static hosting

---

## 📧 Contact

**Ashwin Prabou**
- GitHub: [@aprabou](https://github.com/aprabou)

---

**Live Site:** https://project-terraforma.github.io/Ashwin-DaD/

---

*Last Updated: December 2025*
