"""
Job Scrapers - Fetch real jobs from multiple job portals
"""
import requests
from bs4 import BeautifulSoup
import cloudscraper
from fake_useragent import UserAgent
from datetime import datetime, timedelta
import time
import json
import re

class JobScrapers:
    def __init__(self):
        self.ua = UserAgent()
        self.scraper = cloudscraper.create_scraper()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def scrape_indeed(self, query="software engineer", location="", max_results=50):
        """Scrape jobs from Indeed"""
        jobs = []
        try:
            # Indeed URL format
            base_url = "https://www.indeed.com/jobs"
            params = {
                'q': query,
                'l': location,
                'fromage': '2',  # Last 2 days
                'limit': 50
            }
            
            print(f"Fetching Indeed jobs for: {query} in {location or 'Any Location'}")
            response = self.scraper.get(base_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards (Indeed's structure)
                job_cards = soup.find_all('div', class_=re.compile('job_seen_beacon|jobsearch-SerpJobCard'))
                
                for card in job_cards[:max_results]:
                    try:
                        title_elem = card.find('h2', class_='jobTitle') or card.find('a', class_='jcs-JobTitle')
                        company_elem = card.find('span', class_='companyName')
                        location_elem = card.find('div', class_='companyLocation')
                        
                        if title_elem and company_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True),
                                'location': location_elem.get_text(strip=True) if location_elem else 'Not specified',
                                'source': 'Indeed',
                                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                                'url': 'https://www.indeed.com' + title_elem.find('a')['href'] if title_elem.find('a') else '#'
                            }
                            jobs.append(job)
                    except Exception as e:
                        continue
                
                print(f"✓ Found {len(jobs)} jobs from Indeed")
            else:
                print(f"✗ Indeed returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"✗ Error scraping Indeed: {e}")
        
        return jobs
    
    def scrape_dice(self, query="software engineer", location="", max_results=50):
        """Scrape jobs from Dice"""
        jobs = []
        try:
            # Dice API endpoint
            base_url = "https://www.dice.com/jobs"
            params = {
                'q': query,
                'location': location,
                'radius': '30',
                'radiusUnit': 'mi',
                'page': '1',
                'pageSize': '50'
            }
            
            print(f"Fetching Dice jobs for: {query}")
            response = self.scraper.get(base_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('div', {'data-cy': 'card'}) or soup.find_all('div', class_=re.compile('card'))
                
                for card in job_cards[:max_results]:
                    try:
                        title_elem = card.find('a', {'data-cy': 'card-title-link'}) or card.find('h5')
                        company_elem = card.find('a', {'data-cy': 'card-company'}) or card.find('span', class_='company')
                        location_elem = card.find('span', {'data-cy': 'card-location'})
                        
                        if title_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True) if company_elem else 'Company not listed',
                                'location': location_elem.get_text(strip=True) if location_elem else 'Remote',
                                'source': 'Dice',
                                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                                'url': title_elem['href'] if title_elem.get('href') else '#'
                            }
                            jobs.append(job)
                    except Exception as e:
                        continue
                
                print(f"✓ Found {len(jobs)} jobs from Dice")
            else:
                print(f"✗ Dice returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"✗ Error scraping Dice: {e}")
        
        return jobs
    
    def scrape_linkedin(self, query="software engineer", location="", max_results=25):
        """Scrape jobs from LinkedIn (limited due to auth requirements)"""
        jobs = []
        try:
            # LinkedIn jobs public search
            base_url = "https://www.linkedin.com/jobs/search"
            params = {
                'keywords': query,
                'location': location,
                'f_TPR': 'r86400',  # Last 24 hours
                'position': '1',
                'pageNum': '0'
            }
            
            print(f"Fetching LinkedIn jobs for: {query}")
            response = self.scraper.get(base_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('div', class_='base-card')
                
                for card in job_cards[:max_results]:
                    try:
                        title_elem = card.find('h3', class_='base-search-card__title')
                        company_elem = card.find('h4', class_='base-search-card__subtitle')
                        location_elem = card.find('span', class_='job-search-card__location')
                        link_elem = card.find('a', class_='base-card__full-link')
                        
                        if title_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True) if company_elem else 'Company not listed',
                                'location': location_elem.get_text(strip=True) if location_elem else 'Not specified',
                                'source': 'LinkedIn',
                                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                                'url': link_elem['href'] if link_elem and link_elem.get('href') else '#'
                            }
                            jobs.append(job)
                    except Exception as e:
                        continue
                
                print(f"✓ Found {len(jobs)} jobs from LinkedIn")
            else:
                print(f"✗ LinkedIn returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"✗ Error scraping LinkedIn: {e}")
        
        return jobs
    
    def scrape_glassdoor(self, query="software engineer", location="", max_results=30):
        """Scrape jobs from Glassdoor"""
        jobs = []
        try:
            # Glassdoor job search
            base_url = "https://www.glassdoor.com/Job/jobs.htm"
            params = {
                'sc.keyword': query,
                'locT': 'C',
                'locId': '1147401',  # Default to US
                'fromAge': '2'  # Last 2 days
            }
            
            print(f"Fetching Glassdoor jobs for: {query}")
            response = self.scraper.get(base_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job listings
                job_cards = soup.find_all('li', class_=re.compile('react-job-listing'))
                
                for card in job_cards[:max_results]:
                    try:
                        title_elem = card.find('a', class_='jobLink')
                        company_elem = card.find('div', class_='employerName')
                        location_elem = card.find('div', class_='location')
                        
                        if title_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True) if company_elem else 'Company not listed',
                                'location': location_elem.get_text(strip=True) if location_elem else 'Not specified',
                                'source': 'Glassdoor',
                                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                                'url': 'https://www.glassdoor.com' + title_elem['href'] if title_elem.get('href') else '#'
                            }
                            jobs.append(job)
                    except Exception as e:
                        continue
                
                print(f"✓ Found {len(jobs)} jobs from Glassdoor")
            else:
                print(f"✗ Glassdoor returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"✗ Error scraping Glassdoor: {e}")
        
        return jobs
    
    def aggregate_all_jobs(self, query="software engineer", location=""):
        """Aggregate jobs from all sources"""
        print(f"\n{'='*60}")
        print(f"AGGREGATING JOBS FROM MULTIPLE SOURCES")
        print(f"Query: {query} | Location: {location or 'Any'}")
        print(f"{'='*60}\n")
        
        all_jobs = []
        
        # Scrape from all sources
        all_jobs.extend(self.scrape_indeed(query, location, max_results=50))
        time.sleep(2)  # Polite delay
        
        all_jobs.extend(self.scrape_dice(query, location, max_results=50))
        time.sleep(2)
        
        all_jobs.extend(self.scrape_linkedin(query, location, max_results=25))
        time.sleep(2)
        
        all_jobs.extend(self.scrape_glassdoor(query, location, max_results=30))
        
        print(f"\n{'='*60}")
        print(f"✓ TOTAL JOBS AGGREGATED: {len(all_jobs)}")
        print(f"{'='*60}\n")
        
        return all_jobs
