import React, {Component} from 'react';
import Dashboard from "./dashboard/Dashboard";
import {inject, observer} from "mobx-react";
import API from "api";


@inject('imageModel', 'videoModel')
@observer
class Annotator extends Component {
    datasetID = this.props.match.params.datasetID;

    constructor(props) {
        super(props);
        this.state = {
            isLoaded: false,
            progress: 0,
            type: null,
            items: [],
            landmarks: [],
            index: 0
        }
    }

    componentDidMount() {
        this.props.imageModel.fetch(this.datasetID)
            .then((value) => {
                if (value.length !== 0) {
                    this.setState({
                        type: 'image',
                        items: value,
                        progress: 50,
                    });
                }
            }).finally(() => {
                if (this.state.items.length !== 0) {
                    this.setState({
                        isLoaded: true,
                        progress: 100,
                    });
                }
            });

        this.props.videoModel.fetch(this.datasetID)
            .then((value) => {
                if (value.length !== 0) {
                    this.setState({
                        type: 'video',
                        items: value,
                        progress: 50,
                    });
                }
            }).finally(() => {
                if (this.state.items.length !== 0) {
                    this.setState({
                        isLoaded: true,
                        progress: 100,
                    });
                }
        });
    }

    render() {
        if (this.state.type !== null) {

            let item;
            if (this.state.type === 'image') {
                item = this.props.imageModel.data;
            } else if (this.state.type === 'video') {
                item = this.props.videoModel.data;
            }

            API.post('detect', {
                type: this.state.type,
                item: item,
            });
        }

        return (
            <div id="annotator">
                <Dashboard
                    items={this.state.items}
                    type={this.state.type}
                    isLoaded={this.state.isLoaded}
                    progress={this.state.progress}
                    index={this.state.index}
                />
            </div>
        );
    }
}

export default Annotator;