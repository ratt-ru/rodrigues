"use strict";

var Client = require("../api/client");
var authStore = require("../store/auth");

var UserActions = {
    login: function(payload, done) {
        Client.post("/auth/login", payload, function(err){
            if (err) return done(err);

            // fill authstore

        });
    }
}
