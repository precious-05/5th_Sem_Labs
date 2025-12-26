const express = require("express");
const router = express.Router();

const {
  getAllUsers,
  updateUser,
  deleteUser
} = require("../controllers/adminController");

const isAdmin = require("../middleware/adminMiddleware");

// Protect all routes
router.use(isAdmin);

// View all users
router.get("/users", getAllUsers);

// Update user
router.put("/users/:id", updateUser);

// Delete user
router.delete("/users/:id", deleteUser);

module.exports = router;
