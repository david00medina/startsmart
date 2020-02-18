import React, {Component} from 'react';

class SearchBar extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div id="search-bar" className="searchbar">
                <form className="form-inline my-2 my-lg-0">
                    <input className="form-control mr-sm-2" type="text" placeholder={this.props.placeholder} />
                    <button className="btn btn-secondary my-2 my-sm-0" type="submit">{this.props.button_name}</button>
                </form>
            </div>
        );
    }
}

export default SearchBar;