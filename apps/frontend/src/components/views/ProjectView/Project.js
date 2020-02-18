import React, {Component} from "react";
import {inject, observer} from "mobx-react";
import {
    Alert,
    Button,
    Card,
    Checkbox,
    Elevation, FormGroup, InputGroup,
    Intent,
    Menu,
    MenuItem,
    Popover
} from "@blueprintjs/core";
import {PopoverInteractionKind} from "@blueprintjs/core/lib/cjs/components/popover/popover";
import API from "api";
import {Redirect} from "react-router";


@inject('projectCollection')
@observer
class Project extends Component {
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
        this.props.projectCollection.delete(this.props.url);
        this.setState({
            isDeletionAlertOpened: false
        });
    };

    handleCardClick = (e) => {
        console.log("CARD CLICK : " + API.retrievePathID(this.props.url));
        this.setState({
            redirect: true,
            selected: API.retrievePathID(this.props.url)
        });
    };

    handleEditClick = (e) => {
        console.log(e.target);
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

    renderAlert() {
        return (
            <Alert
                cancelButtonText="Cancel"
                confirmButtonText="Delete"
                icon="trash"
                intent={Intent.DANGER}
                isOpen={this.state.isDeletionAlertOpened}
                canEscapeKeyCancel={true}
                onCancel={this.handleMoveCancel}
                onConfirm={this.handleMoveDeletion}
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
                    <h5 id="project-title" className="text-center m-1">{this.props.name}</h5>
                </div>
            );
        } else {
            return (
                <div className="col-8">
                    <FormGroup labelFor="project-name-edit">
                        <InputGroup
                            id="project-name-edit"
                            placeholder="Project name"
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
                <MenuItem id="edit-button-menu" icon="edit" text="Edit" onClick={this.handleEditClick} />
                <MenuItem
                    id="delete-button-menu"
                    icon="trash"
                    text="Delete"
                    intent={Intent.DANGER}
                    onClick={this.handleDeleteClick}
                />
            </Menu>
        );
    }

    render() {
        if (this.state.redirect) {
            return <Redirect push to={`${this.state.selected}/datasets`} />
        }
        return (
            <div id="project" className="d-flex container justify-content-center">
                <Card
                    id="project-card"
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
                                <Button id="button-menu" icon="menu" type="button" minimal="true"  />
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

export default Project;