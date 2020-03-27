import React, {Component} from 'react';
import NavigationTool from "./NavigationTool";
import {Button, ButtonGroup, ControlGroup} from "@blueprintjs/core";
import {Intent} from "@blueprintjs/core/lib/cjs/common/intent";

class TopToolbar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div id="top-navigator" className={"container-fluid"}>
                <div className="row justify-content-center">

                    <div className="col justify-content-center">
                        <NavigationTool
                            file_name={`${this.props.filename} [${this.props.index}]`}
                            onClickPrevious={this.props.onClickPrevious}
                            onClickNext={this.props.onClickNext}
                        />
                    </div>
                    <div className="col-auto mr-auto">
                        <ControlGroup vertical={true} onKeyPress={this.props.onKeyPress}>
                            <ButtonGroup fill={true} large={true}>
                                <Button
                                    icon="export"
                                    intent={Intent.PRIMARY}
                                    onClick={this.props.onClick}
                                >
                                    Export
                                </Button>
                            </ButtonGroup>
                        </ControlGroup>
                    </div>
                </div>
            </div>
        );
    }
}

export default TopToolbar;