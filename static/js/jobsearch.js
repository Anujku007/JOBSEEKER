// static/js/jobsearch.js

document.addEventListener('DOMContentLoaded', function() {
    const jobListings = document.getElementById('job-listings');
    const jobCount = document.getElementById('job-count');
    const searchForm = document.querySelector('form[action="/jobs/"]');
    const searchInput = document.querySelector('input[name="q"]');
    const locationInput = document.querySelector('input[name="location"]');

    // Get URL parameters
    function getUrlParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            q: params.get('q') || '',
            location: params.get('location') || ''
        };
    }

    // Update the URL with the search parameters
    function updateUrl(params) {
        const url = new URL(window.location);
        url.search = new URLSearchParams(params).toString();
        window.history.pushState({}, '', url);
    }

    // Fetch jobs from the API
    async function fetchJobs(params = {}) {
        const apiUrl = '/jobs/api/search?' + new URLSearchParams(params);
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching jobs:', error);
            return { success: false, jobs: [] };
        }
    }

    // Render job count
    function renderJobCount(count) {
        jobCount.textContent = `Available Jobs (${count})`;
    }

    // Render job listings
    function renderJobs(jobs) {
        if (jobs.length === 0) {
            jobListings.innerHTML = `
                <div class="text-center py-12">
                    <i class="fas fa-search text-gray-400 text-6xl mb-4"></i>
                    <h3 class="text-2xl font-semibold text-gray-600">No jobs found</h3>
                    <p class="text-gray-500">Try different search terms or <a href="/jobs/" class="text-blue-600 hover:text-blue-800">browse all jobs</a></p>
                </div>
            `;
            return;
        }

        const jobsHTML = jobs.map(job => `
            <div class="bg-white rounded-2xl shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="flex flex-col md:flex-row md:items-center justify-between">
                    <div class="flex-1">
                        <h3 class="text-xl font-semibold text-gray-900 mb-2">
                            <a href="/jobs/${job.id}" class="hover:text-blue-600">${job.title}</a>
                        </h3>
                        <p class="text-gray-600 mb-2">${job.company} • ${job.location}</p>
                        <div class="flex justify-between">
                          <span class="text-gray-600">Job Type:</span>
                           <span class="font-medium">{{ job.job_type }}</span>
                            </span>
                            ${job.remote ? '<span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Remote</span>' : ''}
                            <span class="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm">
                                ${job.source}
                            </span>
                        </div>
                        <p class="text-gray-700 line-clamp-2">${job.description}</p>
                    </div>
                    <div class="mt-4 md:mt-0 md:text-right">
                        ${job.salary ? `<p class="text-lg font-semibold text-gray-900 mb-2">${job.salary}</p>` : ''}
                        <p class="text-sm text-gray-500 mb-3">Posted ${job.posted_date}</p>
                        <a href="/jobs/${job.id}" class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors inline-block">
                            View Details
                        </a>
                    </div>
                </div>
            </div>
        `).join('');

        jobListings.innerHTML = jobsHTML;
    }

    // Load and display jobs
    async function loadJobs() {
        const params = getUrlParams();
        // Update the form inputs
        searchInput.value = params.q;
        locationInput.value = params.location;

        jobCount.textContent = 'Loading jobs...';
        jobListings.innerHTML = '';

        const data = await fetchJobs(params);
        if (data.success) {
            renderJobCount(data.count);
            renderJobs(data.jobs);
        } else {
            jobCount.textContent = 'Error loading jobs';
        }
    }

    // Handle search form submission
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const params = {
                q: searchInput.value,
                location: locationInput.value
            };
            updateUrl(params);
            loadJobs();
        });
    }

    // Initial load
    loadJobs();
});