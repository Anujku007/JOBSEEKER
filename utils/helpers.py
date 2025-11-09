def format_salary(salary_min, salary_max, currency='$'):
    """Format salary range for display"""
    if salary_min and salary_max:
        return f"{currency}{salary_min:,} - {currency}{salary_max:,}"
    return "Salary not specified"

def validate_search_params(query, location):
    """Validate search parameters"""
    errors = []
    
    if len(query) > 100:
        errors.append("Search query too long")
    
    if len(location) > 50:
        errors.append("Location too long")
    
    return errors

def get_job_type_badge_color(job_type):
    """Return Tailwind CSS classes for job type badges"""
    colors = {
        'full-time': 'bg-blue-100 text-blue-800',
        'part-time': 'bg-green-100 text-green-800',
        'contract': 'bg-yellow-100 text-yellow-800',
        'internship': 'bg-purple-100 text-purple-800'
    }
    return colors.get(job_type, 'bg-gray-100 text-gray-800')