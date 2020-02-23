import {action, observable} from "mobx";
import "regenerator-runtime/runtime";
import API from "api";


class Image {
    path = 'image/';
    query = '?dataset=%s';
    @observable data = [];
    @observable isLoading = false;

    @action async fetch(id) {
        let path = this.path + this.query;
        const response = await API.get(path.replace("%s", id));
        const status = await response.status;

        if (status === 200) {
            this.data = await response.json();
        }
        return this.data;
    }

    @action async add(data) {
        const formData = new FormData();
        formData.append('dataset', data.dataset);
        formData.append('license', data.license);
        formData.append('filename', data.filename);
        formData.append('uri', data.uri);
        formData.append('roi', data.roi);
        const response = API.post_file(this.path, formData);
        response.onload = function() {
            if (response.status !== 201) {
                console.log(response.status);
            }
        };
    }

    @action async update(imageURL, data) {
        const path = this.path.replace("%s", API.retrievePathID(imageURL));

        const response = await API.put(path, data);
        const status = await response.status;

        if (status === 200) {
            this.fetchAll();
        }
    }

    @action async delete(imageURL) {
        const path = this.path.replace("%s", API.retrievePathID(imageURL));

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

const imageModel = new Image();

export default imageModel;
