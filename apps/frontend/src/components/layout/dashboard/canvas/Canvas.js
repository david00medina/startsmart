import React, { Component } from 'react'
import Sketch from "react-p5";

class Canvas extends Component {
    img = null;
    width = 0;
    height = 800;

    componentDidMount() {
        fetch('startsmart/api/image', {
          headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
           }
        }).then(res => res.json()).then(json => {
                this.setState({
                    isLoaded: true,
                    items: json
                });
        });
    }

    setup = (p5, canvasParentRef) => {
        let canvas = p5.select('#canvas');
        this.width = canvas.width;
        this.height = 800;
        p5.createCanvas(this.width, this.height).parent(canvasParentRef);
        this.img = p5.loadImage(this.props.image.uri);
        console.log(this.props.image);
    };

    draw = p5 => {
        p5.background('#1d1e1f');
        p5.image(this.img, 0, 0);
    };

    render() {
        return <Sketch setup={this.setup} draw={this.draw} />;
    }
}

Canvas.propTypes = {};

export default Canvas;