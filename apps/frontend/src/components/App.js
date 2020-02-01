import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import React, { Component, Fragment, Suspense, lazy } from 'react';
import ReactDOM from "react-dom";

import NavBar from "./layout/navbar/NavBar";
import Home from "./layout/Home";
import Project from "./layout/Project";
import Dataset from "./layout/Dataset";
import Annotator from "./layout/Annotator";
import NotFound from "./layout/NotFound";

class App extends Component {
    render() {
        return (
            <Router>
                <NavBar />
                <Switch>
                    <Route exact path="/" component={Home} />
                    <Route exact path="/projects" component={Project} />
                    <Route exact path="/datasets" component={Dataset} />
                    <Route exact path="/annotator" component={Annotator} />
                    <Route exact path="/404" component={NotFound} />
                    <Redirect to="/404" />
                </Switch>
            </Router>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('startsmart'));
