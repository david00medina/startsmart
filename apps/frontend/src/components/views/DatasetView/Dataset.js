import React, {Component} from 'react';
import {
    Alert,
    Button,
    Card,
    Checkbox,
    Elevation,
    FormGroup,
    InputGroup,
    Intent,
    Menu, MenuItem,
    Popover
} from "@blueprintjs/core";
import {PopoverInteractionKind} from "@blueprintjs/core/lib/cjs/components/popover/popover";
import API from "../../../../lib/api";
import {inject, observer} from "mobx-react";
import {Redirect} from "react-router";


@inject('datasetCollection')
@observer
class Dataset extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isChecked: false,
            isPopoverOpened: false,
            isDeletionAlertOpened: false,
            isEditMode: false,
            redirect: false,
            selected: null,
        };
    }

    handleChange = (e) => {
        const isChecked = !this.state.isChecked;
        this.setState({
            isChecked: isChecked
        });
    };

    handlePopoverClick = (e) => {
        const isPopoverOpened = !this.state.isPopoverOpen;
        this.setState({
            isPopoverOpened: isPopoverOpened
        });
    };

    handleDeleteClick = (e) => {
        const isDeletionAlertOpened = !this.state.isDeletionAlertOpened;
        this.setState({
            isDeletionAlertOpened: isDeletionAlertOpened
        });
    };

    handleMoveCancel = (e) => {
        this.setState({
            isDeletionAlertOpened: false
        });
    };

    handleMoveDeletion = (e) => {
        this.props.datasetCollection.delete(this.props.url, this.props.projectID);
        this.setState({
            isDeletionAlertOpened: false
        });
    };

    handleCardClick = (e) => {
        this.setState({
            redirect: true,
            selected: API.retrievePathID(this.props.url)
        });
    };

    handleEditClick = (e) => {
        this.setState({
            isEditMode: true
        });
    };

    handleKeyPress = (e) => {
        this.props.datasetCollection.update(this.props.url, {
            name: document.getElementById("dataset-name-edit").value,
            project: this.props.projectID
        });

        if (e.key === 'Enter') {
            this.setState({
                isEditMode: false
            })
        }
    };

    renderAlert() {
        return (<Alert
            cancelButtonText="Cancel"
            confirmButtonText="Delete"
            icon="trash"
            intent={Intent.DANGER}
            isOpen={this.state.isDeletionAlertOpened}
            onCancel={this.handleMoveCancel}
            onConfirm={this.handleMoveDeletion}
            canEscapeKeyCancel={true}
        >
            <p>
                Are you sure you want to remove <b>{this.props.name}</b>?
            </p>
        </Alert>);
    }

    renderTitle() {
        if (!this.state.isEditMode) {
            return (
                <div className="col-8" onClick={this.handleCardClick}>
                    <h5 className="text-center m-1">{this.props.name}</h5>
                </div>
            );
        } else {
            return (
                <div className="col-8">
                    <FormGroup labelFor="dataset-name-edit">
                        <InputGroup
                            id="dataset-name-edit"
                            placeholder="Dataset name"
                            type="text"
                            large={true}
                            onKeyPress={this.handleKeyPress}
                        />
                    </FormGroup>
                </div>
            );
        }
    }

    getMenuContent() {
        return (
            <Menu key="menu">
                <MenuItem icon="edit" text="Edit" onClick={this.handleEditClick} />
                <MenuItem icon="trash" text="Delete" intent={Intent.DANGER} onClick={this.handleDeleteClick} />
            </Menu>
        );
    }

    render() {
        if (this.state.redirect) {
            return <Redirect push to={`${this.state.selected}/annotator`} />
        }
        return (
            <div id="dataset" className="d-flex container justify-content-center">
                <Card
                    id="dataset-card"
                    interactive={true}
                    elevation={Elevation.TWO}
                    style={{width: "20vw", height: "25vh"}}
                >
                    <div className="row align-items-center justify-content-center">
                        <div className="col-1">
                            <Checkbox checked={this.state.isChecked} onChange={this.handleChange} />
                        </div>

                        {this.renderTitle()}

                        <div className="col-1">
                            <Popover
                                enforceFocus={false}
                                isOpened={this.state.isPopoverOpen === true ? true: undefined}
                                interactionKind={PopoverInteractionKind.CLICK}
                            >
                                <Button icon="menu" type="button" minimal="true" />
                                {this.getMenuContent()}
                            </Popover>
                        </div>
                    </div>
                </Card>
                {this.renderAlert()}
            </div>
        );
    }
}

export default Dataset;