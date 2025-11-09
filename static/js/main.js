// static/js/main.js

// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    
    // Handle Save Job buttons
    const saveButtons = document.querySelectorAll('.save-job-btn');
    saveButtons.forEach(button => {
        button.addEventListener('click', function() {
            const jobId = this.getAttribute('data-job-id');
            const heartIcon = this.querySelector('i');
            
            // Send request to server
            fetch(`/jobs/save-job/${jobId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.saved) {
                    // Job was saved
                    heartIcon.classList.remove('far');
                    heartIcon.classList.add('fas');
                    this.classList.add('text-red-500');
                    alert('Job saved!');
                } else {
                    // Job was unsaved
                    heartIcon.classList.remove('fas');
                    heartIcon.classList.add('far');
                    this.classList.remove('text-red-500');
                    alert('Job removed from saved jobs');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving job');
            });
        });
    });
    
    // Handle Quick Apply buttons
    const applyButtons = document.querySelectorAll('.quick-apply-btn');
    applyButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.disabled) return;
            
            const jobId = this.getAttribute('data-job-id');
            
            fetch(`/jobs/apply-job/${jobId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Application successful
                    this.disabled = true;
                    this.classList.remove('bg-green-600', 'hover:bg-green-700');
                    this.classList.add('bg-gray-400');
                    this.innerHTML = '<i class="fas fa-paper-plane"></i> Applied';
                    alert('Application submitted!');
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error applying to job');
            });
        });
    });
});