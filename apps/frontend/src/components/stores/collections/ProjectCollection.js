import {action, observable} from "mobx";
import "regenerator-runtime/runtime";
import API from "api";


class ProjectCollection {
    path = 'project/';
    @observable all = [];
    @observable isLoading = false;

    @action async fetchAll() {
        const response = await API.get(this.path);
        const status = await response.status;

        if (status === 200) {
            this.all = await response.json();
        }
    }
    
    @action async add(data) {
        const response = await API.post(this.path, data);
        const status = await response.status;

        if (status === 201) {
            this.fetchAll();
        }

        return response.json();
    }

    @action find(projectURL) {
        return (
            this.all.slice().filter(
                p => p.url === parseInt(projectURL, 10)
            )[0]
        );
    }

    @action async update(projectURL, data) {
        const path = this.path + API.retrievePathID(projectURL) + '/';

        const response = await API.put(path, data);
        const status = await response.status;

        if (status === 200) {
            this.fetchAll();
        }
    }

    @action async delete(projectURL) {
        const path = this.path + API.retrievePathID(projectURL) + '/';

        const response = await API.delete(path);
        const status = await response.status;

        if (status === 204) {
            this.fetchAll();
        }
    }

    @action retrieveID(path) {
        return API.retrievePathID(path);
    }
}

const projectCollection = new ProjectCollection();

export default projectCollection;
