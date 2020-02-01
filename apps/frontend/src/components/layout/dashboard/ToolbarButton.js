import React, { Component } from 'react';

import css from '../../../../static/css/layout/dashboard/toolbar-button.module.css'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'


class ToolbarButton extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div className="row">
                <div className="col-auto mr-auto">
                    <a href="#">
                        <FontAwesomeIcon icon={this.props.icon} />
                    </a>
                </div>
            </div>
        );
    }
}

ToolbarButton.propTypes = {};

export default ToolbarButton;