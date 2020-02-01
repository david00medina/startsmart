import React, {Component} from 'react';

class ProgressBar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div id="progressbar" className="progress">
                <div className="progress-bar progress-bar-striped progress-bar-animated bg-info"
                    role="progressbar"
                    aria-valuenow="75"
                    aria-valuemin="0"
                    aria-valuemax="100"
                    style={{width: `${this.props.progress}%`}}>

                </div>
            </div>
        );
    }
}

export default ProgressBar;