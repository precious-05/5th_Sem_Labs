const express = require("express");
const router = express.Router();

const isAuthenticated = require("../middleware/authMiddleware");

// Protected dashboard route
router.get("/dashboard", isAuthenticated, (req, res) => {
  res.json({
    message: "Welcome to user dashboard",
    user: req.session.user
  });
});

module.exports = router;
