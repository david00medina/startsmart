import React, {Component} from 'react';
import ToolbarButton from "./ToolbarButton";


class VerticalToolbar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="toolbar">
                <div id="vertical-toolbar" className="btn-group-vertical" data-toggle="buttons">
                    <ToolbarButton icon="mouse-pointer" />
                    <ToolbarButton icon="arrows-alt" />
                    <ToolbarButton icon="draw-polygon" />
                    <ToolbarButton icon="tag" />
                </div>
            </div>
        );
    }
}

export default VerticalToolbar;