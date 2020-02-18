import {action, observable} from "mobx";
import API from "api";


class LibraryCollection {
    path = 'library/';
    @observable all = [];

    @action async fetchAll() {
        const response = await API.get(this.path);
        const status = await response.status;

        if (status === 200) {
            this.all = await response.json();
        }
    }
}

const libraryCollection = new LibraryCollection();

export default libraryCollection;
