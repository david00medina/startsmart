import React, { Component } from "react";

import css from "../../../../../../static/css/annotator.module.css";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

class NavigationTool extends Component {
    constructor(props) {
        super(props);
        this.state = {
            previous: "#",
            next: "#"
        };
    }

    render() {
        return (
            <div id="navigation-tool" className="container-fluid">
                <div className={"row justify-content-center"}>
                    <div className="col-auto align-self-center">
                        <a href={this.state.previous} >
                            <FontAwesomeIcon
                                icon="angle-left"
                                onClick={this.props.onClickPrevious}
                            />
                        </a>
                    </div>
                    <div className="col-auto align-self-center">
                        <div className="container-fluid">
                            <span className={css.filename}>{this.props.file_name}</span>
                        </div>
                        <div className="container-fluid">
                            ZOOM
                        </div>
                    </div>
                    <div className="col-auto align-self-center">
                        <a href={this.state.next} >
                            <FontAwesomeIcon
                                icon="angle-right"
                                onClick={this.props.onClickNext}
                            />
                        </a>
                    </div>
                </div>
            </div>
        );
    }
}

export default NavigationTool;