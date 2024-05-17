// LOad the file temperature.json and parse it into a variable named temperature
const temperature = require ('./temperature.json');

// Sett the HTTPS module so that accepts self-signed certificates
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// Iterate through the temperature array and load each item into ElasticSearch using a simple HTTP request
const https = require ('https');

const options = {
  hostname: 'localhost',
  port: 9200,
  path: '/temperatures/_doc',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  auth: 'elastic:elastic'
};

Object.entries (temperature).forEach ((item) => {
  const req = https.request (options, (res) => {
    console.log (`statusCode: ${res.statusCode}`);
    res.on ('data', (d) => {
      process.stdout.write (d);
    });
  });
  req.on ('error', (error) => {
    console.error (error);
  });
  req.write (JSON.stringify ({date: item[0], temperature: item[1]}));
  req.end ();
});


