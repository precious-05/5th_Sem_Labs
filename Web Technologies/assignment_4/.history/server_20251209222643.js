const express = require("express");
// Syntax for importing any library in Node.js
// require() = CommonJS module import, express = library
// Loading express framework to create web server

const app = express();
// This is the server object for creating routes, starting server, using middlewear

const path = require("path");
// "Path" is built-in module of Node.js
// It combines paths in correct file formats and also resolves windows VS linux path issyes

const PORT = 3000;
// Only tells on which port server will run

