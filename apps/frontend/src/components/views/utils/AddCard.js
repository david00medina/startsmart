import React, {Component} from "react";
import {Card, Elevation, Icon, Intent} from "@blueprintjs/core";

class AddCard extends Component {
    handleClick = (e) => {
        console.log("Launch add Project module");
    };

    render() {
        return (
            <div id="add-card" className="d-flex container justify-content-center">
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