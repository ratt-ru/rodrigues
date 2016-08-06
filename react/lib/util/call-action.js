"use strict";

function defaultErrorHandler(err) {
    // could do something useful here,
    // like storing the error and displaying
    if (err) console.error(err);
}

function callAction(action, payload = {}, done = defaultErrorHandler ) {
    action.call(null, payload, done);
}

module.exports = callAction;
