import React, { Component } from 'react'
import Sketch from "react-p5";

class Canvas extends Component {
    width = 0;
    height = 800;
    canvas = null;
    img = null;

    windowResized = (p5) => {
        let canvas = p5.select('#canvas');
        this.width = canvas.width;
        this.height = 800;
        p5.clear();
    };

    setup = (p5, canvasParentRef) => {
        this.canvas = p5.select('#canvas');
        this.width = this.canvas.width;
        this.height = p5.windowHeight * 0.87;
        p5.createCanvas(this.width, this.height).parent(canvasParentRef);
        if (this.props.image) {
            this.img = p5.loadImage(this.props.image.uri);
        }

        p5.fill(255,0,0);

        p5.beginShape();
        let point = [];
        for (var i = 0; i < this.props.roi.length; i++) {
            point[0] = this.props.roi[i];
            if ((i+1) % 2 === 0) {
                point[1] = this.props.roi[i];
                p5.vertex(point[0],  point[1]);
                point = [];
            }
        }
        p5.endShape(p5.CLOSE);
    };

    drawROI(rois) {
        this.props.rois.map((point, i) => {

        });
    }

    imageRatio = () => {
        return this.img.height / this.img.width;
    };

    draw = p5 => {
        p5.background(this.img);
        p5.ellipse(800, 300, 10, 10);
    };

    render() {
        return (
            <Sketch setup={this.setup} draw={this.draw} windowResized={this.windowResized} />
        );
    }
}

export default Canvas;