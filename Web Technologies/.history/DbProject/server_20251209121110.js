const express = require('express');
const usermodel = require('./user_data');


const app = express();
const port = 3000;  //We can add any number to this port


app.get('/', (req,res) =>    //http request 
{
    res.send('Welcome to User Data API');

})

const Port = port;
app.listen(port, () => {
    console.log("Server is running on http://localhost:${port}");
})

// const Port = port;


app.get('/create', async(req,res) =>    //http request , create is used to create user
{
    const created_user = await new usermodel 
    ({
        name : "Alina",
        email : "alina@gmail.com",
        age : 20
    })

    res.send(created_user)

});