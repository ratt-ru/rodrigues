"use strict";

const API_BASE_URL = "http://localhost:8000/scheduler/rest";

var agent = require("superagent");

var Api = {
    get: function(path, query = {}, done) {
        if (!done) return Api.get(path, {}, done);
        agent.get(`${API_BASE_URL}${path}`, query, done);
    },

    post: function(path, body, done) {
        agent.get(`${API_BASE_URL}${path}`, body, done);
    }
}

module.exports = Api;