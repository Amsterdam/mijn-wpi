/**
 *
 * This is a script to test the throttle functionality.
 * This is expected to be ran on the focus docker container
 * It does many requests in one second, and prints the status code returned.
 *
 */

var http = require('http');

var reqsPerSecond = 60;
var startCounter = 0;
var doneCounter = 0;

function makeCall () {
    var options = {
        hostname: 'localhost',
        post: 8000,
        path: '/focus/aanvragen',
        method: 'GET',
        agent: false
    };

    var req = http.request(options, function (res) {
        res.on('data', (d) => {
            doneCounter += 1;
            console.log(res.statusCode);
            console.log('>> requests:', doneCounter, ' took:', (Date.now() - start) / 1000, ' seconds');
        });
    });

    req.end();

    startCounter += 1;
    if (startCounter >= reqsPerSecond) {
        clearTimeout(interval);
    }
}

var start = Date.now();

var interval = setInterval(makeCall, reqsPerSecond / 60);
