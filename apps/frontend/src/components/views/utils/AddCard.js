import React, {Component} from "react";
import {Card, Dialog, Elevation, Icon, Intent} from "@blueprintjs/core";
import GeneralPopUp from "./GeneralPopUp"

class AddCard extends Component {
    constructor(props) {
        super();
        this.state = {
            isOpenProject: false,
            isOpenDataset: false,
        }
    }

    render() {
        return (
            <div id="add-card" className="d-flex container justify-content-center">

                <GeneralPopUp
                    bp3={this.props.bp3}
                    name={this.props.name}
                    isOpenCreate={this.props.isOpenCreate}
                    onClick={this.props.onCreate}
                    onKeyPress={this.props.onKeyPress}
                    onInputChange={this.props.onInputChange}
                    onChangeStatus={this.props.onChangeStatus}
                />

                <Card
                    id="project-card"
                    interactive={true}
                    elevation={Elevation.TWO}
                    onClick={this.props.onClick}
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
// <CreateDatasetPopup isOpen={this.state.isOpenDataset}/>
export default AddCard;