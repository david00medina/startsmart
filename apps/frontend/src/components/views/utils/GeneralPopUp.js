import React, {Component} from 'react';
import CreateProjectPopup from "../ProjectView/CreateProjectPopup";
import CreateDatasetPopup from "../DatasetView/CreateDatasetPopup";

class GeneralPopUp extends Component {
    constructor(props) {
        super();
    }

    render() {
        if (this.props.name === 'Project') {
            return <CreateProjectPopup
                isOpen={this.props.isOpenCreate}
                onClick={this.props.onClick}
                onKeyPress={this.props.onKeyPress}
            />;
        } else if (this.props.name === 'Dataset') {
            return <CreateDatasetPopup
                {...this.props.bp3}
                isOpen={this.props.isOpenCreate}
                onClick={this.props.onClick}
                onKeyPress={this.props.onKeyPress}
                onInputChange={this.props.onInputChange}
                onChangeStatus={this.props.onChangeStatus}
            />
        }
    }
}

export default GeneralPopUp;