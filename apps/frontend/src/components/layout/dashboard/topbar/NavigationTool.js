import React, { Component } from "react";

import css from "../../../../../static/css/annotator.module.css";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import styles from "../../../../../static/css/layout/dashboard/topbar/topbar.module.css";

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
                <div className={"row justify-content-center " + styles.topbar}>
                    <div className="col-auto align-self-center">
                        <a href={this.state.previous}>
                            <FontAwesomeIcon icon="angle-left" />
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
                        <a href={this.state.next}>
                            <FontAwesomeIcon icon="angle-right" />
                        </a>
                    </div>
                </div>
            </div>
        );
    }
}

export default NavigationTool;