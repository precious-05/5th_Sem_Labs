// Form Validation and Savig the data
if (window.location.pathname.includes("index.html")) {

    document.getElementById("regForm").addEventListener("submit", function (e) {
        e.preventDefault();

        let name = document.getElementById("name").value.trim();
        let email = document.getElementById("email").value.trim();
        let age = document.getElementById("age").value;

        // -- Validationn PART
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

        // Getting the previous data or  enpty
        let students = JSON.parse(localStorage.getItem("students")) || [];

        // Adding a new student
        students.push({ name, email, age });

        // Saving.---. back
        localStorage.setItem("students", JSON.stringify(students));

        // Redirecting    to thr next page
        window.location.href = "students.html";
    });
}



// DISPLAYING DATA
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
