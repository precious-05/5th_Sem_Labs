// server.js

const express = require("express");
const app = express();
const path = require("path");
const PORT = 3000;

// Middleware to parse JSON request body
app.use(express.json());

// 👉 Serve the "public" folder (static files)
app.use(express.static("public"));

// 👉 Serve the toDo.html when user opens "/"
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "toDo.html"));
});

// Sample API route
app.get("/api/data", (req, res) => {
    res.json({
        message: "Here is your data",
        status: "success"
    });
});

// POST route example
app.post("/api/send", (req, res) => {
    const userData = req.body;
    res.json({
        received: userData,
        message: "POST request received!"
    });
});

// Start Server
app.listen(PORT, () => {
    console.log(`Server started at http://localhost:${PORT}`);
});