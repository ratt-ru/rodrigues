"use strict";

var Api = require("../api/client");
var jobStore = require("../store/job");

var jobActions = module.exports =  {
    list: function(payload, done) {
        Api.get("/jobs", {}, function(err, res){
            if (err) return done(err);

            jobStore.set("jobs", res.body);

            done();
        });
    }
};
