// ===============================
// FETCH USER SESSION DATA
// ===============================
async function getUser() {
  try {
    const response = await fetch(
      "http://localhost:5000/api/user/dashboard",
      {
        method: "GET",
        credentials: "include" // IMPORTANT
      }
    );

    if (!response.ok) {
      // If not logged in → redirect to login
      window.location.href = "login.html";
      return;
    }

    const data = await response.json();
    document.getElementById("username").textContent = data.user.name;

  } catch (error) {
    console.error(error);
    window.location.href = "login.html";
  }
}

// ===============================
// GAME NAVIGATION
// ===============================
function goToGame(gamePage) {
  window.location.href = gamePage;
}

// ===============================
// LOGOUT
// ===============================
async function logout() {
  await fetch("http://localhost:5000/api/auth/logout", {
    method: "POST",
    credentials: "include"
  });

  window.location.href = "login.html";
}

// Load user when page opens
getUser();
