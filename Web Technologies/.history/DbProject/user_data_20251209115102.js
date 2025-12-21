const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/Practice');

const userSchema = new mongoose.Schema({
    name: String,
    email: String,
    age: Number
})


const User = mongoose.model('user', userSchema);