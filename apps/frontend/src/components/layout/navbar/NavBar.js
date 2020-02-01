import React, {Component} from 'react';
import NavButton from "./NavButton";
import SearchBar from "../utils/SearchBar";


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
                    <span className="navbar-toggler-icon">Datasets</span>
                    <span className="navbar-toggler-icon">Annotator</span>
                </button>
                <a className="navbar-brand" href="/">StartSmart</a>

                <div className="collapse navbar-collapse" id="navbarColor02">
                    <ul className="navbar-nav mr-auto">
                        {this.renderButtons(0, "Home", "/")}
                        {this.renderButtons(1, "Projects", "/projects")}
                        {this.renderButtons(2, "Datasets", "/datasets")}
                        {this.renderButtons(3, "Annotator", "/annotator")}
                    </ul>
                    <SearchBar placeholder="Buscar" button_name="Buscar" />
                </div>
            </nav>
        );
    }
}


export default NavBar;