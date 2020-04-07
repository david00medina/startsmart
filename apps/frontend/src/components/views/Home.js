import React, {Component} from 'react';
import {Button, ButtonGroup, ControlGroup, FormGroup, InputGroup} from "@blueprintjs/core";
import {Intent} from "@blueprintjs/core/lib/cjs/common/intent";

class Home extends Component {
    render() {
        return (
            <div id="home" className='home text-center'>
                <h1>Sign up</h1>
                <div className="d-flex align-items-center align-self-center justify-content-center" style={{height: "94vh"}}>
                    <ControlGroup vertical={true} onKeyPress={this.props.onKeyPress}>
                        <FormGroup label={`USERNAME`} labelInfo={`(required)`} inline={true}>
                            <InputGroup
                                id="username"
                                placeholder="Username"
                                type="text"
                                fill={true}
                                large={true}
                                round={true}
                                inputRef={this.props.nameRef}
                            />
                        </FormGroup>
                        <FormGroup label={'PASSWORD'} labelInfo={`(required)`} inline={true}>
                            <InputGroup
                                id="password"
                                placeholder="Password"
                                type="password"
                                fill={true}
                                large={true}
                                round={true}
                                inputRef={this.props.nameRef}
                            />
                        </FormGroup>

                        <ButtonGroup fill={true} large={true}>
                            <Button
                                intent={Intent.PRIMARY}
                                onClick={this.props.onClick}
                            >
                                Sign up
                            </Button>
                        </ButtonGroup>
                    </ControlGroup>
                </div>
            </div>
        );
    }
}

export default Home;