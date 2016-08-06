"use strict";

let Store = require("./lib/store");
let JobStore = Store.create("Job");
let instance = JobStore();

module.exports = instance;