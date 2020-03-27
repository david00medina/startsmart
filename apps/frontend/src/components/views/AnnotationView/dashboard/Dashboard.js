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

            let item;
            let image;

            if ('image' === this.props.type) {
                item = this.props.items[this.props.index];
                image = item.uri;
            } else if ('video' === this.props.type) {
                item = this.props.items[0];
                image = item.uri;
            }

            return (
                <div id="dashboard">
                    <TopToolbar
                        filename={item.filename}
                        index={this.props.index}
                        onClickPrevious={this.props.onClickPrevious}
                        onClickNext={this.props.onClickNext}
                    />
                    <div>
                        <div className="row">

                            <div id="middle-section" className="col-10 align-content-center">
                                <div id="canvas">
                                    <Canvas
                                        image={image}
                                        roi={[840, 220, 840, 240, 860, 240, 860, 260, 820, 260]}
                                    />
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            );
        }
    }
}

export default Dashboard;