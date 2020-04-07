import React, { Component } from "react";
import {inject, observer} from "mobx-react";
import {FormGroup} from "@blueprintjs/core";

import CreateDatasetPopup from "./CreateDatasetPopup";
import AddCard from "../utils/AddCard";
import Dataset from "./Dataset";


@inject('datasetCollection', 'imageModel', 'videoModel')
@observer
class DatasetCollectionView extends Component {
    projectID = this.props.match.params.projectID;

    constructor(props) {
        super(props);

        this.bp3 = {
            nameRef: React.createRef(),
            selectRef: React.createRef(),
        };

        this.state = {
            isCreateAlertOpened: false,
            files: Array(0),
            isOpenCreate: false,
        };
    }

    componentDidMount() {
        this.props.datasetCollection.fetchAll(this.projectID);
    }

    addDatasetButton = (e) => {
        this.doAdd();
        this.bp3.nameRef.current.value = null;

        this.setState({
            isOpenCreate: false,
        });
    };

    addDatasetKeyPress = (e) => {
        if (e.key === 'Enter') {
            this.doAdd();
            e.target.value = null;

            this.setState({
                isOpenCreate: false,
            });
        }
    };

    doAdd = () => {
        this.props.datasetCollection.add({
            name: this.bp3.nameRef.current.value,
            project: this.projectID,
        }).then((res) => {
            this.state.files.slice().map((file, i) => {
                if (file.type.match('image.*')) {
                    this.props.imageModel.add({
                        dataset: this.props.datasetCollection.retrieveID(res.url),
                        license: null,
                        filename: file.name,
                        uri: file,
                        roi: null
                    });
                } else if (file.type.match('video.*')) {
                    this.props.videoModel.add({
                        dataset: this.props.datasetCollection.retrieveID(res.url),
                        license: null,
                        filename: file.name,
                        uri: file
                    });
                }
            });
        });
    };

    handleChangeStatus = ({file, meta}, status) => {
        if (status === "done") {
            let files = this.state.files;
            files.push(file);

            this.setState({
                file: files,
            });
        }
    };

    handleCreateCardClick = (e) => {
        e.stopPropagation();
        this.setState({
            isOpenCreate: true,
        });
    };

    render() {
        const datasets = this.props.datasetCollection.all;

        return (
            <div id="dataset-collection" className="container-fluid m-3" style={{"height": document.documentElement.clientHeight*0.7}}>
                <h1 className="text-center">Datasets</h1>

                <CreateDatasetPopup
                    {...this.bp3}
                    onChangeStatus={this.handleChangeStatus}
                    onClick={this.addDatasetButton}
                    onKeyPress={this.addDatasetKeyPress}
                    onInputChange={this.handleInputChange}
                />

                <FormGroup labelFor="dataset-form">
                    <div className="d-flex align-items-center" style={{height: "54vh"}}>
                        {datasets.slice().map( (info, i) =>
                            <Dataset key={i} projectID={this.projectID} {...info} />
                        )}
                        <AddCard
                            bp3={this.bp3}
                            name={`Dataset`}
                            onClick={this.handleCreateCardClick}
                            isOpenCreate={this.state.isOpenCreate}
                            onCreate={this.addDatasetButton}
                            onKeyPress={this.addDatasetKeyPress}
                            onInputChange={this.handleInputChange}
                            onChangeStatus={this.handleChangeStatus}
                        />
                    </div>
                </FormGroup>
            </div>
        );
    }
}

export default DatasetCollectionView;