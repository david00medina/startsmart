import {action, observable} from "mobx";
import "regenerator-runtime/runtime";
import API from "api";


class Video {
    path = 'video/';
    path_get_frame = 'get_frame/';
    query = '?dataset=%s';
    query_video = '?video=%s&';
    query_frame_no = '&frame_no=%s';
    @observable data = [];
    @observable frame = null;
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

    @action async get_frame(data) {
        let path = this.path_get_frame + this.query_video.replace("%s", data.video)
            + this.query_frame_no.replace("%s", data.frame_no);
        const response = await API.get(path);
        const status = await response.status;

        if (status === 200) {
            this.frame = await response.json();
        }

        return this.frame;
    }

    @action async add(data) {
        const formData = new FormData();
        formData.append('dataset', data.dataset);
        formData.append('license', data.license);
        formData.append('filename', data.filename);
        formData.append('uri', data.uri);
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

const videoModel = new Video();

export default videoModel;
