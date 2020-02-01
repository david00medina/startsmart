import React, {Component} from 'react';
import ToolbarButton from "./ToolbarButton";

import css from '../../../../static/css/layout/dashboard/vertical-toolbar.module.css'

class VerticalToolbar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div id="vertical-toolbar" className="container-fluid">
                <div className="row align-items-start" style={css.verticalToolbar}>
                    <div className="col-auto align-self-center">
                        <ToolbarButton icon="mouse-pointer"/>
                    </div>
                    <div className="w-100"></div>
                    <div className="col-auto align-self-center">
                        <ToolbarButton icon="arrows-alt"/>
                    </div>
                    <div className="w-100"></div>
                    <div className="col-auto align-self-center">
                        <ToolbarButton icon="draw-polygon"/>
                    </div>
                    <div className="w-100"></div>
                    <div className="col-auto align-self-center">
                        <ToolbarButton icon="tag"/>
                    </div>
                </div>
            </div>
        );
    }
}

export default VerticalToolbar;