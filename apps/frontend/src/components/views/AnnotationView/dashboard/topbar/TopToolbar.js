import React, {Component} from 'react';
import NavigationTool from "./NavigationTool";

class TopToolbar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div id="top-navigator" className={"container-fluid"}>
                <div className="row justify-content-center">
                    <div className="col-auto mr-auto">
                        HOME
                    </div>
                    <div className="col justify-content-center">
                        <NavigationTool
                            file_name={`${this.props.filename} [${this.props.index}]`}
                            onClickPrevious={this.props.onClickPrevious}
                            onClickNext={this.props.onClickNext}
                        />
                    </div>
                </div>
            </div>
        );
    }
}

export default TopToolbar;