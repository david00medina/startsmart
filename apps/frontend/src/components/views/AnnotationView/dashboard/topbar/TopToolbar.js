import React, {Component} from 'react';
import NavigationTool from "./NavigationTool";

import styles from '../../../../../../static/css/layout/dashboard/topbar/topbar.module.css'

class TopToolbar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let filename = this.props.item.substring(this.props.item.lastIndexOf('/')+1);

        return (
            <div id="top-navigator" className={"container-fluid " + styles.topbar}>
                <div className="row justify-content-center">
                    <div className="col-auto mr-auto" >
                        HOME
                    </div>
                    <div className="col justify-content-center">
                        <NavigationTool file_name={filename} />
                    </div>
                </div>
            </div>
        );
    }
}

export default TopToolbar;