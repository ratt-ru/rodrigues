"use strict";

import React, {Component} from 'react';

var authStore = require("../store/auth");
var authActions = require("../action/auth");

export default class App extends Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    onChange(e) {
        var {name, value} = e.target;
        var state = this.state;
        state[name] = value;

        this.setState(state);
    }

    onSubmit(e) {
        e.preventDefault();
        authActions.login(this.state);
    }

    render() {
        if (authStore.username)
            return <div>You are logged in</div>;

        return (
            <form onSubmit={this.onSubmit.bind(this)}>
                <input onChange={this.onChange.bind(this)} type="text" name="username" />
                <input onChange={this.onChange.bind(this)} type="password" name="password" />
                <input type="submit" value="login" />
            </form>
        );
    }
}






