let mongoose = require('mongoose');

// Connect to mongoDB
mongoose.connect('mongodb://localhost/MS3DB', {useNewUrlParser:true});

mongoose.connection.once('open', function() {
    console.log('Connection has been made.');
}).on('error', function(error) {
    console.log("Connection error: Couldn't establish a connection.");
});
