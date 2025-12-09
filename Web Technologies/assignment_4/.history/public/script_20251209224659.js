// Form Validation and Savig the data
if (window.location.pathname.includes("index.html")) {

    document.getElementById("regForm").addEventListener("submit", function (e) {
        e.preventDefault();

        let name = document.getElementById("name").value.trim();
        let email = document.getElementById("email").value.trim();
        let age = document.getElementById("age").value;

        // Validation
        if (name === "") {
            alert("Name cannot be empty");
            return;
        }
        if (!email.includes("@")) {
            alert("Email must contain '@'");
            return;
        }
        if (age <= 0) {
            alert("Age must be greater than 0");
            return;
        }

        // Get previous data or empty
        let students = JSON.parse(localStorage.getItem("students")) || [];

        // Add new student
        students.push({ name, email, age });

        // Save back
        localStorage.setItem("students", JSON.stringify(students));

        // Redirect to next page
        window.location.href = "students.html";
    });
}



// PAGE 2 — DISPLAY DATA
if (window.location.pathname.includes("students.html")) {

    let students = JSON.parse(localStorage.getItem("students")) || [];
    let table = document.getElementById("studentsTable");

    students.forEach(std => {
        let row = document.createElement("tr");

        row.innerHTML = `
            <td>${std.name}</td>
            <td>${std.email}</td>
            <td>${std.age}</td>
        `;

        table.appendChild(row);
    });
}
