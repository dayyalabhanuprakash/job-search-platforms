"""
Generate large dataset of job listings
"""
import random
from datetime import datetime, timedelta

class JobDataGenerator:
    def __init__(self):
        self.companies = [
            'Citadel Securities', 'Jane Street', 'Two Sigma', 'Hudson River Trading',
            'Jump Trading', 'Optiver', 'IMC Trading', 'DRW', 'Flow Traders',
            'Virtu Financial', 'Tower Research Capital', 'Akuna Capital',
            'Five Rings Capital', 'G-Research', 'Susquehanna International Group',
            'XTX Markets', 'Quantlab', 'Belvedere Trading', 'Chicago Trading Company',
            'Wolverine Trading', 'Goldman Sachs', 'JPMorgan Chase', 'Morgan Stanley',
            'Bank of America', 'Citigroup', 'Barclays', 'BlackRock', 'Vanguard',
            'Fidelity Investments', 'Citadel', 'Millennium Management',
            'D.E. Shaw & Co.', 'Renaissance Technologies', 'Bridgewater Associates',
            'Google', 'Meta', 'Amazon', 'Microsoft', 'Apple', 'Netflix', 'Tesla',
            'Uber', 'Lyft', 'Airbnb', 'Stripe', 'Coinbase', 'Robinhood',
            'Databricks', 'Snowflake', 'Palantir', 'OpenAI', 'Anthropic',
            'IBM', 'Oracle', 'Salesforce', 'Adobe', 'Atlassian', 'Slack',
            'Zoom', 'DocuSign', 'ServiceNow', 'Workday', 'Square', 'PayPal'
        ]
        
        self.job_titles = [
            'Software Engineer', 'Senior Software Engineer', 'Staff Software Engineer',
            'Principal Engineer', 'Full Stack Developer', 'Frontend Developer',
            'Backend Developer', 'Data Engineer', 'Senior Data Engineer',
            'Data Scientist', 'Machine Learning Engineer', 'ML Engineer',
            'DevOps Engineer', 'Site Reliability Engineer', 'Cloud Engineer',
            'Quantitative Trader', 'Quantitative Researcher', 'Quantitative Developer',
            'Software Development Engineer', 'Engineering Manager', 'Technical Lead',
            'Product Manager', 'Solutions Architect', 'Security Engineer',
            'Python Developer', 'Java Developer', 'C++ Developer', 'React Developer',
            'Node.js Developer', 'Mobile Developer', 'iOS Developer', 'Android Developer',
            'Platform Engineer', 'Infrastructure Engineer', 'Database Administrator',
            'QA Engineer', 'Test Engineer', 'Automation Engineer'
        ]
        
        self.locations = [
            'New York, NY', 'San Francisco, CA', 'Chicago, IL', 'Austin, TX',
            'Seattle, WA', 'Boston, MA', 'Los Angeles, CA', 'Remote',
            'Denver, CO', 'Washington, DC', 'Atlanta, GA', 'Miami, FL',
            'Philadelphia, PA', 'San Diego, CA', 'Dallas, TX', 'Houston, TX',
            'Portland, OR', 'Phoenix, AZ', 'Minneapolis, MN', 'Detroit, MI'
        ]
        
        self.skills_pool = [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'Go', 'Rust',
            'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'Spring',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform',
            'SQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Kafka', 'Spark',
            'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch',
            'Data Science', 'Statistics', 'Algorithms', 'System Design',
            'REST API', 'GraphQL', 'Microservices', 'CI/CD', 'Git'
        ]
        
        self.job_types = ['Full-time', 'Part-time', 'Contract', 'Internship']
        self.experience_levels = ['Entry-level', 'Mid-level', 'Senior']
        
        self.reputed_companies = [
            'Citadel Securities', 'Jane Street', 'Two Sigma', 'Hudson River Trading',
            'Jump Trading', 'Optiver', 'Goldman Sachs', 'JPMorgan Chase',
            'BlackRock', 'Vanguard', 'Google', 'Meta', 'Amazon', 'Microsoft', 'Apple'
        ]
    
    def generate_jobs(self, count=100):
        """Generate specified number of jobs"""
        jobs = []
        now = datetime.now()
        
        for i in range(count):
            company = random.choice(self.companies)
            is_reputed = company in self.reputed_companies
            is_remote = random.choice([True, False, False])  # 33% remote
            
            # Generate posted date within last 48 hours
            hours_ago = random.randint(1, 48)
            posted_date = (now - timedelta(hours=hours_ago)).strftime('%Y-%m-%d')
            
            # Random salary range
            if 'Senior' in random.choice(self.job_titles) or 'Principal' in random.choice(self.job_titles):
                salary_min = random.randint(130, 200)
                salary_max = random.randint(salary_min + 40, salary_min + 100)
            else:
                salary_min = random.randint(80, 140)
                salary_max = random.randint(salary_min + 30, salary_min + 60)
            
            title = random.choice(self.job_titles)
            
            # Generate realistic company career page URLs
            location_param = random.choice(self.locations) if not is_remote else 'Remote'
            company_clean = company.replace(' ', '').replace('&', '').replace('.', '').replace(',', '').lower()
            title_clean = title.replace(' ', '-').lower()
            
            # Create realistic company career page URLs
            # Format: company.com/careers or company.com/jobs
            career_page_formats = [
                f'https://www.{company_clean}.com/careers',
                f'https://careers.{company_clean}.com',
                f'https://www.{company_clean}.com/jobs',
                f'https://jobs.{company_clean}.com',
                f'https://www.{company_clean}.com/careers/{title_clean}',
            ]
            
            job_search_urls = career_page_formats
            
            job = {
                'id': f'job-{i+1}',
                'title': title,
                'company': company,
                'location': location_param,
                'remote': is_remote,
                'salary': f'${salary_min}k - ${salary_max}k',
                'job_type': random.choice(self.job_types),
                'experience_level': random.choice(self.experience_levels),
                'posted_date': posted_date,
                'description': f'Join our team as a {title}. Work on exciting projects with cutting-edge technologies.',
                'skills': random.sample(self.skills_pool, k=random.randint(4, 8)),
                'url': random.choice(job_search_urls),
                'source': 'Generated',
                'reputed': is_reputed
            }
            jobs.append(job)
        
        return jobs
