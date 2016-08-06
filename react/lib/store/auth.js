"use strict";

let Store = require("./lib/store");
let AuthStore = Store.create("Auth");
let instance = AuthStore();

module.exports = instance;