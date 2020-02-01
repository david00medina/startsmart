import React, {Component} from 'react';
import {NavLink, withRouter} from "react-router-dom";

class NavButton extends Component {
    getNavLinkClass(path) {
        return this.props.location.pathname === path ? 'active' : '';
    }

    render() {
        return (
            <li className={"nav-item " + this.getNavLinkClass(this.props.href)}>
                <NavLink className="nav-link"
                         activeClassName="nav-link active"
                         to={this.props.href}>
                    {this.props.value}
                </NavLink>
            </li>
        );
    }
}

NavButton = withRouter(NavButton);
export default NavButton;