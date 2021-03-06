import React, { Component } from "react";
import {inject, observer} from "mobx-react";
import {Intent} from "@blueprintjs/core/lib/cjs/common/intent";
import {Button, ButtonGroup, FormGroup, InputGroup} from "@blueprintjs/core";
import Project from "./Project";
import API from "api";
import CreateProjectPopup from "./CreateProjectPopup";
import AddCard from "../utils/AddCard";

@inject("projectCollection")
@observer
class ProjectCollectionView extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isCreateAlertOpened: false,
            isOpenCreate: false,
        }
    }

    componentDidMount() {
        this.props.projectCollection.fetchAll();
    }

    addProjectButton = e => {
        e.preventDefault();
        this.props.projectCollection.add({
            name: document.getElementById("project-name-create").value,
        });

        document.getElementById("project-name-create").value = null;

        this.setState({
            isOpenCreate: false,
        });
    };

    addProjectKeyPress = (e) => {
        if (e.key === 'Enter') {
            this.props.projectCollection.add({
                name: e.target.value,
            });

            e.target.value = null;

            this.setState({
                isOpenCreate: false,
            });
        }
    };

    handleChange = () => {
        const isChecked = !this.state.isChecked;
        this.setState({
            isChecked: isChecked
        });
    };

    handlePopoverClick = () => {
        const isPopoverOpened = !this.state.isPopoverOpen;
        this.setState({
            isPopoverOpened: isPopoverOpened
        });
    };

    handleDeleteClick = () => {
        const isDeletionAlertOpened = !this.state.isDeletionAlertOpened;
        this.setState({
            isDeletionAlertOpened: isDeletionAlertOpened
        });
    };

    handleMoveCancel = () => {
        this.setState({
            isDeletionAlertOpened: false
        });
    };

    handleMoveDeletion = () => {
        this.props.projectCollection.delete(this.props.url);
        this.setState({
            isDeletionAlertOpened: false
        });
    };

    handleCardClick = (e) => {
        e.stopPropagation();
        this.setState({
            redirect: true,
            selected: API.retrievePathID(this.props.url)
        });
    };

    handleEditClick = () => {
        this.setState({
            isEditMode: true
        });
    };

    handleKeyPress = (e) => {
        this.props.projectCollection.update(this.props.url, {
            name: document.getElementById("project-name-edit").value,
        });
        if (e.key === 'Enter') {
            this.setState({
                isEditMode: false
            })
        }
    };

    handleCreateCardClick = (e) => {
        e.stopPropagation();
        this.setState({
            isOpenCreate: true,
        });
    };

    render() {
        const projects = this.props.projectCollection.all;


        return (
            <div id="project-collection" className="container-fluid m-3" style={{"height": document.documentElement.clientHeight*0.7}}>
                <h1 className="text-center">Projects</h1>

                <FormGroup labelFor="projects-form">
                    <div className="d-flex align-items-center" style={{height: "54vh"}} >
                        {projects.slice().map( (info, i) =>
                            <Project key={i} {...info} />
                        )}
                        <AddCard
                            name={`Project`}
                            onClick={this.handleCreateCardClick}
                            isOpenCreate={this.state.isOpenCreate}
                            onCreate={this.addProjectButton}
                            onKeyPress={this.addProjectKeyPress}
                        />
                    </div>
                </FormGroup>
            </div>
        );
    }
}

export default ProjectCollectionView;