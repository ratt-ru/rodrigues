"use strict";

module.exports.create = function create(name) {
    var ctor = function(name){
        let observers = [];
        let state = {};

        const store =  {
            get name() {
                return name;
            },

            get state() {
                return Object.assign({}, state);
            },

            set: function(name, value) {
                state[name] = value;

                observers.forEach(function(fn){
                    fn(Object.assign({}, state));
                });
            },

            get: function(name) {
                return state[name];
            },

            observe: function(observer) {
                observers.push(observer);
            },

            stopObserving: function(observer) {
                observers.splice(observers.indexOf(observer), 1);
            }
        };

        return store;
    };

    return ctor;
}


