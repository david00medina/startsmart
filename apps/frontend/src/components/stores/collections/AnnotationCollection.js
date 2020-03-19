import {action, observable} from "mobx";
import "regenerator-runtime/runtime";
import API from "api";


class AnnotationCollection {
    path = 'annotation/';
    query = '?id=%s';
    @observable all = [];
    @observable isLoading = false;

    @action async fetchAll(id) {
        const response = await API.get(this.path
            + this.query.replace('%s', id));
        const status = await response.status;

        if (status === 200) {
            this.all = await response.json();
        }
    }

    @action async add(data) {
        const response = await API.post(this.path, data);
        const status = await response.status;
        return response.json();
    }
}

const annotationCollection = new AnnotationCollection();

export default annotationCollection;