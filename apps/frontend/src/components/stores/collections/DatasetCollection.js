import {action, observable} from "mobx";
import "regenerator-runtime/runtime";
import API from "api";


class DatasetCollection {
    path = 'dataset/';
    query = '?project=';
    @observable all = [];
    @observable isLoading = false;

    @action async fetchAll(projectID) {
        const response = await API.get(this.path + this.query + projectID);
        const status = await response.status;

        if (status === 200) {
            this.all = await response.json();
        }
    }

    @action async add(data) {
        const response = await API.post(this.path, data);
        const status = await response.status;

        if (status === 201) {
            this.fetchAll(data.project);
        }

        return response.json();
    }

    @action find(datasetURL) {
        return (
            this.all.slice().filter(
                p => p.url === parseInt(datasetURL, 10)
            )[0]
        );
    }

    @action async update(datasetURL, data) {
        const path = this.path + API.retrievePathID(datasetURL) + '/';

        const response = await API.put(path, data);
        const status = await response.status;

        if (status === 200) {
            this.fetchAll(data.project);
        }
    }

    @action async delete(datasetURL, projectID) {
        const path = this.path + API.retrievePathID(datasetURL) + '/';

        const response = await API.delete(path);
        const status = await response.status;

        if (status === 204) {
            this.fetchAll(projectID);
        }
    }

    @action retrieveID(path) {
        return API.retrievePathID(path);
    }
}

const datasetCollection = new DatasetCollection();

export default datasetCollection;
