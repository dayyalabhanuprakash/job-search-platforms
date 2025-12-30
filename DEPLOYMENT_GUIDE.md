# 🚀 Deploy Job Aggregator to Live Website

## Step-by-Step Guide to Deploy on Render (Free)

### Prerequisites
- GitHub account (free)
- Render account (free) - https://render.com

---

## STEP 1: Prepare Your Code for GitHub

### 1.1 Create .gitignore file (if not exists)
Already exists in your project. Contains:
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg-info/
dist/
build/
.env
.venv/
venv/
*.log
.DS_Store
```

### 1.2 Verify all necessary files are present
✅ app.py - Main Flask application
✅ requirements.txt - Python dependencies
✅ runtime.txt - Python version
✅ Procfile - Deployment configuration
✅ render.yaml - Render configuration
✅ static/ - Frontend files
✅ All job scraper files

---

## STEP 2: Initialize Git Repository

Open terminal in your project folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Job Aggregator with real-time scraping"
```

---

## STEP 3: Create GitHub Repository

### Option A: Using GitHub Website (Recommended)

1. **Go to GitHub:** https://github.com
2. **Sign in** to your account
3. **Click** the "+" icon (top right) → "New repository"
4. **Repository details:**
   - Repository name: `job-aggregator` (or your choice)
   - Description: "Job aggregator with real-time scraping from Indeed, LinkedIn, and more"
   - Visibility: **Public** (required for free Render hosting)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. **Click** "Create repository"

### Option B: Using GitHub CLI (if you have it)

```bash
gh repo create job-aggregator --public --source=. --remote=origin
```

---

## STEP 4: Push Code to GitHub

After creating the repository, GitHub will show you commands. Run these:

```bash
# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/job-aggregator.git

# Push code to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username!**

Example:
```bash
git remote add origin https://github.com/john123/job-aggregator.git
git branch -M main
git push -u origin main
```

---

## STEP 5: Deploy to Render

### 5.1 Create Render Account

1. **Go to:** https://render.com
2. **Click** "Get Started" or "Sign Up"
3. **Sign up** with your GitHub account (easiest)
4. **Authorize** Render to access your GitHub

### 5.2 Create New Web Service

1. **Click** "New +" → "Web Service"
2. **Connect your repository:**
   - Click "Connect repository"
   - Find and select: `job-aggregator`
   - Click "Connect"

### 5.3 Configure Web Service

Fill in the deployment settings:

**Basic Settings:**
- **Name:** `job-aggregator` (or your choice)
  - This will be your URL: `job-aggregator.onrender.com`
- **Region:** Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch:** `main`
- **Root Directory:** Leave blank
- **Runtime:** `Python 3`

**Build Settings:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

**Plan:**
- **Instance Type:** `Free` (select Free tier)
  - Note: Free tier sleeps after 15 min of inactivity
  - Wakes up automatically when accessed (takes 30 seconds)

### 5.4 Environment Variables (Optional)

If you want to add any API keys later, you can add them in:
- "Environment" section
- Add key-value pairs
- Example: `API_KEY=your_key_here`

### 5.5 Deploy!

1. **Click** "Create Web Service"
2. **Wait** 5-10 minutes for deployment
3. **Watch** the logs in real-time
4. **Success!** You'll see "Your service is live" ✅

---

## STEP 6: Access Your Live Website

### Your URL will be:
```
https://job-aggregator.onrender.com
```
(Replace `job-aggregator` with whatever name you chose)

### Test it:
1. Open the URL in your browser
2. Search for "Data Engineer"
3. Try all features!

---

## 🎯 Quick Reference Commands

### Initial Setup (run once):
```bash
cd /path/to/your/project
git init
git add .
git commit -m "Initial commit - Job Aggregator"
git remote add origin https://github.com/YOUR_USERNAME/job-aggregator.git
git branch -M main
git push -u origin main
```

### Making Updates Later:
```bash
git add .
git commit -m "Description of changes"
git push
```
*Render will automatically redeploy when you push to GitHub!*

---

## 🔧 Troubleshooting

### Problem: Git not installed
**Solution:** Install Git
- Windows: https://git-scm.com/download/win
- Mac: `brew install git` or Xcode Command Line Tools
- Linux: `sudo apt install git` or `sudo yum install git`

### Problem: GitHub authentication failed
**Solution:** Use Personal Access Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Give it "repo" permissions
4. Use token as password when pushing

### Problem: Render deployment fails
**Solution:** Check logs
1. In Render dashboard, click your service
2. Go to "Logs" tab
3. Look for error messages
4. Common fixes:
   - Ensure `requirements.txt` is correct
   - Check `Procfile` exists
   - Verify Python version in `runtime.txt`

### Problem: Website is slow
**Solution:** Normal for free tier
- Free tier sleeps after 15 minutes
- First request after sleep takes 30-60 seconds
- Subsequent requests are fast
- Upgrade to paid tier ($7/month) for always-on service

### Problem: Real job scraping times out
**Solution:** 
- Render free tier has limited resources
- Use generated jobs by default (unchecked "Fetch Real Jobs")
- Real jobs work but may be slower on free tier

---

## 💰 Cost Information

### Render Free Tier:
- ✅ **Cost:** $0/month
- ✅ 750 hours/month (enough for 24/7)
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ Takes 30-60 sec to wake up
- ✅ Perfect for portfolio/demo projects

### Render Paid Tier (Optional):
- 💵 **Cost:** $7/month
- ✅ Always-on (no sleep)
- ✅ Faster performance
- ✅ More resources
- ✅ Better for production use

---

## 🎨 Customizing Your URL

### Free Option (Render subdomain):
- `your-app-name.onrender.com`
- Free and works immediately

### Custom Domain (Optional):
1. Buy domain (e.g., from Namecheap, GoDaddy)
2. In Render dashboard → Settings → Custom Domains
3. Add your domain
4. Update DNS records as instructed
5. Your site: `yourdomain.com`

---

## 📊 Monitoring Your App

### Render Dashboard shows:
- ✅ Deployment status
- ✅ Real-time logs
- ✅ Resource usage
- ✅ Request metrics
- ✅ Build history

### Access Dashboard:
1. Login to Render
2. Click your service name
3. View all metrics and logs

---

## 🔄 Updating Your Live Site

Whenever you make changes:

```bash
# 1. Make your changes in the code
# 2. Test locally (python3 app.py)
# 3. Commit and push to GitHub
git add .
git commit -m "Added new feature"
git push

# 4. Render automatically detects and redeploys!
# Wait 2-5 minutes for deployment
```

---

## ✅ Deployment Checklist

Before deploying, ensure:
- [ ] All files committed to Git
- [ ] `.gitignore` excludes sensitive files
- [ ] `requirements.txt` is up to date
- [ ] `Procfile` exists with correct command
- [ ] `runtime.txt` specifies Python version
- [ ] Code works locally (test thoroughly)
- [ ] No hardcoded localhost URLs
- [ ] Environment variables configured (if needed)

---

## 🎉 Success!

Once deployed, share your live URL:
```
https://your-app-name.onrender.com
```

Your job aggregator is now live and accessible worldwide! 🌍

---

## 📞 Need Help?

- **Render Docs:** https://render.com/docs
- **GitHub Docs:** https://docs.github.com
- **This Project:** Check IMPLEMENTATION_SUMMARY.md

---

**Good luck with your deployment! 🚀**
