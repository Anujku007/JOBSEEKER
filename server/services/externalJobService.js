const axios = require('axios');

/**
 * Fetches external jobs via RapidAPI JSearch when RAPIDAPI_KEY is configured,
 * or returns curated fallback listings so the aggregator endpoint always works.
 */
const fetchExternalJobs = async ({ query = 'Software Developer', location = 'India' }) => {
  const apiKey = process.env.RAPIDAPI_KEY;
  const apiHost = process.env.RAPIDAPI_HOST || 'jsearch.p.rapidapi.com';

  if (apiKey && apiKey !== 'your_rapidapi_jsearch_key_optional') {
    try {
      const response = await axios.get(`https://${apiHost}/search`, {
        params: {
          query: `${query} in ${location}`,
          page: '1',
          num_pages: '1',
        },
        headers: {
          'X-RapidAPI-Key': apiKey,
          'X-RapidAPI-Host': apiHost,
        },
        timeout: 8000,
      });

      const items = response.data?.data || [];
      return items.map((item) => ({
        _id: `ext_${item.job_id}`,
        title: item.job_title,
        companyName: item.employer_name,
        location: [item.job_city, item.job_country].filter(Boolean).join(', ') || location,
        jobType: item.job_is_remote ? 'Remote' : 'Full-Time',
        salaryRange:
          item.job_min_salary && item.job_max_salary
            ? `${item.job_salary_currency || 'INR'} ${item.job_min_salary} - ${item.job_max_salary}`
            : 'Not Disclosed',
        description: item.job_description?.slice(0, 600) || 'External job listing.',
        skillsRequired: item.job_highlights?.Qualifications?.slice(0, 4) || ['JavaScript', 'React', 'Node.js'],
        source: 'external',
        externalApplyUrl: item.job_apply_link,
        createdAt: item.job_posted_at_datetime_utc || new Date().toISOString(),
      }));
    } catch (error) {
      console.warn('External API fallback triggered:', error.message);
    }
  }

  return [
    {
      _id: 'ext_demo_1',
      title: `${query} (External Partner Feed)`,
      companyName: 'CloudScale Technologies',
      location: location || 'Bengaluru, India',
      jobType: 'Full-Time',
      salaryRange: '₹12,00,000 - ₹18,00,000',
      description:
        'Aggregated external opening. Add your RAPIDAPI_KEY in server/.env to pull real-time listings from RapidAPI JSearch.',
      skillsRequired: ['React', 'Node.js', 'MongoDB', 'REST APIs'],
      source: 'external',
      externalApplyUrl: 'https://www.linkedin.com/jobs/',
      createdAt: new Date().toISOString(),
    },
  ];
};

module.exports = { fetchExternalJobs };
