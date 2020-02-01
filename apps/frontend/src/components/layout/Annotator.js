import React, {Component} from 'react';
import Dashboard from "./dashboard/Dashboard";

class Annotator extends Component {
    render() {
        return (
            <div id="annotator" className="annotator text-center">
                <Dashboard />
            </div>
        );
    }
}

export default Annotator;