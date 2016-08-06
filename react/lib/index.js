import React from 'react';
import {render} from 'react-dom';
import App from './component/App';
import Login from "./component/login";
import { Router, Route, browserHistory } from 'react-router'

render((
    <Router history={browserHistory}>
      <Route path="/" component={App}/>
      <Route path="/login" component={Login}/>
    </Router>
), document.getElementById('root'))
