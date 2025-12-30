"""
Job API Integrations - Use public APIs and aggregators
"""
import requests
from datetime import datetime, timedelta
import json

class JobAPIIntegrations:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_adzuna(self, query="software engineer", location="", max_results=50):
        """
        Adzuna Job Search API - Free tier available
        Public job board aggregator
        """
        jobs = []
        try:
            # Adzuna public API (requires app_id and app_key for production)
            # For demo, we'll use their public endpoint
            base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
            
            params = {
                'what': query,
                'where': location,
                'results_per_page': min(max_results, 50),
                'content-type': 'application/json'
            }
            
            print(f"Fetching jobs from Adzuna API...")
            # Note: Real implementation needs API keys
            # response = requests.get(base_url, params=params, headers=self.headers, timeout=10)
            
            print(f"ℹ️  Adzuna requires API keys for production use")
            
        except Exception as e:
            print(f"✗ Error with Adzuna: {e}")
        
        return jobs
    
    def search_usajobs_gov(self, query="software engineer", location="", max_results=50):
        """
        USAJobs.gov API - Government jobs (Free, no key needed for basic search)
        """
        jobs = []
        try:
            base_url = "https://data.usajobs.gov/api/search"
            
            headers = {
                'User-Agent': 'jobfinder@example.com',
                'Authorization-Key': 'YOUR_API_KEY_HERE'  # Free to get
            }
            
            params = {
                'Keyword': query,
                'LocationName': location,
                'ResultsPerPage': min(max_results, 100)
            }
            
            print(f"Fetching jobs from USAJobs.gov...")
            # Note: Requires free API key registration
            
        except Exception as e:
            print(f"✗ Error with USAJobs: {e}")
        
        return jobs
    
    def search_github_jobs(self, query="software engineer", location="", max_results=50):
        """
        GitHub Jobs API alternative - Remote jobs
        """
        jobs = []
        try:
            # GitHub Jobs was deprecated, but we can use alternatives
            # like RemoteOK, We Work Remotely APIs
            print(f"ℹ️  GitHub Jobs API has been deprecated")
            
        except Exception as e:
            print(f"✗ Error: {e}")
        
        return jobs
    
    def search_remoteok(self, query="software engineer", max_results=50):
        """
        RemoteOK API - Remote jobs (public API)
        """
        jobs = []
        try:
            base_url = "https://remoteok.com/api"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            
            print(f"Fetching remote jobs from RemoteOK...")
            response = requests.get(base_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    # First item is metadata, skip it
                    job_listings = data[1:] if len(data) > 1 else []
                    
                    query_lower = query.lower()
                    
                    for job_data in job_listings:
                        if isinstance(job_data, dict):
                            # Filter by query
                            title = str(job_data.get('position', ''))
                            company = str(job_data.get('company', ''))
                            tags = job_data.get('tags', [])
                            tags_str = ' '.join([str(t) for t in tags]) if tags else ''
                            
                            # More flexible matching
                            if (query_lower in title.lower() or 
                                query_lower in company.lower() or
                                query_lower in tags_str.lower() or
                                any(word in tags_str.lower() for word in query_lower.split())):
                                
                                job = {
                                    'title': title,
                                    'company': company,
                                    'location': 'Remote',
                                    'source': 'RemoteOK',
                                    'posted_date': datetime.now().strftime('%Y-%m-%d'),
                                    'url': job_data.get('url', f"https://remoteok.com/l/{job_data.get('id', '')}")
                                }
                                jobs.append(job)
                                
                                if len(jobs) >= max_results:
                                    break
                    
                    print(f"✓ Found {len(jobs)} jobs from RemoteOK")
                except json.JSONDecodeError as e:
                    print(f"✗ RemoteOK JSON decode error: {e}")
            else:
                print(f"✗ RemoteOK returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"✗ Error scraping RemoteOK: {e}")
        
        return jobs
    
    def search_arbeitnow(self, query="software engineer", max_results=50):
        """
        Arbeitnow API - European tech jobs (Free public API)
        """
        jobs = []
        try:
            base_url = "https://www.arbeitnow.com/api/job-board-api"
            
            print(f"Fetching jobs from Arbeitnow...")
            response = requests.get(base_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                job_listings = data.get('data', [])
                
                for job_data in job_listings[:max_results]:
                    title = job_data.get('title', '')
                    company = job_data.get('company_name', '')
                    
                    if query.lower() in title.lower() or query.lower() in company.lower():
                        job = {
                            'title': title,
                            'company': company,
                            'location': job_data.get('location', 'Remote'),
                            'source': 'Arbeitnow',
                            'posted_date': job_data.get('created_at', datetime.now().strftime('%Y-%m-%d')),
                            'url': job_data.get('url', '#')
                        }
                        jobs.append(job)
                
                print(f"✓ Found {len(jobs)} jobs from Arbeitnow")
            else:
                print(f"✗ Arbeitnow returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"✗ Error with Arbeitnow: {e}")
        
        return jobs
    
    def search_findwork(self, query="software engineer", max_results=50):
        """
        Findwork API - Tech jobs aggregator
        """
        jobs = []
        try:
            base_url = "https://findwork.dev/api/jobs/"
            
            print(f"Fetching jobs from Findwork.dev...")
            response = requests.get(base_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                job_listings = data.get('results', [])
                
                for job_data in job_listings[:max_results]:
                    title = job_data.get('role', '')
                    company = job_data.get('company_name', '')
                    
                    if query.lower() in title.lower() or query.lower() in company.lower():
                        job = {
                            'title': title,
                            'company': company,
                            'location': job_data.get('location', 'Not specified'),
                            'source': 'Findwork',
                            'posted_date': job_data.get('date_posted', datetime.now().strftime('%Y-%m-%d')),
                            'url': job_data.get('url', '#')
                        }
                        jobs.append(job)
                
                print(f"✓ Found {len(jobs)} jobs from Findwork")
            else:
                print(f"✗ Findwork returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"✗ Error with Findwork: {e}")
        
        return jobs
    
    def aggregate_from_apis(self, query="software engineer", location=""):
        """
        Aggregate jobs from multiple free APIs
        """
        print(f"\n{'='*60}")
        print(f"AGGREGATING JOBS FROM PUBLIC APIs")
        print(f"Query: {query} | Location: {location or 'Any'}")
        print(f"{'='*60}\n")
        
        all_jobs = []
        
        # Use free public APIs that don't require authentication
        all_jobs.extend(self.search_remoteok(query, max_results=50))
        all_jobs.extend(self.search_arbeitnow(query, max_results=50))
        all_jobs.extend(self.search_findwork(query, max_results=50))
        
        print(f"\n{'='*60}")
        print(f"✓ TOTAL REAL JOBS FROM APIs: {len(all_jobs)}")
        print(f"{'='*60}\n")
        
        return all_jobs
