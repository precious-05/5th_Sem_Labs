// ROLE-BASED ADMIN AUTHORIZATION
const isAdmin = (req, res, next) => {
  if (req.session && req.session.user && req.session.user.role === "admin") {
    next(); // Admin verified → allow access
  } else {
    res.status(403).json({ message: "Access denied. Admins only." });
  }
};

module.exports = isAdmin;
