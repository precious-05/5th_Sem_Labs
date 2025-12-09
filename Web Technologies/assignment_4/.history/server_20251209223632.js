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


app.use(express.static(path.join(__dirname, "public")));
//This tells browser , "public" folder ke andar jo bhi files hain unko browser ko directly de do
// Example: Browser me agar hm likhen  http://localhost:3000/index.html to express automatically public/index.html return karega

/*

JS Concept:

app.use() = middleware
express.static() = built-in middleware
path.join() = creating safe path
__dirname = current folder's path

Why Necessary? Because here is no backend logic just website static pages (HTML, CSS, JS) are being used 


*/



// ROUTE / ENDPOINT (API Concept)


















const express = require("express");
const app = express();
const path = require("path");

const PORT = 3000;

// Make the public folder static
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
