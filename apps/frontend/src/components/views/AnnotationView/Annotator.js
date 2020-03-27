import React, {Component} from 'react';
import Dashboard from "./dashboard/Dashboard";
import {inject, observer} from "mobx-react";
import API from "api";


@inject('imageModel', 'videoModel', 'annotationCollection')
@observer
class Annotator extends Component {
    projectID = this.props.match.params.projectID;
    datasetID = this.props.match.params.datasetID;

    constructor(props) {
        super(props);
        this.state = {
            firstRendered: true,
            isLoaded: false,
            progress: 0,
            type: null,
            items: [],
            image: null,
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
                        firstRendered: false,
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
                        firstRendered: false,
                        isLoaded: true,
                        progress: 100,
                    });
                }
        });

        this.props.annotationCollection.fetchAll(1);
    }

    onClickPrevious = (e) => {
        e.preventDefault();

        let index = this.state.index - 1;
        if (index < 0 && this.state.type === 'image') {
            index = this.state.items.length - 1;
        } else if (index < 0 && this.state.type === 'video') {
            index = this.state.items[0].total_frames - 1;
        }

        this.setState({
            index: index,
        });
    };

    onClickNext = (e) => {
        e.preventDefault();

        let index = this.state.index + 1;
        if (index > (this.state.items.length-1) && this.state.type === 'image') {
            index = 0;
        } else if (index > (this.state.items[0].total_frames-1) && this.state.type === 'video') {
            index = 0;
        }

        this.setState({
            index: index,
        });
    };

    render() {
        if (this.state.type !== null && this.state.firstRendered) {
            this.process();
            this.load_frame();
        }

        return (
            <div id="annotator">
                <Dashboard
                    items={this.state.items}
                    image={this.state.image}
                    type={this.state.type}
                    isLoaded={this.state.isLoaded}
                    progress={this.state.progress}
                    index={this.state.index}
                    onClickPrevious={this.onClickPrevious}
                    onClickNext={this.onClickNext}
                />
            </div>
        );
    }

    process() {
        let items = this.state.type === 'image' ? this.props.imageModel.data : this.props.videoModel.data;
        let total_items = this.state.type === 'image' ? items.length -1 : items[0].total_frames;

        let data = {
            project: this.projectID,
            dataset: this.datasetID,
            predictor: 'Openpose',
            width: 1136,
            height: 640,
            index: total_items,
        };
        data[this.state.type === 'image' ? 'image' : 'video'] = items.slice().map((item, i) => {
            return API.retrievePathID(item.url);
        });

        this.props.annotationCollection.add(data);
    }

    load_frame() {
        let item = this.props.videoModel.data[0];
        /*let response = this.props.videoModel.get_frame({
            video: API.retrievePathID(item.url),
            frame_no: this.state.index,
        });

        if (response.result === 'ok'){
            this.setState({
                image: response.image,
            });
        }*/
    }
}

export default Annotator;