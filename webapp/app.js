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
// data parser (enabling to send json)
const bodyParser = require('body-parser');
// promise based http client
const axios = require('axios');
// http and https
const http = require('http');
const https = require('https');

// SSL/TLS setup
try {
    var private_key = fs.readFileSync('/etc/ssl/notio/private_key.key', 'utf8');
    var certificate = fs.readFileSync('/etc/ssl/notio/certificate.pem', 'utf8');
} catch(error) {
    console.log('SSL certificates not found')
    var private_key = '';
    var certificate = '';
}

var credentials = {key: private_key, cert: certificate};


// config env variables
dotenv.config();

// define framwork
const app = express();
// trust Nginx proxy
app.enable("trust proxy");
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
const PORT_HTTP = process.env.PORT_HTTP || 8081;
const PORT_HTTPS = process.env.PORT_HTTPS || 8444;
// create httpServer
http.createServer(app).listen(PORT_HTTP, (error) => {
    if(error) {
        console.log('App failed to start', error);
    } else {
        console.log(`App is listening port ${PORT_HTTP}`);
    }
});
// create httpsServer
https.createServer(credentials, app).listen(PORT_HTTPS, (error) => {
    if(error) {
        console.log('App failed to start', error);
    } else {
        console.log(`App is listening port ${PORT_HTTPS}`)
    }
});


const URL = "http://127.0.0.1:5000";

// serve post request
app.post('/query', async (req, res) => {
    try {
        // get json
        const json = req.body;
        // form request to the model
        axios.post(URL, json).then(response => {
            // send response back to the client
            res.status(200).send(response.data);
        }).catch(error => {
            res.status(503).send(error);
        });

    } catch(error) {
        console.log(error);
        res.status(500).send(error);
    }
});