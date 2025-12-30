# 🎯 Job Aggregator - User Guide

## 🚀 Quick Start

### Starting the Application
```bash
python3 app.py
```

Then open: **http://localhost:5000**

---

## 📋 Two Ways to Search

### 1. 🔥 **REAL JOBS MODE** (Recommended)

**What it does:**
- Fetches real jobs from Indeed & LinkedIn
- Uses 3 related search terms automatically
- Shows fresh jobs from last 24-48 hours

**How to use:**
1. ✅ Check the box: **"Fetch Real Jobs"**
2. Type: **"Data Engineer"** (or any job title)
3. Location: **"Remote"** or **"United States"**
4. Time filter: **"Last 48 hours"**
5. Click: **"Search Jobs"**
6. ⏱️ Wait: **15-30 seconds**

**What to expect:**
- Loading message: "Fetching real jobs from Indeed & LinkedIn..."
- After 15-30 seconds: Real job listings appear
- Each job shows: Indeed or LinkedIn as source
- If < 20 real jobs found, generated jobs added automatically

**Example Search:**
```
Search: "Data Engineer"
Location: "Remote"
Time: "Last 48 hours"
Result: 50-100+ real jobs
```

---

### 2. ⚡ **GENERATED JOBS MODE** (Instant)

**What it does:**
- Shows pre-generated sample jobs instantly
- No waiting time
- Good for testing filters and UI

**How to use:**
1. ❌ Uncheck: **"Fetch Real Jobs"**
2. Type any search term
3. Click: **"Search Jobs"**
4. Results appear instantly!

**When to use:**
- Testing the interface
- Exploring filters quickly
- When real job search times out
- Practice interviews or applications

---

## 🎨 Features

### Search Terms Auto-Expansion

When you search for **"Data Engineer"**, the system automatically searches:
- Data Engineer
- Big Data Engineer
- ETL Engineer
- (And more related terms!)

This gives you **3x more results** than a single search!

### Time Filters

- **🔥 Last 24 hours** - Ultra fresh jobs
- **⚡ Last 48 hours** - Very recent (recommended)
- Last 3 days
- Last 7 days
- Last 14 days
- Last 30 days
- Any time

### Other Filters

- **Remote Jobs** - Check for remote only
- **Job Type** - Full-time, Part-time, Contract, Internship
- **Experience Level** - Entry, Mid, Senior
- **Location** - Any location

### Job Details Shown

Each job card displays:
- ✅ Job Title
- ✅ Company Name
- ✅ Location
- ✅ Remote/Hybrid/On-site badge
- ✅ Salary (if available)
- ✅ Skills Required
- ✅ Posted Date
- ✅ Source (Indeed, LinkedIn, or Generated)
- ✅ Apply Now button

---

## 🆘 Troubleshooting

### "Failed to load jobs" Error

**Solution 1: Use Generated Jobs**
- Uncheck "Fetch Real Jobs"
- Click Search
- Results appear instantly

**Solution 2: Wait and Retry**
- Real job scraping can take 15-30 seconds
- If it fails, wait a moment and click "Try Again"

**Solution 3: Check Your Query**
- Try simpler search terms: "Data Engineer" instead of complex phrases
- Try "Remote" or "United States" as location

### "Request timed out" Error

**What happened:**
- Search took longer than 60 seconds
- Job sites may be slow or blocking requests

**Solutions:**
1. Uncheck "Fetch Real Jobs" for instant results
2. Try again in a few minutes
3. Try a different search term
4. Check your internet connection

### Getting Zero Results

**For Real Jobs:**
- First search on a query may return fewer results
- Try broader search terms
- Try "Remote" as location
- System will add generated jobs if < 20 real jobs found

**For Generated Jobs:**
- Should never get zero results
- Check if filters are too restrictive

---

## 💡 Pro Tips

### Best Search Practices

1. **Be Specific but Not Too Specific**
   - ✅ Good: "Data Engineer"
   - ❌ Too specific: "Senior Big Data Engineer with Spark and Kafka"

2. **Use Remote for More Results**
   - Remote jobs have broader reach
   - More opportunities available

3. **Use 48-hour Filter**
   - Fresh enough for recent jobs
   - Not too restrictive

4. **Let Cache Work for You**
   - Same search within 1 hour = instant results
   - No need to wait again!

### Understanding Job Sources

**Indeed Jobs:**
- Large job board
- Many listings
- Good variety

**LinkedIn Jobs:**
- Professional network
- Quality listings
- Company insights

**Generated Jobs:**
- Sample data for testing
- Marked as "Generated"
- Good for exploring the interface

---

## 📊 Performance Guide

### Expected Speed

| Mode | First Search | Cached Search |
|------|-------------|---------------|
| Real Jobs | 15-30 sec | <1 sec |
| Generated | <1 sec | <1 sec |

### Cache Duration
- **1 hour** per unique query
- Same query + location + time filter = cached
- After 1 hour, fresh scraping happens

### Results Count

**Real Jobs Mode:**
- 3 search terms × 50 results = ~150 raw jobs
- After deduplication: 50-100 unique jobs
- If < 20 real jobs: Generated jobs added

**Generated Jobs Mode:**
- ~9000 pre-generated jobs available
- Filtered based on your search

---

## 🎓 Example Workflows

### Job Hunting - Fresh Opportunities
```
1. Check "Fetch Real Jobs" ✅
2. Search: "Data Engineer"
3. Location: "Remote"
4. Filter: "Last 24 hours"
5. Wait 15-30 seconds
6. Browse fresh real jobs!
7. Click "Apply Now" on interesting ones
```

### Quick Browse - Exploring Options
```
1. Uncheck "Fetch Real Jobs" ❌
2. Search: "Software Engineer"
3. No location filter
4. Results appear instantly
5. Use filters to narrow down
6. Get ideas for your search
```

### Targeted Search - Specific Role
```
1. Check "Fetch Real Jobs" ✅
2. Search: "Machine Learning Engineer"
3. Location: "San Francisco"
4. Filter: "Last 48 hours"
5. Experience: "Senior"
6. Job Type: "Full-time"
7. Wait for results
8. Apply to best matches!
```

---

## 📞 Support

### Common Questions

**Q: Why is real job search slow?**
A: It's scraping live data from Indeed & LinkedIn. This takes 15-30 seconds but ensures fresh results!

**Q: Can I make it faster?**
A: Use generated jobs mode for instant results, or wait for cache (1 hour).

**Q: Are generated jobs real?**
A: No, they're sample data. Look for "Indeed" or "LinkedIn" as source for real jobs.

**Q: How often should I search?**
A: New jobs are posted hourly. Use 24-hour filter and check a few times per day.

**Q: What if I get too few results?**
A: System automatically adds generated jobs if < 20 real jobs found. You'll always have plenty to browse!

---

## 🎉 Success Tips

1. **Be Patient on First Search**
   - 15-30 seconds is normal
   - You're getting REAL jobs
   - Worth the wait!

2. **Use the Right Mode**
   - Job hunting → Real Jobs
   - Quick browsing → Generated

3. **Leverage Filters**
   - Start broad
   - Narrow with filters
   - Find perfect matches

4. **Check Multiple Times Daily**
   - New jobs posted constantly
   - 24-hour filter shows latest
   - Early applicants have advantage

5. **Apply Quickly**
   - Fresh jobs (< 24 hours) get more responses
   - Look for 🔥 Fresh badge
   - Apply same day!

---

**Happy Job Hunting! 🚀**

For technical details, see `IMPLEMENTATION_SUMMARY.md`
