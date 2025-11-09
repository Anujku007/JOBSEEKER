// Job Actions JavaScript - Save and Apply functionality
console.log('✅ job_actions.js loaded successfully');

function initializeJobActions() {
    console.log('Initializing job actions...');

    // Ensure we know if the user is authenticated
    const isUserAuthenticated = document.body.getAttribute('data-user-authenticated') === 'true';
    console.log("User authenticated:", isUserAuthenticated);

    // Save job functionality
    document.querySelectorAll('.save-job-btn').forEach(button => {
        button.addEventListener('click', function() {
            const jobId = this.dataset.jobId;
            const isSaved = this.dataset.saved === 'true';

            if (!isUserAuthenticated) {
                window.location.href = "/auth/login";
                return;
            }

            if (!isSaved) {
                saveJob(jobId, this);
            } else {
                unsaveJob(jobId, this);
            }
        });
    });

    // Apply job functionality
    document.querySelectorAll('.apply-job-btn').forEach(button => {
        button.addEventListener('click', function() {
            const jobId = this.dataset.jobId;
            const isApplied = this.dataset.applied === 'true';

            if (!isUserAuthenticated) {
                window.location.href = "/auth/login";
                return;
            }

            if (!isApplied) {
                openApplyForm(jobId, this);  // ✅ Show popup form before applying
            } else {
                showNotification('You have already applied to this job.', 'warning');
            }
        });
    });
}

// ------------------------
// SAVE / UNSAVE JOB
// ------------------------
function saveJob(jobId, button) {
    console.log(`Saving job: ${jobId}`);

    fetch(`/jobs/${jobId}/save`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateSaveButton(button, true);
            showNotification('💾 Job saved successfully!', 'success');
        } else {
            showNotification(data.message || 'Error saving job', 'error');
        }
    })
    .catch(error => {
        console.error('❌ Error saving job:', error);
        showNotification('Error saving job', 'error');
    });
}

function unsaveJob(jobId, button) {
    console.log(`Unsaving job: ${jobId}`);

    fetch(`/jobs/${jobId}/unsave`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateSaveButton(button, false);
            showNotification('❎ Job removed from saved', 'success');
        } else {
            showNotification(data.message || 'Error unsaving job', 'error');
        }
    })
    .catch(error => {
        console.error('❌ Error unsaving job:', error);
        showNotification('Error unsaving job', 'error');
    });
}

// ------------------------
// APPLY JOB (Popup Form)
// ------------------------
function openApplyForm(jobId, button) {
    Swal.fire({
        title: "Apply for Job",
        html: `
            <input id="swal-name" class="swal2-input" placeholder="Full Name" required>
            <input id="swal-email" class="swal2-input" placeholder="Email" required>
            <textarea id="swal-cover" class="swal2-textarea" placeholder="Cover Letter (optional)"></textarea>
        `,
        confirmButtonText: "Submit Application",
        focusConfirm: false,
        preConfirm: () => {
            const name = document.getElementById("swal-name").value.trim();
            const email = document.getElementById("swal-email").value.trim();
            const cover = document.getElementById("swal-cover").value.trim();
            if (!name || !email) {
                Swal.showValidationMessage("Please fill in your name and email.");
                return false;
            }
            return { name, email, cover };
        }
    }).then((result) => {
        if (result.isConfirmed && result.value) {
            applyToJob(jobId, button, result.value);
        }
    });
}

function applyToJob(jobId, button, formValues) {
    console.log(`Applying to job: ${jobId}`);

    const formData = new FormData();
    formData.append("name", formValues.name);
    formData.append("email", formValues.email);
    formData.append("cover_letter", formValues.cover);

    fetch(`/jobs/${jobId}/apply`, {
        method: 'POST',
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" },
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateApplyButton(button, true);
            Swal.fire({
                icon: "success",
                title: data.message || "Application submitted successfully!",
                timer: 2500,
                showConfirmButton: false
            });
        } else {
            Swal.fire("Warning", data.message || "Failed to apply.", "warning");
        }
    })
    .catch(error => {
        console.error('❌ Error applying job:', error);
        Swal.fire("Error", "Failed to apply for job. Try again.", "error");
    });
}

// ------------------------
// BUTTON UPDATERS
// ------------------------
function updateSaveButton(button, isSaved) {
    if (isSaved) {
        button.innerHTML = '<i class="fas fa-bookmark mr-2 text-blue-600"></i> Saved';
        button.classList.add('bg-green-100', 'text-green-700');
    } else {
        button.innerHTML = '<i class="far fa-bookmark mr-2"></i> Save Job';
        button.classList.remove('bg-green-100', 'text-green-700');
    }
    button.dataset.saved = isSaved.toString();
}

function updateApplyButton(button, isApplied) {
    if (isApplied) {
        button.innerHTML = '<i class="fas fa-check mr-2"></i> Applied';
        button.classList.remove('bg-blue-600', 'hover:bg-blue-700');
        button.classList.add('bg-green-600');
        button.disabled = true;
    }
    button.dataset.applied = isApplied.toString();
}

// ------------------------
// NOTIFICATIONS
// ------------------------
function showNotification(message, type = 'success') {
    document.querySelectorAll('.custom-notification').forEach(n => n.remove());
    const notification = document.createElement('div');
    notification.className = `custom-notification fixed top-4 right-4 px-4 py-3 rounded-lg shadow-lg text-white z-50 ${
        type === 'success' ? 'bg-green-500' :
        type === 'warning' ? 'bg-yellow-500' : 'bg-red-500'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Auto-initialize
document.addEventListener('DOMContentLoaded', initializeJobActions);
