import React, {Component} from "react";
import {Button, ButtonGroup, ControlGroup, FileInput, FormGroup, InputGroup} from "@blueprintjs/core";
import {Intent} from "@blueprintjs/core/lib/cjs/common/intent";

class CreateProjectPopup extends Component {
    render() {
        return (
            <div id={`create-project-view`}>
                <div className="row align-items-center justify-content-center m-5">
                    <div className="col-auto">
                        <ControlGroup vertical={true}>
                            <FormGroup label={`NAME`} labelInfo={`(required)`} inline={true}>
                                <InputGroup
                                    id="project-name-create"
                                    placeholder="Project name"
                                    type="text"
                                    onKeyPress={this.props.onKeyPress}
                                    fill={true}
                                    large={true}
                                    round={true}
                                />
                            </FormGroup>
                            <ButtonGroup fill={true} large={true}>
                                <Button
                                    icon="add"
                                    intent={Intent.PRIMARY}
                                    onClick={this.props.onClick}
                                >
                                    Create
                                </Button>
                            </ButtonGroup>
                        </ControlGroup>
                    </div>
                </div>
            </div>
        );
    }
}

CreateProjectPopup.propTypes = {};

export default CreateProjectPopup;