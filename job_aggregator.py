"""
Job Aggregator - Fetches jobs from multiple sources
"""
import requests
from datetime import datetime, timedelta
import json
from job_data_generator import JobDataGenerator
from job_scrapers import JobScrapers
from job_api_integrations import JobAPIIntegrations
from job_scraper_enhanced import EnhancedJobScraper

class JobAggregator:
    def __init__(self):
        self.jobs_cache = []
        self.last_fetch = None
        self.job_generator = JobDataGenerator()
        self.job_scrapers = JobScrapers()
        self.job_api = JobAPIIntegrations()
        self.enhanced_scraper = EnhancedJobScraper()
        # Generate large dataset on initialization
        self.all_jobs = self.job_generator.generate_jobs(count=8961)  # Generate 8961 jobs
        self.real_jobs_cache = {}  # Cache by query
        self.real_jobs_last_fetch = {}  # Track last fetch by query
        self.cache_duration = 3600  # Cache for 1 hour (balance between freshness and speed)
        
    def get_jobs(self, query='', location='', remote=False, job_type='all', 
                 experience_level='all', salary_min=0, date_posted='all', 
                 posted_after='', company='', page=1, per_page=20, use_real_jobs=False):
        """
        Fetch jobs from multiple sources
        """
        try:
            # Get hours_old from date_posted filter
            hours_old = 48  # Default to 48 hours
            if date_posted and date_posted != 'all':
                try:
                    hours_old = int(date_posted)
                except:
                    hours_old = 48
            
            # Get all jobs (real or generated)
            if use_real_jobs:
                jobs = self._get_real_jobs(query, location, hours_old)
            else:
                jobs = self._get_sample_jobs()
            
            # Apply filters
            filtered_jobs = self._apply_filters(
                jobs, query, location, remote, job_type, 
                experience_level, salary_min, date_posted, company
            )
            
            # Pagination
            start = (page - 1) * per_page
            end = start + per_page
            paginated_jobs = filtered_jobs[start:end]
            
            return {
                'jobs': paginated_jobs,
                'total': len(filtered_jobs),
                'page': page,
                'per_page': per_page,
                'total_pages': (len(filtered_jobs) + per_page - 1) // per_page
            }
        except Exception as e:
            print(f"Error in get_jobs: {e}")
            import traceback
            traceback.print_exc()
            return {
                'jobs': [],
                'total': 0,
                'page': page,
                'per_page': per_page,
                'total_pages': 0,
                'error': str(e)
            }
    
    def _get_sample_jobs(self):
        """Get jobs from generated dataset"""
        # Return the pre-generated jobs
        return self.all_jobs
        
    def _get_original_sample_jobs(self):
        """Original sample jobs - kept for reference"""
        sample_jobs = [
            {
                'id': 'job-1',
                'title': 'Senior Python Developer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'remote': True,
                'salary': '$120k - $160k',
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'posted_date': '2025-12-27',
                'description': 'We are looking for an experienced Python developer to join our team. Work on cutting-edge projects with modern technologies.',
                'skills': ['Python', 'Flask', 'Django', 'AWS', 'Docker'],
                'url': '/apply/job-1'
            },
            {
                'id': 'job-2',
                'title': 'Frontend Engineer',
                'company': 'StartupXYZ',
                'location': 'New York, NY',
                'remote': False,
                'salary': '$100k - $140k',
                'job_type': 'Full-time',
                'experience_level': 'Mid-level',
                'posted_date': '2025-12-28',
                'description': 'Join our frontend team to build amazing user experiences. React, TypeScript, and modern web technologies.',
                'skills': ['React', 'TypeScript', 'CSS', 'JavaScript', 'Redux'],
                'url': '/apply/job-2'
            },
            {
                'id': 'job-3',
                'title': 'Full Stack Developer',
                'company': 'Digital Solutions Inc',
                'location': 'Remote',
                'remote': True,
                'salary': '$110k - $150k',
                'job_type': 'Full-time',
                'experience_level': 'Mid-level',
                'posted_date': '2025-12-26',
                'description': 'Looking for a full stack developer comfortable with both frontend and backend development.',
                'skills': ['JavaScript', 'Node.js', 'React', 'MongoDB', 'Express'],
                'url': '/apply/job-3'
            },
            {
                'id': 'job-4',
                'title': 'Data Engineer',
                'company': 'Data Analytics Pro',
                'location': 'Austin, TX',
                'remote': True,
                'salary': '$130k - $170k',
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'posted_date': '2025-12-29',
                'description': 'Build and maintain data pipelines. Work with big data technologies and cloud platforms.',
                'skills': ['Python', 'SQL', 'Spark', 'Airflow', 'AWS'],
                'url': '/apply/job-4'
            },
            {
                'id': 'job-5',
                'title': 'DevOps Engineer',
                'company': 'Cloud Systems',
                'location': 'Seattle, WA',
                'remote': False,
                'salary': '$125k - $165k',
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'posted_date': '2025-12-25',
                'description': 'Manage cloud infrastructure and CI/CD pipelines. Experience with Kubernetes required.',
                'skills': ['Kubernetes', 'Docker', 'AWS', 'Terraform', 'Jenkins'],
                'url': '/apply/job-5'
            },
            {
                'id': 'job-6',
                'title': 'Junior Web Developer',
                'company': 'WebDev Studio',
                'location': 'Chicago, IL',
                'remote': True,
                'salary': '$60k - $80k',
                'job_type': 'Full-time',
                'experience_level': 'Entry-level',
                'posted_date': '2025-12-28',
                'description': 'Great opportunity for recent graduates. Learn from experienced developers.',
                'skills': ['HTML', 'CSS', 'JavaScript', 'Git', 'React'],
                'url': '/apply/job-6'
            },
            {
                'id': 'job-7',
                'title': 'Mobile App Developer',
                'company': 'AppMakers',
                'location': 'Los Angeles, CA',
                'remote': False,
                'salary': '$105k - $145k',
                'job_type': 'Full-time',
                'experience_level': 'Mid-level',
                'posted_date': '2025-12-27',
                'description': 'Develop iOS and Android applications using React Native.',
                'skills': ['React Native', 'JavaScript', 'iOS', 'Android', 'Firebase'],
                'url': '/apply/job-7'
            },
            {
                'id': 'job-8',
                'title': 'Machine Learning Engineer',
                'company': 'AI Innovations',
                'location': 'Boston, MA',
                'remote': True,
                'salary': '$140k - $180k',
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'posted_date': '2025-12-29',
                'description': 'Build and deploy ML models. Work with cutting-edge AI technologies.',
                'skills': ['Python', 'TensorFlow', 'PyTorch', 'ML', 'Deep Learning'],
                'url': '/apply/job-8'
            },
            # Jobs from reputed companies
            {
                'id': 'job-9',
                'title': 'Quantitative Trader',
                'company': 'Jane Street',
                'location': 'New York, NY',
                'remote': False,
                'salary': '$150k - $250k',
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'posted_date': '2025-12-29',
                'description': 'Join our trading team to develop and implement quantitative trading strategies.',
                'skills': ['Python', 'C++', 'Statistics', 'Machine Learning', 'Trading'],
                'url': '/apply/job-9',
                'reputed': True
            },
            {
                'id': 'job-10',
                'title': 'Software Engineer - Trading Systems',
                'company': 'Citadel Securities',
                'location': 'Chicago, IL',
                'remote': False,
                'salary': '$180k - $280k',
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'posted_date': '2025-12-29',
                'description': 'Build high-performance trading systems. Work with cutting-edge technology.',
                'skills': ['C++', 'Python', 'Low Latency', 'Distributed Systems', 'Trading'],
                'url': '/apply/job-10',
                'reputed': True
            },
            {
                'id': 'job-11',
                'title': 'Quantitative Researcher',
                'company': 'Two Sigma',
                'location': 'New York, NY',
                'remote': True,
                'salary': '$200k - $350k',
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'posted_date': '2025-12-29',
                'description': 'Develop predictive models and trading strategies using machine learning.',
                'skills': ['Python', 'R', 'Machine Learning', 'Statistics', 'Data Science'],
                'url': '/apply/job-11',
                'reputed': True
            },
            {
                'id': 'job-12',
                'title': 'Investment Banking Analyst',
                'company': 'Goldman Sachs',
                'location': 'New York, NY',
                'remote': False,
                'salary': '$100k - $150k',
                'job_type': 'Full-time',
                'experience_level': 'Entry-level',
                'posted_date': '2025-12-28',
                'description': 'Join our investment banking division. Work on M&A, IPOs, and strategic advisory.',
                'skills': ['Finance', 'Excel', 'Financial Modeling', 'PowerPoint', 'Analysis'],
                'url': '/apply/job-12',
                'reputed': True
            },
            {
                'id': 'job-13',
                'title': 'Software Developer - Portfolio Management',
                'company': 'BlackRock',
                'location': 'San Francisco, CA',
                'remote': True,
                'salary': '$130k - $180k',
                'job_type': 'Full-time',
                'experience_level': 'Mid-level',
                'posted_date': '2025-12-28',
                'description': 'Build portfolio management tools and analytics platforms.',
                'skills': ['Java', 'Python', 'SQL', 'AWS', 'Financial Systems'],
                'url': '/apply/job-13',
                'reputed': True
            },
            {
                'id': 'job-14',
                'title': 'Algorithmic Trader',
                'company': 'Hudson River Trading',
                'location': 'New York, NY',
                'remote': False,
                'salary': '$175k - $300k',
                'job_type': 'Full-time',
                'experience_level': 'Senior',
                'posted_date': '2025-12-29',
                'description': 'Design and implement automated trading algorithms for global markets.',
                'skills': ['Python', 'C++', 'Trading', 'Algorithms', 'Data Analysis'],
                'url': '/apply/job-14',
                'reputed': True
            },
            {
                'id': 'job-15',
                'title': 'Quantitative Developer',
                'company': 'Optiver',
                'location': 'Amsterdam, Netherlands',
                'remote': False,
                'salary': '€120k - €200k',
                'job_type': 'Full-time',
                'experience_level': 'Mid-level',
                'posted_date': '2025-12-28',
                'description': 'Develop trading systems and tools for our market-making operations.',
                'skills': ['C++', 'Python', 'Low Latency', 'Trading', 'Linux'],
                'url': '/apply/job-15',
                'reputed': True
            },
            {
                'id': 'job-16',
                'title': 'Data Scientist - Investments',
                'company': 'Vanguard',
                'location': 'Malvern, PA',
                'remote': True,
                'salary': '$110k - $150k',
                'job_type': 'Full-time',
                'experience_level': 'Mid-level',
                'posted_date': '2025-12-27',
                'description': 'Apply data science to investment research and portfolio optimization.',
                'skills': ['Python', 'R', 'Machine Learning', 'SQL', 'Statistics'],
                'url': '/apply/job-16',
                'reputed': True
            }
        ]
        
        return sample_jobs
    
    def _apply_filters(self, jobs, query, location, remote, job_type, 
                      experience_level, salary_min, date_posted, company=''):
        """Apply filters to job list"""
        filtered = jobs
        
        # Date posted filter (hours ago)
        if date_posted and date_posted != 'all':
            try:
                hours_limit = int(date_posted)
                now = datetime.now()
                temp_filtered = []
                for job in filtered:
                    job_date = datetime.strptime(job['posted_date'], '%Y-%m-%d')
                    hours_ago = (now - job_date).total_seconds() / 3600
                    if hours_ago <= hours_limit:
                        temp_filtered.append(job)
                filtered = temp_filtered
            except (ValueError, KeyError) as e:
                print(f"Date filter error: {e}")
                pass  # If parsing fails, skip this filter
        
        # Query filter (search in title, company, description)
        if query:
            query = query.lower()
            filtered = [j for j in filtered if 
                       query in j['title'].lower() or 
                       query in j['company'].lower() or 
                       query in j['description'].lower() or
                       any(query in skill.lower() for skill in j['skills'])]
        
        # Location filter
        if location:
            location = location.lower()
            filtered = [j for j in filtered if location in j['location'].lower()]
        
        # Remote filter
        if remote:
            filtered = [j for j in filtered if j['remote']]
        
        # Job type filter
        if job_type and job_type != 'all':
            filtered = [j for j in filtered if j['job_type'].lower() == job_type.lower()]
        
        # Experience level filter
        if experience_level and experience_level != 'all':
            filtered = [j for j in filtered if j['experience_level'].lower() == experience_level.lower()]

        # Company filter
        if company and company != 'all':
            try:
                comp_lower = company.lower()
                filtered = [j for j in filtered if 'company' in j and j['company'].lower() == comp_lower]
            except Exception as e:
                print(f"Company filter error: {e}")
                pass
        
        return filtered
    
    def _get_real_jobs(self, query, location='', hours_old=48):
        """Fetch real jobs from job portals using enhanced scraper"""
        # Check cache
        now = datetime.now()
        cache_key = f"{query}_{location}_{hours_old}"
        
        if cache_key in self.real_jobs_cache and cache_key in self.real_jobs_last_fetch:
            time_diff = (now - self.real_jobs_last_fetch[cache_key]).seconds
            if time_diff < self.cache_duration:
                print(f"✓ Using cached real jobs ({len(self.real_jobs_cache[cache_key])} jobs, cached {time_diff}s ago)")
                return self.real_jobs_cache[cache_key]
        
        # Determine search terms based on query (limit to top 3 for speed)
        all_search_terms = self._expand_search_terms(query)
        search_terms = all_search_terms[:3]  # Use only top 3 terms
        
        # Determine locations (limit to 1 for speed)
        if location and location.lower() != 'all':
            locations = [location]
        else:
            locations = ['United States']  # Single location for faster results
        
        # Fetch new jobs using enhanced scraper
        print(f"🔍 Fetching real jobs from Indeed, LinkedIn, ZipRecruiter...")
        print(f"   Search terms: {search_terms} (using top 3 for speed)")
        print(f"   Locations: {locations}")
        print(f"   Hours old: {hours_old}")
        
        try:
            # Use enhanced scraper with faster settings
            raw_jobs = self.enhanced_scraper.scrape_jobs_multi_term(
                search_terms=search_terms,
                locations=locations,
                sites=['indeed', 'linkedin'],  # Use 2 fastest sites
                results_wanted=50,  # Get more results
                hours_old=hours_old,
                job_type='fulltime',
                country_indeed='USA',
                max_terms=3  # Limit terms
            )
            
            # Format jobs for our platform
            formatted_jobs = self.enhanced_scraper.format_jobs_for_platform(raw_jobs)
            
            print(f"✓ Successfully fetched and formatted {len(formatted_jobs)} real jobs")
            
            # If we got very few real jobs, mix in some generated ones
            if len(formatted_jobs) < 20:
                print(f"⚠️  Only got {len(formatted_jobs)} real jobs, adding generated jobs for better results")
                # Get relevant generated jobs
                generated = self._get_sample_jobs()
                # Mix real jobs first, then generated
                formatted_jobs = formatted_jobs + generated[:100]
            
            # Update cache
            self.real_jobs_cache[cache_key] = formatted_jobs
            self.real_jobs_last_fetch[cache_key] = now
            
            return formatted_jobs
            
        except Exception as e:
            print(f"✗ Error fetching real jobs: {e}")
            import traceback
            traceback.print_exc()
            print(f"   Falling back to generated jobs...")
            # Return generated jobs as fallback
            return self.all_jobs
    
    def _expand_search_terms(self, query):
        """
        Expand a single search query into multiple related terms for better coverage
        """
        if not query:
            return ['Software Engineer']
        
        query_lower = query.lower()
        
        # Data Engineer related terms
        if 'data engineer' in query_lower or 'data' in query_lower:
            return [
                'Data Engineer',
                'Big Data Engineer',
                'ETL Engineer',
                'Data Pipeline Engineer',
                'Data Integration Engineer',
                'Data Platform Engineer',
                'Cloud Data Engineer',
                'Data Warehouse Engineer'
            ]
        
        # Software Engineer related terms
        elif 'software' in query_lower or 'swe' in query_lower:
            return [
                'Software Engineer',
                'Backend Engineer',
                'Full Stack Engineer',
                'Application Developer'
            ]
        
        # Frontend related terms
        elif 'frontend' in query_lower or 'front end' in query_lower:
            return [
                'Frontend Engineer',
                'Front End Developer',
                'UI Engineer',
                'React Developer'
            ]
        
        # Machine Learning related terms
        elif 'machine learning' in query_lower or 'ml' in query_lower or 'ai' in query_lower:
            return [
                'Machine Learning Engineer',
                'ML Engineer',
                'AI Engineer',
                'Applied Scientist'
            ]
        
        # DevOps related terms
        elif 'devops' in query_lower or 'sre' in query_lower:
            return [
                'DevOps Engineer',
                'Site Reliability Engineer',
                'Infrastructure Engineer',
                'Platform Engineer'
            ]
        
        # Default: use the query as-is
        else:
            return [query]
    
    def get_job_by_id(self, job_id):
        """Get a specific job by ID"""
        jobs = self._get_sample_jobs()
        for job in jobs:
            if job['id'] == job_id:
                return job
        return None
    
    def get_statistics(self):
        """Get job statistics"""
        jobs = self._get_sample_jobs()
        
        company_set = sorted(list(set(j['company'] for j in jobs if 'company' in j)))

        return {
            'total_jobs': len(jobs),
            'remote_jobs': len([j for j in jobs if j['remote']]),
            'companies': len(company_set),
            'company_list': company_set,
            'reputed_companies': len([j for j in jobs if j.get('reputed', False)]),
            'locations': len(set(j['location'] for j in jobs))
        }
