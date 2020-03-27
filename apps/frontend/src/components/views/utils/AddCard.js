import React, {Component} from "react";
import {Card, Dialog, Elevation, Icon, Intent} from "@blueprintjs/core";
import CreateProjectPopup from "../ProjectView/CreateProjectPopup";
import CreateDatasetPopup from "../DatasetView/CreateDatasetPopup";

class AddCard extends Component {
    constructor(props) {
        super();
        this.state = {
            isOpenProject: false,
            isOpenDataset: false,
        }
    }
    handleClick = (e) => {
        if (this.props.name === 'Project') {
            this.setState({
                isOpenProject: true,
            });

        } else if (this.props.name === 'Dataset') {
            this.setState({
                isOpenDataset: true,
            });
        }
    };

    render() {
        return (
            <div id="add-card" className="d-flex container justify-content-center">
                <CreateProjectPopup isOpen={this.state.isOpenProject}/>
                <CreateDatasetPopup isOpen={this.state.isOpenDataset}/>
                <Card
                    id="project-card"
                    interactive={true}
                    elevation={Elevation.TWO}
                    onClick={this.handleClick}
                    style={{width: "20vw", height: "25vh"}}
                    className="d-flex align-items-center justify-content-center"
                >
                    <Icon
                        icon={`add`}
                        intent={Intent.PRIMARY}
                        title={`Add ${this.props.name}`}
                        iconSize={64}
                    />
                </Card>
            </div>
        );
    }
}

AddCard.propTypes = {};

export default AddCard;