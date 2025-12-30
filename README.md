# 🚀 Job Finder Platform

A modern job search and aggregation platform built with Flask and vanilla JavaScript. Search and filter jobs with a beautiful, responsive interface.

![Job Finder Platform](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![Status](https://img.shields.io/badge/Status-Ready-success)

## ✨ Features

- 🔍 **Smart Job Search** - Search by keywords, skills, company, or job title
- 📍 **Location Filtering** - Filter by city, state, or remote positions
- 🎯 **Advanced Filters** - Job type, experience level, salary range
- 📊 **Live Statistics** - Real-time stats on jobs, companies, and locations
- 💼 **Beautiful UI** - Modern gradient design with smooth animations
- 📱 **Fully Responsive** - Works perfectly on desktop, tablet, and mobile
- ⚡ **Fast & Lightweight** - No heavy frameworks, pure performance

## 🎬 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/dayyalabhanuprakash/job-search-platforms.git
cd job-search-platforms

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open browser to http://localhost:5000
```

## 🌐 Deploy to Render (Free)

### Quick Deploy

1. **Push to GitHub** (if not done)
   ```bash
   ./deploy_to_render.sh
   ```

2. **Go to Render**
   - Visit [render.com](https://render.com)
   - Sign in with GitHub
   - Click "New +" → "Web Service"
   - Select this repository
   - Click "Create Web Service"

3. **Done!** 🎉
   - Your live URL: `https://your-app-name.onrender.com`
   - Deployment time: ~3 minutes

### Manual Deploy

See detailed instructions in [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md)

## 📂 Project Structure

```
job-search-platforms/
├── app.py                          # Flask backend API
├── job_aggregator.py               # Job search logic
├── requirements.txt                # Python dependencies
├── Procfile                        # Gunicorn config
├── render.yaml                     # Render deployment config
├── runtime.txt                     # Python version
├── static/
│   ├── jobs.html                   # Main frontend page
│   ├── jobs.css                    # Styling
│   └── jobs.js                     # JavaScript logic
└── DEPLOYMENT_INSTRUCTIONS.md      # Full deployment guide
```

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- Flask 3.1 - Web framework
- Gunicorn - Production server
- Flask-CORS - Cross-origin support

**Frontend:**
- HTML5
- CSS3 with modern gradients
- Vanilla JavaScript (ES6+)
- Font Awesome icons

**Deployment:**
- Render.com (Platform)
- Gunicorn (WSGI server)
- GitHub (Version control)

## 🎯 API Endpoints

```
GET  /                          # Main application page
GET  /dashboard                 # Dashboard (alias)
GET  /health                    # Health check
GET  /api/jobs                  # Get jobs with filters
GET  /api/jobs/:id              # Get specific job
GET  /api/statistics            # Get job statistics
```

### Example API Calls

```bash
# Get all jobs
curl https://your-app.onrender.com/api/jobs

# Search for Python jobs
curl "https://your-app.onrender.com/api/jobs?query=python"

# Filter remote jobs
curl "https://your-app.onrender.com/api/jobs?remote=true"

# Get statistics
curl https://your-app.onrender.com/api/statistics
```

## 📊 Query Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `query` | string | Search keywords | `python`, `developer` |
| `location` | string | Job location | `New York`, `Remote` |
| `remote` | boolean | Remote jobs only | `true`, `false` |
| `job_type` | string | Type of job | `full-time`, `part-time` |
| `experience_level` | string | Experience required | `entry-level`, `senior` |
| `page` | integer | Page number | `1`, `2`, `3` |
| `per_page` | integer | Results per page | `10`, `20`, `50` |

## 🔄 Adding Real Job Data

Currently uses sample data. To add real jobs, update `job_aggregator.py`:

**Popular Job APIs:**
- Indeed API
- LinkedIn Jobs API
- GitHub Jobs
- RemoteOK API
- Adzuna API

```python
# Example: Add real API integration
def fetch_jobs_from_api(self, query):
    response = requests.get(f"https://api.example.com/jobs?q={query}")
    return response.json()
```

## 🐛 Troubleshooting

### Local Issues

**Port already in use:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Deployment Issues

**Build fails on Render:**
- Check Python version in `runtime.txt`
- Verify all dependencies in `requirements.txt`
- Review build logs in Render dashboard

**Site not loading:**
- Wait 30 seconds (cold start on free tier)
- Check `/health` endpoint
- Review Render logs

## 📈 Performance

- **First Load**: ~30s (cold start on free tier)
- **Subsequent Loads**: <1s
- **API Response**: <100ms
- **Bundle Size**: <50KB (no frameworks)

## 🎨 Customization

### Change Colors

Edit `static/jobs.css`:
```css
/* Update gradient colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Add More Jobs

Edit `job_aggregator.py`:
```python
# Add to sample_jobs list in _get_sample_jobs()
```

### Modify Layout

Edit `static/jobs.html` and update classes in `jobs.css`

## 📝 License

MIT License - Feel free to use for personal or commercial projects

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

- 📧 Email: dayyalabhanuprakash@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/dayyalabhanuprakash/job-search-platforms/issues)
- 📖 Docs: See [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md)

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ by Bhanu Prakash**

🚀 **Live Demo**: [Coming soon - Deploy yours now!](https://render.com)
