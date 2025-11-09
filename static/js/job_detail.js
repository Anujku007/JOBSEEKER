// =====================================================
// JOB DETAIL PAGE INTERACTIONS
// Handles Save, Apply, and Share actions
// Compatible with Mantiks, RapidAPI & Mock jobs
// =====================================================

console.log("✅ job_detail.js initialized");

document.addEventListener("DOMContentLoaded", () => {
  const userAuthenticated = document.body.dataset.userAuthenticated === "true";
  const saveBtn = document.querySelector(".save-job-btn");
  const applyBtn = document.querySelector(".apply-job-btn");
  const shareBtn = document.querySelector(".share-job-btn");

  // -----------------------------------------------
  // 💾 SAVE / UNSAVE JOB
  // -----------------------------------------------
  if (saveBtn) {
    saveBtn.addEventListener("click", async () => {
      const jobId = saveBtn.dataset.jobId;
      const isSaved = saveBtn.dataset.saved === "true";

      if (!userAuthenticated) {
        Swal.fire({
          icon: "warning",
          title: "Please login to save jobs",
          confirmButtonText: "Login",
          showCancelButton: true,
        }).then((res) => {
          if (res.isConfirmed) window.location.href = "/auth/login";
        });
        return;
      }

      const endpoint = isSaved ? `/jobs/${jobId}/unsave` : `/jobs/${jobId}/save`;

      try {
        const res = await fetch(endpoint, {
          method: "POST",
          headers: { "X-Requested-With": "XMLHttpRequest" },
          credentials: "include",
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const data = await res.json();

        if (data.success) {
          updateSaveButton(saveBtn, !isSaved);
          Swal.fire({
            icon: "success",
            title: data.message,
            timer: 1800,
            showConfirmButton: false,
          });
        } else {
          Swal.fire({
            icon: "warning",
            title: data.message || "Failed to update saved job",
            timer: 2000,
            showConfirmButton: false,
          });
        }
      } catch (err) {
        console.error("❌ Save job error:", err);
        Swal.fire({
          icon: "error",
          title: "Server Error",
          text: err.message || "Unable to save this job. Please try again later.",
          confirmButtonColor: "#2563eb",
        });
      }
    });
  }

  // -----------------------------------------------
  // 📝 APPLY JOB (Improved version)
  // -----------------------------------------------
  if (applyBtn) {
    applyBtn.addEventListener("click", () => {
      const jobId = applyBtn.dataset.jobId;
      const applied = applyBtn.dataset.applied === "true";

      if (!userAuthenticated) {
        Swal.fire({
          icon: "warning",
          title: "Please login to apply for this job",
          confirmButtonText: "Login",
          showCancelButton: true,
        }).then((res) => {
          if (res.isConfirmed) window.location.href = "/auth/login";
        });
        return;
      }

      if (applied) {
        Swal.fire({
          icon: "info",
          title: "You’ve already applied for this job!",
          timer: 2000,
          showConfirmButton: false,
        });
        return;
      }

      // --- SweetAlert2 Apply Form ---
      Swal.fire({
        title: "Apply for this Job",
        html: `
          <form id="applyForm" class="text-left">
            <input type="text" name="name" placeholder="Full Name" class="swal2-input" required>
            <input type="email" name="email" placeholder="Email" class="swal2-input" required>
            <input type="tel" name="phone" placeholder="Phone (optional)" class="swal2-input">
            <textarea name="cover_letter" placeholder="Cover Letter (optional)" class="swal2-textarea"></textarea>
            <label class="block text-sm text-gray-600 mt-2 mb-1">Upload Resume (PDF/DOC)</label>
            <input type="file" name="resume" accept=".pdf,.doc,.docx" class="swal2-file">
          </form>
        `,
        confirmButtonText: "Submit Application",
        showCancelButton: true,
        focusConfirm: false,
        preConfirm: async () => {
          try {
            const form = Swal.getPopup().querySelector("#applyForm");
            const formData = new FormData(form);

            const response = await fetch(`/jobs/${jobId}/apply`, {
              method: "POST",
              body: formData,
              credentials: "include",
            });

            // Handle non-JSON or server issues
            let result = null;
            try {
              result = await response.json();
            } catch (err) {
              throw new Error("Unexpected response from server.");
            }

            if (!response.ok || !result.success) {
              throw new Error(result?.message || "❌ Failed to submit application.");
            }

            return result.message || "✅ Application submitted successfully!";
          } catch (error) {
            throw new Error(error.message || "Server error, please try again later.");
          }
        },
      })
        .then((result) => {
          if (result.isConfirmed) {
            updateApplyButton(applyBtn, true);
            Swal.fire({
              icon: "success",
              title: "✅ Application Submitted!",
              text: result.value || "Your application was successfully submitted.",
              confirmButtonColor: "#2563eb",
              timer: 2200,
              showConfirmButton: false,
            });
          }
        })
        .catch((error) => {
          console.error("❌ Apply job error:", error);
          Swal.fire({
            icon: "error",
            title: "Server Error",
            text: error.message || "Unable to connect to the server. Please try again later.",
            confirmButtonColor: "#2563eb",
          });
        });
    });
  }

  // -----------------------------------------------
  // 🔗 SHARE JOB
  // -----------------------------------------------
  if (shareBtn) {
    shareBtn.addEventListener("click", async () => {
      const jobUrl = window.location.href;
      try {
        await navigator.clipboard.writeText(jobUrl);
        Swal.fire({
          icon: "success",
          title: "Link copied to clipboard!",
          timer: 1500,
          showConfirmButton: false,
        });
      } catch (err) {
        console.error("Clipboard error:", err);
        Swal.fire({
          icon: "info",
          title: "Copy this link manually:",
          text: jobUrl,
        });
      }
    });
  }
});

// =====================================================
// 🔧 UI Update Helpers (Safe DOM version)
// =====================================================

function updateSaveButton(button, isSaved) {
  if (!button || !(button instanceof HTMLElement)) return;

  let icon = button.querySelector("i");
  let textSpan = button.querySelector("span");

  if (!textSpan) {
    textSpan = document.createElement("span");
    button.appendChild(textSpan);
  }

  if (isSaved) {
    if (icon) icon.className = "fas fa-bookmark mr-3 text-blue-600";
    textSpan.textContent = "Saved";
    button.classList.add("border-blue-600", "text-blue-600");
    button.classList.remove("text-gray-700", "border-gray-300");
    button.dataset.saved = "true";
  } else {
    if (icon) icon.className = "far fa-bookmark mr-3";
    textSpan.textContent = "Save for Later";
    button.classList.remove("border-blue-600", "text-blue-600");
    button.classList.add("text-gray-700", "border-gray-300");
    button.dataset.saved = "false";
  }
}

function updateApplyButton(button, isApplied) {
  if (!button || !(button instanceof HTMLElement)) return;

  let icon = button.querySelector("i");
  let textSpan = button.querySelector("span");

  if (!textSpan) {
    textSpan = document.createElement("span");
    button.appendChild(textSpan);
  }

  if (isApplied) {
    if (icon) icon.className = "fas fa-check mr-3";
    textSpan.textContent = "Applied";
    button.classList.remove("bg-blue-600", "hover:bg-blue-700");
    button.classList.add("bg-green-600", "hover:bg-green-700");
    button.dataset.applied = "true";
    button.disabled = true;
  } else {
    if (icon) icon.className = "fas fa-paper-plane mr-3";
    textSpan.textContent = "Apply Now";
    button.classList.remove("bg-green-600", "hover:bg-green-700");
    button.classList.add("bg-blue-600", "hover:bg-blue-700");
    button.dataset.applied = "false";
    button.disabled = false;
  }
}
