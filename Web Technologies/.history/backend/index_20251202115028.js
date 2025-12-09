// server.js

const express = require("express");
const app = express();
const PORT = 3000;

// Middleware to parse JSON request body
app.use(express.json());

// Sample route
app.get("/", (req, res) => {
    res.send("Server is running successfully!");
});

// Example API route
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
