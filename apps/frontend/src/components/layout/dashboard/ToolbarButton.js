import React, { Component } from 'react';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'


class ToolbarButton extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <button type="button" className="btn btn-primary">
                <FontAwesomeIcon icon={this.props.icon} />
            </button>
        );
    }
}

ToolbarButton.propTypes = {};

export default ToolbarButton;