// Form validation and interactivity
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("predictionForm");

  if (form) {
    // Real-time input validation
    const openingTheatersInput = document.getElementById("opening_theaters");
    const releaseDaysInput = document.getElementById("release_days");

    // Add input counters
    if (openingTheatersInput) {
      addInputCounter(openingTheatersInput, "theaters");
      openingTheatersInput.addEventListener("input", function () {
        validateInput(this);
        updatePredictButton();
      });
    }

    if (releaseDaysInput) {
      addInputCounter(releaseDaysInput, "days");
      releaseDaysInput.addEventListener("input", function () {
        validateInput(this);
        updatePredictButton();
      });
    }

    // Form submission
    form.addEventListener("submit", function (e) {
      const openingTheaters = document.getElementById("opening_theaters").value;
      const releaseDays = document.getElementById("release_days").value;

      if (openingTheaters <= 0 || releaseDays <= 0) {
        e.preventDefault();
        showError("Opening theaters and release days must be greater than 0");
        return false;
      }

      // Show loading state
      const submitBtn = form.querySelector('button[type="submit"]');
      submitBtn.innerHTML = "<span>⏳ Predicting...</span>";
      submitBtn.disabled = true;

      // Add loading spinner
      showLoadingSpinner();
    });

    // Genre selection counter
    const genreCheckboxes = document.querySelectorAll('input[name="genres"]');
    const genreCounter = document.createElement("div");
    genreCounter.className = "input-counter";
    genreCounter.id = "genre-counter";
    genreCounter.textContent = "No genres selected";

    const genreGrid = document.querySelector(".genre-grid");
    if (genreGrid) {
      genreGrid.parentNode.insertBefore(genreCounter, genreGrid.nextSibling);

      genreCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener("change", function () {
          updateGenreCounter();
          updatePredictButton();
        });
      });
    }
  }

  // Add animation to checkboxes
  const checkboxes = document.querySelectorAll(".genre-checkbox");
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("click", function () {
      this.style.transform = "scale(0.95)";
      setTimeout(() => {
        this.style.transform = "scale(1)";
      }, 100);
    });
  });

  // Auto-format number inputs
  const numberInputs = document.querySelectorAll('input[type="number"]');
  numberInputs.forEach((input) => {
    input.addEventListener("blur", function () {
      if (this.value) {
        this.value = parseInt(this.value).toLocaleString();
      }
    });

    input.addEventListener("focus", function () {
      this.value = this.value.replace(/,/g, "");
    });
  });
});

// Helper Functions
function validateInput(input) {
  const value = parseFloat(input.value);

  if (isNaN(value) || value <= 0) {
    input.classList.remove("valid");
    input.classList.add("invalid");
    return false;
  } else {
    input.classList.remove("invalid");
    input.classList.add("valid");
    return true;
  }
}

function addInputCounter(input, unit) {
  const counter = document.createElement("div");
  counter.className = "input-counter";
  counter.id = `${input.id}-counter`;
  input.parentNode.appendChild(counter);

  input.addEventListener("input", function () {
    const value = parseInt(this.value);
    if (!isNaN(value) && value > 0) {
      counter.textContent = `${value.toLocaleString()} ${unit}`;
    } else {
      counter.textContent = `Enter number of ${unit}`;
    }
  });
}

function updateGenreCounter() {
  const selectedGenres = document.querySelectorAll(
    'input[name="genres"]:checked',
  );
  const counter = document.getElementById("genre-counter");

  if (counter) {
    if (selectedGenres.length === 0) {
      counter.textContent = "No genres selected";
      counter.style.color = "#999";
    } else if (selectedGenres.length === 1) {
      counter.textContent = "1 genre selected";
      counter.style.color = "#667eea";
    } else {
      counter.textContent = `${selectedGenres.length} genres selected`;
      counter.style.color = "#667eea";
    }
  }
}

function updatePredictButton() {
  const form = document.getElementById("predictionForm");
  if (!form) return;

  const submitBtn = form.querySelector('button[type="submit"]');
  const requiredInputs = form.querySelectorAll("[required]");
  let allValid = true;

  requiredInputs.forEach((input) => {
    if (input.type === "checkbox" || input.type === "radio") {
      return; // Skip checkboxes for required validation
    }
    if (
      !input.value ||
      (input.type === "number" && parseFloat(input.value) <= 0)
    ) {
      allValid = false;
    }
  });

  if (allValid) {
    submitBtn.classList.add("ready");
  } else {
    submitBtn.classList.remove("ready");
  }
}

function showError(message) {
  // Create error toast
  const toast = document.createElement("div");
  toast.className = "error-toast";
  toast.textContent = message;
  toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #f44336;
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = "fadeOut 0.3s ease-out";
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 300);
  }, 3000);
}

function showLoadingSpinner() {
  const form = document.getElementById("predictionForm");
  if (!form) return;

  const spinner = document.createElement("div");
  spinner.className = "loading-spinner";
  spinner.style.display = "block";
  spinner.innerHTML =
    '<div class="spinner"></div><p>Analyzing movie data...</p>';

  form.appendChild(spinner);
}

// Add smooth scroll to top on page load
window.addEventListener("load", function () {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});

// Add entrance animation to form
setTimeout(() => {
  const formContainer = document.querySelector(".form-container");
  if (formContainer) {
    formContainer.style.opacity = "0";
    formContainer.style.transform = "translateY(30px)";

    setTimeout(() => {
      formContainer.style.transition = "all 0.6s ease-out";
      formContainer.style.opacity = "1";
      formContainer.style.transform = "translateY(0)";
    }, 100);
  }
}, 100);
