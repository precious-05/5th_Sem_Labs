const message = document.getElementById("message");

/* ======================
   SIGNUP FUNCTION
====================== */
const signupForm = document.getElementById("signupForm");

if (signupForm) {
  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("http://localhost:5000/api/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
      });

      const data = await response.json();

      if (response.ok) {
        message.textContent = data.message;
        message.className = "success";
        signupForm.reset();
      } else {
        message.textContent = data.message;
        message.className = "error";
      }

    } catch (error) {
      message.textContent = "Server error";
      message.className = "error";
    }
  });
}

/* ======================
   LOGIN FUNCTION
====================== */
const loginForm = document.getElementById("loginForm");

if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    try {
      const response = await fetch("http://localhost:5000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include", // IMPORTANT for session
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (response.ok) {
        message.textContent = data.message;
        message.className = "success";

        // Redirect based on role
        setTimeout(() => {
          if (data.user.role === "admin") {
            window.location.href = "admin.html";
          } else {
            window.location.href = "dashboard.html";
          }
        }, 1000);

      } else {
        message.textContent = data.message;
        message.className = "error";
      }

    } catch (error) {
      message.textContent = "Server error";
      message.className = "error";
    }
  });
}
