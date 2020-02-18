import React, { Component } from 'react';
import { Router, Route, Switch } from "react-router-dom";
import { createBrowserHistory } from "history";
import {Provider} from "mobx-react";

import NavBar from "./views/navbar/NavBar";
import stores from "./stores";


const history = createBrowserHistory();

class App extends Component {
    render() {
        const {projectCollection, datasetCollection, libraryCollection} = stores.collections;
        const {imageModel, videoModel} = stores.models;
        return (
            <Provider
                projectCollection={projectCollection}
                datasetCollection={datasetCollection}
                libraryCollection={libraryCollection}
                imageModel={imageModel}
                videoModel={videoModel}
            >
                <Router history={history}>
                    <NavBar />
                    <Switch>
                        {this.props.routes.map((route, i) => (
                            <RouteWithSubroutes key={i} {...route} />
                        ))}
                    </Switch>
                </Router>
            </Provider>
        );
    }
}

function RouteWithSubroutes(route) {
    return (
        <Route
            path={route.path}
            render={props => (
                <route.component {...props} routes={route.routes} />
            )}
        />
    );
}

export default App;
