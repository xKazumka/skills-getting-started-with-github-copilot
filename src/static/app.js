document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;
        const participantsList = details.participants.length > 0 
          ? details.participants.map(email => `<li><span class="participant-email">${email}</span><button class="delete-btn" data-email="${email}" data-activity="${name}" type="button" title="Unregister">✕</button></li>`).join('')
          : '<li class="no-participants">No participants yet</li>';

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants-section">
            <button class="participants-toggle" type="button">
              <span class="toggle-icon">▶</span>
              <span class="participants-count">${details.participants.length} Participant${details.participants.length !== 1 ? 's' : ''}</span>
            </button>
            <ul class="participants-list collapsed">
              ${participantsList}
            </ul>
          </div>
        `;

        activitiesList.appendChild(activityCard);
        
        // Add toggle functionality
        const toggleBtn = activityCard.querySelector('.participants-toggle');
        const participantsList_elem = activityCard.querySelector('.participants-list');
        toggleBtn.addEventListener('click', () => {
          participantsList_elem.classList.toggle('collapsed');
          toggleBtn.querySelector('.toggle-icon').textContent = participantsList_elem.classList.contains('collapsed') ? '▶' : '▼';
        });

        // Add delete button functionality
        const deleteButtons = activityCard.querySelectorAll('.delete-btn');
        deleteButtons.forEach(btn => {
          btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const email = btn.getAttribute('data-email');
            const activity = btn.getAttribute('data-activity');
            
            try {
              const response = await fetch(
                `/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`,
                { method: "POST" }
              );

              if (response.ok) {
                // Remove the participant from UI
                btn.closest('li').remove();
                // Update participant count
                const participantCount = participantsList_elem.querySelectorAll('li:not(.no-participants)').length;
                toggleBtn.querySelector('.participants-count').textContent = 
                  `${participantCount} Participant${participantCount !== 1 ? 's' : ''}`;
              } else {
                const result = await response.json();
                alert(result.detail || "Failed to unregister participant");
              }
            } catch (error) {
              alert("Error unregistering participant");
              console.error("Error:", error);
            }
          });
        });

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
