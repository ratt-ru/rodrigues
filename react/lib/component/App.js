"use strict";

var React = require("react");
var { Link } = require("react-router");

var callAction = require("../util/call-action");
var jobActions = require("../action/job");
var jobStore = require("../store/job");

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    componentDidMount() {
        jobStore.observe(this.setState.bind(this));
        callAction(jobActions.list);
    }

    componentWillUnmount() {
        jobStore.stopObserving(this.setState);
    }

    render() {
        if (!this.state.jobs)
            return null;

        return (
            <div>
                <Link to="/login">login</Link>
                <h1>Hello, World!</h1>
                {this.state.jobs.map((job) => {
                    return <div key={job.url}>{job.name}</div>
                })}
            </div>
        );
    }
}
