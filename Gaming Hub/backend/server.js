const express = require("express");
const dotenv = require("dotenv");
const session = require("express-session");
const connectDB = require("./config/db");
const cors = require("cors");
const authRoutes = require("./routes/authRoutes");
const userRoutes = require("./routes/userRoutes");
const adminRoutes = require("./routes/adminRoutes");

dotenv.config(); // Load .env variables

const app = express();

// =======================
// MIDDLEWARE
// =======================

// Parse JSON and form data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Enable CORS for frontend running at http://localhost:3000
app.use(cors({
  origin: "http://localhost:3000",
  credentials: true
}));

// Session middleware
app.use(
  session({
    secret: process.env.SESSION_SECRET || "secret",
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false } // set true if using HTTPS
  })
);

// =======================
// ROUTES
// =======================
app.use("/api/auth", authRoutes);
app.use("/api/user", userRoutes);
app.use("/api/admin", adminRoutes);

// =======================
// CONNECT MONGODB
// =======================
connectDB();

// =======================
// OPTIONAL: Create initial admin
// =======================
const User = require("./models/User");
const bcrypt = require("bcryptjs");

// async function createAdmin() {
//   const admin = await User.findOne({ role: "admin" });
//   if (!admin) {
//     const salt = await bcrypt.genSalt(10);
//     const hashed = await bcrypt.hash("admin123", salt);
//     await User.create({
//       name: "Admin User",
//       email: "admin@gmail.com",
//       password: hashed,
//       role: "admin"
//     });
//     console.log("Initial admin created: admin@gmail.com / admin123");
//   }
// }

// Uncomment to create admin on first run
// createAdmin();

// =======================
// START SERVER
// =======================
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
