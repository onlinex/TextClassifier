// back end web application
const express = require('express');
// logger
const morgan = require('morgan');
// filesystem
const fs = require('fs');
const path = require('path');
// cross-origin resource sharing
const cors = require('cors');
// connect env file
const dotenv = require('dotenv');
// data parser
const bodyParser = require('body-parser');


// config env variables
dotenv.config();

// define framwork
const app = express();
// define static directory
app.use(express.static(path.join(__dirname, 'public')));
// use cors
app.use(cors());
// connect json
app.use(bodyParser.json());

// setup the logger
app.use(morgan('common', {
    // stream write to file
    stream: fs.createWriteStream(path.join(__dirname, 'access.log'), { flags: 'a'})
}));

// get an environment variable
const PORT = process.env.PORT || 3000;
// start server
app.listen(PORT, () => {
    console.log(`App is listening port ${PORT}`)
});

// serve post request
app.post('/query', async (req, res) => {
    try {
        const json = req.body;

        console.log(json);

        res.status(200).send();

    } catch(error) {
        console.log(error);
        res.status(500).send(error);
    }
});