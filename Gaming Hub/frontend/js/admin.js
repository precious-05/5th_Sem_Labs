const adminNameSpan = document.getElementById("adminName");
const usersTableBody = document.querySelector("#usersTable tbody");

// ===============================
// LOAD ADMIN NAME AND USERS
// ===============================
async function loadAdmin() {
  try {
    const res = await fetch("http://localhost:5000/api/user/dashboard", {
      credentials: "include"
    });

    if (!res.ok) {
      window.location.href = "login.html";
      return;
    }

    const data = await res.json();
    if (data.user.role !== "admin") {
      alert("Access denied. Admins only.");
      window.location.href = "login.html";
      return;
    }

    adminNameSpan.textContent = data.user.name;
    loadUsers();

  } catch (error) {
    console.error(error);
    window.location.href = "login.html";
  }
}

// ===============================
// FETCH ALL USERS
// ===============================
async function loadUsers() {
  try {
    const res = await fetch("http://localhost:5000/api/admin/users", {
      credentials: "include"
    });

    const users = await res.json();

    usersTableBody.innerHTML = "";

    users.forEach(user => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${user.name}</td>
        <td>${user.email}</td>
        <td>${user.role}</td>
        <td>
          <button class="update" onclick='updateUser("${user._id}")'>Update</button>
          <button class="delete" onclick='deleteUser("${user._id}")'>Delete</button>
        </td>
      `;

      usersTableBody.appendChild(tr);
    });

  } catch (error) {
    console.error(error);
  }
}

// ===============================
// UPDATE USER (prompt for simplicity)
// ===============================
async function updateUser(id) {
  const name = prompt("Enter new name:");
  const email = prompt("Enter new email:");
  const role = prompt("Enter role (user/admin):");

  try {
    const res = await fetch(`http://localhost:5000/api/admin/users/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ name, email, role })
    });

    const data = await res.json();
    alert(data.message);
    loadUsers();

  } catch (error) {
    console.error(error);
  }
}

// ===============================
// DELETE USER
// ===============================
async function deleteUser(id) {
  if (!confirm("Are you sure you want to delete this user?")) return;

  try {
    const res = await fetch(`http://localhost:5000/api/admin/users/${id}`, {
      method: "DELETE",
      credentials: "include"
    });

    const data = await res.json();
    alert(data.message);
    loadUsers();

  } catch (error) {
    console.error(error);
  }
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

// Initialize
loadAdmin();
