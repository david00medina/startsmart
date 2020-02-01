import React, {Component} from 'react';

import styles from '../../../../static/css/layout/dashboard/vertical-toolbar.module.css'

import TopToolbar from "./topbar/TopToolbar";
import ProgressBar from "../utils/ProgressBar";
import VerticalToolbar from "./VerticalToolbar";

class Dashboard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoaded: false,
            progress: 50,
            items: []
        }
    }

    componentDidMount() {
        fetch('startsmart/api/image', {
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
           }
        }).then(res => res.json()).then(json => {
                this.setState({
                    isLoaded: true,
                    items: json
                });
        });
    }

    render() {
        let { isLoaded, items } = this.state;

        if (!isLoaded) {
            return (
                <div className="container-fluid center">
                    <ProgressBar progress={this.state.progress} />
                </div>
            )
        } else {
            let item = items[8].uri;

            return (
                <div id="dashboard" className="container-fluid">
                    <TopToolbar item={item} />
                    <div className="row row-cols-3">
                        <div className={'col-auto ' + styles['vertical-toolbar']}>
                            <VerticalToolbar />
                        </div>
                        <div className="col-auto">
                            <div className="container-fluid">
                                <img src={item} />
                            </div>
                        </div>
                        <div className="col-auto">
                            Aqui va algo
                        </div>
                    </div>
                </div>
            );
        }
    }
}

export default Dashboard;