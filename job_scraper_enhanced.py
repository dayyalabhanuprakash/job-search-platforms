"""
Enhanced Job Scraper using python-jobspy
Supports: Indeed, Glassdoor, Dice, LinkedIn, ZipRecruiter, Google Jobs
"""
from jobspy import scrape_jobs
from datetime import datetime, timedelta
import pandas as pd

class EnhancedJobScraper:
    def __init__(self):
        self.supported_sites = ['indeed', 'linkedin', 'glassdoor', 'zip_recruiter', 'google']
        
    def scrape_jobs_multi_term(self, search_terms, locations, sites=None, 
                                results_wanted=50, hours_old=48, job_type='fulltime',
                                country_indeed='USA', max_terms=3):
        """
        Scrape jobs with multiple search terms and locations
        
        Args:
            search_terms (list): List of job titles to search for
            locations (list): List of locations to search in
            sites (list): List of sites to scrape from
            results_wanted (int): Number of results per search
            hours_old (int): Only return jobs posted within this many hours
            job_type (str): Type of job (fulltime, parttime, contract, internship)
            country_indeed (str): Country for Indeed searches
            max_terms (int): Maximum search terms to use (for speed)
        
        Returns:
            list: Combined list of job dictionaries
        """
        if sites is None:
            sites = self.supported_sites
        
        # Limit search terms for faster results
        search_terms = search_terms[:max_terms]
        
        all_jobs = []
        total_searches = len(search_terms) * len(locations)
        current_search = 0
        
        print(f"\n{'='*80}")
        print(f"🔍 ENHANCED JOB SCRAPER - QUICK SEARCH")
        print(f"{'='*80}")
        print(f"Search Terms: {', '.join(search_terms)} (limited to {max_terms} for speed)")
        print(f"Locations: {', '.join(locations)}")
        print(f"Sites: {', '.join(sites)}")
        print(f"Results per search: {results_wanted}")
        print(f"Hours old filter: {hours_old} hours")
        print(f"Total searches to perform: {total_searches}")
        print(f"{'='*80}\n")
        
        for search_term in search_terms:
            for location in locations:
                current_search += 1
                print(f"\n[{current_search}/{total_searches}] Searching: '{search_term}' in '{location}'")
                print("-" * 60)
                
                try:
                    # Scrape jobs using jobspy with timeout protection
                    jobs_df = scrape_jobs(
                        site_name=sites,
                        search_term=search_term,
                        location=location,
                        results_wanted=results_wanted,
                        hours_old=hours_old,
                        country_indeed=country_indeed,
                        job_type=job_type,
                        is_remote=False  # We'll handle remote filtering separately
                    )
                    
                    if jobs_df is not None and not jobs_df.empty:
                        print(f"✓ Found {len(jobs_df)} jobs for '{search_term}' in '{location}'")
                        
                        # Convert DataFrame to list of dicts
                        jobs_list = jobs_df.to_dict('records')
                        all_jobs.extend(jobs_list)
                    else:
                        print(f"✗ No jobs found for '{search_term}' in '{location}'")
                        
                except Exception as e:
                    print(f"✗ Error scraping '{search_term}' in '{location}': {str(e)}")
                    continue
        
        print(f"\n{'='*80}")
        print(f"✓ TOTAL JOBS SCRAPED: {len(all_jobs)}")
        print(f"{'='*80}\n")
        
        # Remove duplicates based on job URL
        unique_jobs = self._remove_duplicates(all_jobs)
        print(f"✓ After removing duplicates: {len(unique_jobs)} unique jobs\n")
        
        return unique_jobs
    
    def scrape_data_engineer_jobs(self, locations=['United States', 'Remote'], 
                                   sites=None, results_wanted=50, hours_old=48):
        """
        Specialized scraper for Data Engineer positions with multiple related terms
        
        This uses the exact search terms you specified in your command
        """
        search_terms = [
            "Data Engineer",
            "Big Data Engineer",
            "ETL Engineer",
            "Data Pipeline Engineer",
            "Data Integration Engineer",
            "Data Platform Engineer",
            "Data Infrastructure Engineer",
            "Cloud Data Engineer",
            "Data Warehouse Engineer"
        ]
        
        return self.scrape_jobs_multi_term(
            search_terms=search_terms,
            locations=locations,
            sites=sites,
            results_wanted=results_wanted,
            hours_old=hours_old,
            job_type='fulltime',
            country_indeed='USA'
        )
    
    def _remove_duplicates(self, jobs):
        """Remove duplicate jobs based on job URL"""
        seen_urls = set()
        unique_jobs = []
        
        for job in jobs:
            job_url = job.get('job_url', '') or job.get('url', '')
            if job_url and job_url not in seen_urls:
                seen_urls.add(job_url)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def format_jobs_for_platform(self, jobs):
        """
        Convert jobspy format to our platform's format
        
        Args:
            jobs (list): List of jobs from jobspy
            
        Returns:
            list: List of jobs in our platform's format
        """
        formatted_jobs = []
        
        for idx, job in enumerate(jobs):
            try:
                # Extract salary information
                salary = self._format_salary(job)
                
                # Extract location
                location = job.get('location', 'Not specified')
                
                # Determine if remote
                is_remote = (
                    'remote' in str(location).lower() or
                    job.get('is_remote', False) or
                    'Remote' in str(location)
                )
                
                # Extract posted date
                posted_date = self._extract_posted_date(job)
                
                # Extract company
                company = job.get('company', job.get('company_name', 'Company not listed'))
                
                # Extract title
                title = job.get('title', job.get('job_title', 'Position'))
                
                # Extract description
                description = job.get('description', job.get('job_description', ''))
                if not description or not isinstance(description, str):
                    description = f"Exciting opportunity for {title} at {company}. Apply now!"
                
                # Truncate description if too long
                if isinstance(description, str) and len(description) > 500:
                    description = description[:497] + "..."
                
                # Extract job URL
                job_url = job.get('job_url', job.get('url', '#'))
                
                # Extract site/source
                source = job.get('site', job.get('source', 'Unknown'))
                
                # Extract job type
                job_type = job.get('job_type', 'Full-time')
                if not job_type or job_type == 'nan' or str(job_type) == 'nan':
                    job_type = 'Full-time'
                
                # Determine experience level from title or description
                experience_level = self._determine_experience_level(title, description)
                
                # Clean all fields to ensure no NaN or invalid values
                formatted_job = {
                    'id': str(f'job-{idx}-{hash(job_url) % 100000}'),
                    'title': str(title) if title else 'Position',
                    'company': str(company) if company else 'Company',
                    'location': str(location) if location else 'Location',
                    'remote': bool(is_remote),
                    'salary': str(salary) if salary else 'Not specified',
                    'job_type': str(job_type) if job_type and str(job_type) != 'nan' else 'Full-time',
                    'experience_level': str(experience_level) if experience_level else 'Not specified',
                    'posted_date': str(posted_date) if posted_date else datetime.now().strftime('%Y-%m-%d'),
                    'description': str(description) if description else 'No description available',
                    'skills': self._extract_skills(str(description)) if description else [],
                    'url': str(job_url) if job_url else '#',
                    'source': str(source).capitalize() if source else 'Unknown',
                    'reputed': False
                }
                
                formatted_jobs.append(formatted_job)
                
            except Exception as e:
                print(f"Warning: Error formatting job {idx}: {e}")
                continue
        
        return formatted_jobs
    
    def _format_salary(self, job):
        """Extract and format salary information"""
        # Try different salary fields
        min_salary = job.get('min_amount')
        max_salary = job.get('max_amount')
        interval = job.get('interval', 'yearly')
        
        # Handle None and NaN values
        try:
            if min_salary is not None and max_salary is not None:
                # Check for valid numbers (not NaN)
                if str(min_salary) != 'nan' and str(max_salary) != 'nan':
                    if interval == 'yearly':
                        return f"${int(float(min_salary)/1000)}k - ${int(float(max_salary)/1000)}k"
                    elif interval == 'monthly':
                        return f"${int(float(min_salary))} - ${int(float(max_salary))}/month"
                    elif interval == 'hourly':
                        return f"${float(min_salary):.2f} - ${float(max_salary):.2f}/hour"
            elif min_salary is not None and str(min_salary) != 'nan':
                if interval == 'yearly':
                    return f"${int(float(min_salary)/1000)}k+"
                else:
                    return f"${float(min_salary):.0f}+/{interval}"
        except (ValueError, TypeError, ZeroDivisionError):
            pass
        
        return "Salary not specified"
    
    def _extract_posted_date(self, job):
        """Extract and format posted date"""
        date_posted = job.get('date_posted')
        
        if date_posted:
            try:
                # If it's already a date object
                if isinstance(date_posted, datetime):
                    return date_posted.strftime('%Y-%m-%d')
                # If it's a string, try to parse it
                elif isinstance(date_posted, str):
                    # Try common formats
                    for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%m/%d/%Y']:
                        try:
                            parsed_date = datetime.strptime(date_posted, fmt)
                            return parsed_date.strftime('%Y-%m-%d')
                        except:
                            continue
            except:
                pass
        
        # Default to today if we can't parse
        return datetime.now().strftime('%Y-%m-%d')
    
    def _determine_experience_level(self, title, description):
        """Determine experience level from title or description"""
        title_lower = title.lower()
        desc_lower = description.lower()
        combined = f"{title_lower} {desc_lower}"
        
        if any(word in combined for word in ['senior', 'sr.', 'lead', 'principal', 'staff', 'architect']):
            return 'Senior'
        elif any(word in combined for word in ['junior', 'jr.', 'entry', 'graduate', 'associate']):
            return 'Entry-level'
        else:
            return 'Mid-level'
    
    def _extract_skills(self, description):
        """Extract skills from job description"""
        # Common tech skills to look for
        common_skills = [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust', 'Ruby',
            'SQL', 'NoSQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
            'AWS', 'Azure', 'GCP', 'Cloud',
            'Docker', 'Kubernetes', 'Jenkins',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring',
            'Machine Learning', 'AI', 'Data Science', 'Deep Learning',
            'Spark', 'Hadoop', 'Kafka', 'Airflow', 'ETL',
            'Git', 'Agile', 'Scrum', 'CI/CD'
        ]
        
        found_skills = []
        desc_lower = description.lower()
        
        for skill in common_skills:
            if skill.lower() in desc_lower:
                found_skills.append(skill)
        
        return found_skills[:10]  # Return max 10 skills


# Example usage
if __name__ == "__main__":
    scraper = EnhancedJobScraper()
    
    # Example: Scrape data engineer jobs
    print("Testing Enhanced Job Scraper...")
    
    jobs = scraper.scrape_data_engineer_jobs(
        locations=['United States', 'Remote'],
        sites=['indeed', 'linkedin', 'zip_recruiter'],
        results_wanted=10,
        hours_old=48
    )
    
    formatted_jobs = scraper.format_jobs_for_platform(jobs)
    
    print(f"\n✓ Successfully formatted {len(formatted_jobs)} jobs")
    
    # Display first job as example
    if formatted_jobs:
        print("\nExample job:")
        print(f"Title: {formatted_jobs[0]['title']}")
        print(f"Company: {formatted_jobs[0]['company']}")
        print(f"Location: {formatted_jobs[0]['location']}")
        print(f"Source: {formatted_jobs[0]['source']}")
