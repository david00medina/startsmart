import React, {Component} from 'react';

import styles from '../../../../static/css/layout/dashboard/vertical-toolbar.module.css'

import TopToolbar from "./topbar/TopToolbar";
import ProgressBar from "../utils/ProgressBar";
import VerticalToolbar from "./VerticalToolbar";
import Canvas from "./canvas/Canvas";

class Dashboard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoaded: false,
            progress: 50,
            items: [],
            landmarks: []
        }
    }

    componentDidMount() {
        fetch('startsmart/api/image', {
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
           }
        }).then(res => res.json()).then(json => {
                this.setState({
                    isLoaded: true,
                    items: json
                });
        });
    }

    render() {
        let { isLoaded, items } = this.state;

        if (!isLoaded) {
            return (
                <div className="container-fluid center">
                    <ProgressBar progress={this.state.progress} />
                </div>
            )
        } else {
            let item = items[8];

            return (
                <div id="dashboard">
                    <TopToolbar item={item.uri} />
                    <div>
                        <div className="row">

                            <div id="left-section" className="pl-2">
                                <VerticalToolbar />
                            </div>

                            <div id="middle-section" className="col-9 align-content-center">
                                <div id="canvas">
                                    <Canvas image={item} />
                                </div>
                            </div>

                            <div id="right-section" className="col-2">
                                <p>Hola amigo como estas? bien?</p>
                            </div>

                        </div>
                    </div>
                </div>
            );
        }
    }
}

export default Dashboard;