import React, { Component } from "react";
import {
    Button,
    ButtonGroup,
    ControlGroup,
    Dialog,
    FileInput,
    FormGroup,
    HTMLSelect,
    InputGroup
} from "@blueprintjs/core";
import {Intent} from "@blueprintjs/core/lib/cjs/common/intent";
import {inject, observer} from "mobx-react";
import Dropzone from "react-dropzone-uploader";


@inject('libraryCollection')
@observer
class CreateDatasetPopup extends Component {
    componentDidMount() {
        this.props.libraryCollection.fetchAll();
    }

    render() {
        return (
            <Dialog isOpen={this.props.isOpen}>
            <div id={`create-dataset-view`}>
                <div className="row align-items-center justify-content-center m-5">
                    <div className="col-auto">
                        <ControlGroup vertical={true} onKeyPress={this.props.onKeyPress}>

                            <FormGroup label={`NAME`} labelInfo={`(required)`} inline={true}>
                                <InputGroup
                                    id="dataset-name-create"
                                    placeholder="Dataset name"
                                    type="text"
                                    fill={true}
                                    large={true}
                                    round={true}
                                    inputRef={this.props.nameRef}
                                />
                            </FormGroup>



                            <FormGroup label={`DATASET`} labelInfo={`(required)`} inline={false}>
                                <Dropzone
                                    onChangeStatus={this.props.onChangeStatus}
                                    accept="image/*,video/*"
                                    inputContent={(files, extra) =>
                                        (extra.reject ? 'This is not a video or image file' : 'Drag & Drop')}
                                    styles={{
                                        dropzoneReject: { borderColor: 'red', backgroundColor: '#DAA' },
                                        inputLabel: (files, extra) => (extra.reject ? { color: 'red' } : {}),
                                    }}
                                />
                            </FormGroup>

                            <ButtonGroup fill={true} large={true}>
                                <Button
                                    icon="add"
                                    intent={Intent.PRIMARY}
                                    onClick={this.props.onClick}
                                >
                                    Create
                                </Button>
                            </ButtonGroup>

                        </ControlGroup>
                    </div>
                </div>
            </div>
            </Dialog>
        );
    }
}

CreateDatasetPopup.propTypes = {};

export default CreateDatasetPopup;

/*
<FormGroup label={`LIBRARY`} labelInfo={`(required)`} inline={true}>
                                <HTMLSelect
                                    options={
                                        this.props.libraryCollection.all.slice().map(info => {
                                            return info.name;
                                        })
                                    }
                                    fill={true}
                                    large={true}
                                    elementRef={this.props.selectRef}
                                />
                            </FormGroup>
 */