import React, {Component} from 'react';
import NavButton from "./NavButton";
import SearchBar from "../utils/SearchBar";
import {Button, ButtonGroup, ControlGroup} from "@blueprintjs/core";
import {Intent} from "@blueprintjs/core/lib/cjs/common/intent";


class NavBar extends Component {
    renderButtons(i, value, href) {
        return (
            <NavButton value={value} href={href}/>
        )
    }

    render() {
        return (
            <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor02"
                        aria-controls="navbarColor02" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon">Home</span>
                    <span className="navbar-toggler-icon">Projects</span>
                </button>
                <a className="navbar-brand" href="/">Home</a>

                <div className="collapse navbar-collapse" id="navbarColor02">
                    <ul className="navbar-nav mr-auto">
                        {this.renderButtons(1, "Projects", "/projects")}
                    </ul>
                </div>
                <ControlGroup>
                    <ButtonGroup fill={true} large={true}>
                        <Button
                            icon={"log-out"}
                            intent={Intent.PRIMARY}
                            onClick={this.props.onClick}
                        >
                            Log out
                        </Button>
                    </ButtonGroup>
                </ControlGroup>

            </nav>
        );
    }
}

//<SearchBar placeholder="Buscar" button_name="Buscar" />

/*

*/
export default NavBar;