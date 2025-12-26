// AUTHENTICATION MIDDLEWARE

const isAuthenticated = (req, res, next) => {
  // Check if session exists and user is logged in
  if (req.session && req.session.user) {
    next(); // user is authenticated → continue
  } else {
    res.status(401).json({
      message: "Access denied. Please login first."
    });
  }
};

module.exports = isAuthenticated;
