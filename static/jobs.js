// Job Finder - Frontend JavaScript

let currentPage = 1;
let totalPages = 1;
let currentFilters = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStatistics();
    loadJobs();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Search button
    document.getElementById('searchBtn').addEventListener('click', () => {
        currentPage = 1;
        loadJobs();
    });

    // Enter key in search inputs
    document.getElementById('searchQuery').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            currentPage = 1;
            loadJobs();
        }
    });

    document.getElementById('searchLocation').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            currentPage = 1;
            loadJobs();
        }
    });

    // Filters
    document.getElementById('postedTimeFilter').addEventListener('change', () => {
        currentPage = 1;
        loadJobs();
    });

    document.getElementById('categoryFilter').addEventListener('change', () => {
        currentPage = 1;
        loadJobs();
    });

    document.getElementById('remoteFilter').addEventListener('change', () => {
        currentPage = 1;
        loadJobs();
    });

    document.getElementById('jobTypeFilter').addEventListener('change', () => {
        currentPage = 1;
        loadJobs();
    });

    document.getElementById('experienceFilter').addEventListener('change', () => {
        currentPage = 1;
        loadJobs();
    });

    document.getElementById('sortByFilter').addEventListener('change', () => {
        currentPage = 1;
        loadJobs();
    });

    document.getElementById('sponsorshipFilter').addEventListener('change', () => {
        currentPage = 1;
        loadJobs();
    });

    // Pagination
    document.getElementById('prevPage').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadJobs();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });

    document.getElementById('nextPage').addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            loadJobs();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });

    // Retry button
    document.getElementById('retryBtn').addEventListener('click', () => {
        loadJobs();
    });
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        
        document.getElementById('availableJobs').textContent = data.total_jobs || 0;
        document.getElementById('totalJobs').textContent = data.total_jobs || 0;
        document.getElementById('remoteJobs').textContent = data.remote_jobs || 0;
        document.getElementById('totalCompanies').textContent = data.reputed_companies || 0;
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load jobs with filters
async function loadJobs() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorMessage = document.getElementById('errorMessage');
    const jobsContainer = document.getElementById('jobsContainer');
    const pagination = document.getElementById('pagination');

    // Show loading, hide error and jobs
    loadingSpinner.style.display = 'block';
    errorMessage.style.display = 'none';
    jobsContainer.innerHTML = '';
    pagination.style.display = 'none';
    
    // Show helpful message if fetching real jobs
    if (document.getElementById('realJobsFilter').checked) {
        jobsContainer.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #4CAF50; background: #f0f9ff; border-radius: 8px; margin: 1rem 0;">
                <i class="fas fa-info-circle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <p style="font-size: 1.1rem; font-weight: bold;">Fetching real jobs from Indeed & LinkedIn...</p>
                <p style="margin-top: 0.5rem;">This may take 15-30 seconds for fresh results.</p>
                <p style="margin-top: 0.5rem; font-size: 0.9rem; color: #666;">☕ Grab a coffee while we search!</p>
            </div>
        `;
    }

    // Get filter values
    const query = document.getElementById('searchQuery').value;
    const location = document.getElementById('searchLocation').value;
    const remote = document.getElementById('remoteFilter').checked;
    const jobType = document.getElementById('jobTypeFilter').value;
    const experienceLevel = document.getElementById('experienceFilter').value;
    const postedTime = document.getElementById('postedTimeFilter').value;
    const realJobs = document.getElementById('realJobsFilter').checked;

    // Build query string
    const params = new URLSearchParams({
        query: query,
        location: location,
        remote: remote,
        job_type: jobType,
        experience_level: experienceLevel,
        date_posted: postedTime,
        real_jobs: realJobs,
        page: currentPage,
        per_page: 10
    });

    try {
        // Add timeout for fetch (60 seconds)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000);
        
        const response = await fetch(`/api/jobs?${params}`, {
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Check for errors in response
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Hide loading
        loadingSpinner.style.display = 'none';

        if (data.jobs && data.jobs.length > 0) {
            displayJobs(data.jobs);
            updatePagination(data);
            updateJobsCount(data.total);
        } else {
            jobsContainer.innerHTML = `
                <div style="text-align: center; padding: 3rem; color: #666;">
                    <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 1rem; color: #ccc;"></i>
                    <p style="font-size: 1.2rem;">No jobs found matching your criteria.</p>
                    <p>Try adjusting your filters or search terms.</p>
                </div>
            `;
            updateJobsCount(0);
        }
    } catch (error) {
        console.error('Error loading jobs:', error);
        loadingSpinner.style.display = 'none';
        
        // Show more helpful error message
        jobsContainer.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #f44336; background: #ffebee; border-radius: 8px; margin: 1rem 0;">
                <i class="fas fa-exclamation-triangle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <p style="font-size: 1.1rem; font-weight: bold;">Oops! Something went wrong.</p>
                <p style="margin-top: 0.5rem;">${error.name === 'AbortError' ? 'Request timed out. The job search took too long.' : error.message}</p>
                <p style="margin-top: 1rem; font-size: 0.9rem;">
                    💡 Try: Unchecking "Fetch Real Jobs" for instant generated results, or try again in a moment.
                </p>
                <button onclick="loadJobs()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    <i class="fas fa-redo"></i> Try Again
                </button>
            </div>
        `;
    }
}

// Display jobs
function displayJobs(jobs) {
    const jobsContainer = document.getElementById('jobsContainer');
    jobsContainer.innerHTML = '';

    jobs.forEach(job => {
        const jobCard = createJobCard(job);
        jobsContainer.appendChild(jobCard);
    });
}

// Create job card element
function createJobCard(job) {
    const card = document.createElement('div');
    card.className = 'job-card';
    
    // Determine work mode badge
    let workModeBadge = '';
    if (job.remote) {
        workModeBadge = '<span class="badge badge-remote"><i class="fas fa-laptop-house"></i> Remote</span>';
    } else if (job.location && job.location.toLowerCase().includes('hybrid')) {
        workModeBadge = '<span class="badge badge-hybrid"><i class="fas fa-building"></i> Hybrid</span>';
    } else {
        workModeBadge = '<span class="badge badge-onsite"><i class="fas fa-building"></i> On-site</span>';
    }

    // Additional badges
    const additionalBadges = [];
    
    // Top company badge (for senior positions or high salary)
    if (job.experience_level === 'Senior' || (job.salary && job.salary.includes('160k'))) {
        additionalBadges.push('<span class="badge badge-top-company"><i class="fas fa-star"></i> Top Company</span>');
    }
    
    // Urgent/Fresh badge (posted within last 24 hours)
    const hoursAgo = getHoursAgo(job.posted_date);
    if (hoursAgo <= 24) {
        additionalBadges.push('<span class="badge badge-urgent"><i class="fas fa-fire"></i> Fresh</span>');
    }
    
    // Sponsorship badge
    if (job.sponsorship) {
        additionalBadges.push('<span class="badge badge-sponsorship"><i class="fas fa-globe"></i> Sponsorship</span>');
    }

    const skillsHTML = job.skills 
        ? job.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')
        : '';

    const postedDate = formatDate(job.posted_date);

    card.innerHTML = `
        <div class="job-header">
            <div class="job-title-section">
                <h3>${escapeHtml(job.title)}</h3>
                <p class="job-company"><i class="fas fa-building"></i> ${escapeHtml(job.company)}</p>
            </div>
            <div class="job-badges">
                ${workModeBadge}
                ${additionalBadges.join('')}
            </div>
        </div>
        
        <div class="job-details">
            <div class="job-detail">
                <i class="fas fa-map-marker-alt"></i>
                <span>${escapeHtml(job.location)}</span>
            </div>
            <div class="job-detail">
                <i class="fas fa-briefcase"></i>
                <span>${escapeHtml(job.job_type)}</span>
            </div>
            <div class="job-detail">
                <i class="fas fa-layer-group"></i>
                <span>${escapeHtml(job.experience_level)}</span>
            </div>
            ${job.salary ? `
                <div class="job-detail">
                    <i class="fas fa-dollar-sign"></i>
                    <span>${escapeHtml(job.salary)}</span>
                </div>
            ` : ''}
        </div>

        <p class="job-description">${escapeHtml(job.description)}</p>

        ${skillsHTML ? `<div class="job-skills">${skillsHTML}</div>` : ''}

        <div class="job-footer">
            <span class="job-posted">
                <i class="fas fa-clock"></i> Posted ${postedDate}
            </span>
            <button class="apply-btn" onclick="window.open('${job.url}', '_blank')">
                <i class="fas fa-external-link-alt"></i> Apply Now
            </button>
        </div>
    `;

    return card;
}

// Update pagination
function updatePagination(data) {
    const pagination = document.getElementById('pagination');
    const prevBtn = document.getElementById('prevPage');
    const nextBtn = document.getElementById('nextPage');
    const pageNumbers = document.getElementById('pageNumbers');

    totalPages = data.total_pages || 1;
    
    if (totalPages > 1) {
        pagination.style.display = 'flex';
        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage === totalPages;
        
        // Generate page numbers
        pageNumbers.innerHTML = '';
        
        // Show max 7 page numbers
        let startPage = Math.max(1, currentPage - 3);
        let endPage = Math.min(totalPages, currentPage + 3);
        
        // Adjust if at the beginning or end
        if (currentPage <= 4) {
            endPage = Math.min(7, totalPages);
        }
        if (currentPage > totalPages - 4) {
            startPage = Math.max(1, totalPages - 6);
        }
        
        // First page
        if (startPage > 1) {
            const firstPage = createPageNumber(1);
            pageNumbers.appendChild(firstPage);
            if (startPage > 2) {
                const dots = document.createElement('span');
                dots.className = 'page-info';
                dots.textContent = '...';
                pageNumbers.appendChild(dots);
            }
        }
        
        // Page numbers
        for (let i = startPage; i <= endPage; i++) {
            const pageNum = createPageNumber(i);
            pageNumbers.appendChild(pageNum);
        }
        
        // Last page
        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                const dots = document.createElement('span');
                dots.className = 'page-info';
                dots.textContent = '...';
                pageNumbers.appendChild(dots);
            }
            const lastPage = createPageNumber(totalPages);
            pageNumbers.appendChild(lastPage);
        }
    } else {
        pagination.style.display = 'none';
    }
}

// Create page number button
function createPageNumber(pageNum) {
    const btn = document.createElement('button');
    btn.className = 'page-number';
    if (pageNum === currentPage) {
        btn.classList.add('active');
    }
    btn.textContent = pageNum;
    btn.addEventListener('click', () => {
        currentPage = pageNum;
        loadJobs();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    return btn;
}

// Update jobs count
function updateJobsCount(total) {
    const jobsCount = document.querySelector('.jobs-count');
    jobsCount.textContent = `${total} Job${total !== 1 ? 's' : ''} Found`;
}

// Get hours ago
function getHoursAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
    return diffHours;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffHours < 1) {
        return 'just now';
    } else if (diffHours < 24) {
        return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    } else if (diffDays === 1) {
        return 'yesterday';
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else if (diffDays < 30) {
        const weeks = Math.floor(diffDays / 7);
        return `${weeks} week${weeks > 1 ? 's' : ''} ago`;
    } else {
        const months = Math.floor(diffDays / 30);
        return `${months} month${months > 1 ? 's' : ''} ago`;
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Filter functions for stat cards
function filterByAll() {
    document.getElementById('searchQuery').value = '';
    document.getElementById('remoteFilter').checked = false;
    document.getElementById('realJobsFilter').checked = false;
    currentPage = 1;
    loadJobs();
}

function filterByRemote() {
    document.getElementById('searchQuery').value = '';
    document.getElementById('remoteFilter').checked = true;
    document.getElementById('realJobsFilter').checked = false;
    currentPage = 1;
    loadJobs();
}

function filterByReputed() {
    // Search for reputed companies
    document.getElementById('searchQuery').value = '';
    document.getElementById('remoteFilter').checked = false;
    document.getElementById('realJobsFilter').checked = false;
    currentPage = 1;
    loadJobs();
    // Note: Backend would need to add reputed company filter
}
