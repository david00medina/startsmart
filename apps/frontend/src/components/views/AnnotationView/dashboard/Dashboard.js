import React, {Component} from 'react';

import TopToolbar from "./topbar/TopToolbar";
import ProgressBar from "../../utils/ProgressBar";
import VerticalToolbar from "./VerticalToolbar";
import Canvas from "./canvas/Canvas";

class Dashboard extends Component {
    render() {
        if (!this.props.isLoaded) {
            return (
                <div className="container-fluid center">
                    <ProgressBar progress={this.props.progress} />
                </div>
            )
        } else {
            let item = this.props.items[this.props.index];
            return (
                <div id="dashboard">
                    <TopToolbar item={item.uri} />
                    <div>
                        <div className="row">

                            <div id="left-section" className="pl-2">
                                <VerticalToolbar />
                            </div>

                            <div id="middle-section" className="col-10 align-content-center">
                                <div id="canvas">
                                    <Canvas image={item} roi={[840, 220, 840, 240, 860, 240, 860, 260, 820, 260]} />
                                </div>
                            </div>

                            <div id="right-section" className="col-1">
                                <p>BARRA LATERAL</p>
                            </div>

                        </div>
                    </div>
                </div>
            );
        }
    }
}

export default Dashboard;