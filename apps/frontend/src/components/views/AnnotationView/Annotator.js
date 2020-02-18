import React, {Component} from 'react';
import Dashboard from "./dashboard/Dashboard";
import {inject, observer} from "mobx-react";


@inject('imageModel', 'videoModel')
@observer
class Annotator extends Component {
    datasetID = this.props.match.params.datasetID;

    constructor(props) {
        super(props);
        this.state = {
            isLoaded: false,
            progress: 0,
            items: [],
            landmarks: [],
            index: 0
        }
    }

    componentDidMount() {
        this.props.imageModel.fetch(this.datasetID)
            .then((value) => {
                this.setState({
                    items: value,
                    progress: 50,
                });
            }).finally(() => {
                this.setState({
                    isLoaded: true,
                    progress: 100,
                });
            });
    }

    render() {
        return (
            <div id="annotator">
                <Dashboard
                    items={this.state.items}
                    isLoaded={this.state.isLoaded}
                    progress={this.state.progress}
                    index={this.state.index}
                />
            </div>
        );
    }
}

export default Annotator;