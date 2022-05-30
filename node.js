
export class Node {

    constructor(id, x, y, height = -0.5) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.height = height;

        this.totalElevationDrop = 0.0;
        this.neighbors = new Set()  

        this.edge = false;
    }

    /* Returns the node's color, with alpha
     */
    color(maxHeight) {
        let r, g, b;
        let a = 1.0; //Math.random();

        if ( false && this.edge ) {
            r = 1.0;
            g = 0.0;
            b = 0.0;
        } else if ( 0 < this.height && this.height < 0.15 ) {
            r = 0.1; // + Math.random() * 0.1;
            g = 0.6; // + Math.random() * 0.3;
            b = 0.1; // + Math.random() * 0.2;
        } else if (this.height < 0.05) {
            r = 0.2;
            g = 0.2;
            b = 0.8;
            a = 0.5;
        } else {
            r = 0.0 + this.height / maxHeight;
            g = 0.0 + this.height / maxHeight;
            b = 0.0 + this.height / maxHeight;
        }

        return [r, g, b, a];
    }

    /* Center this this amongst its neighbors. */
    center() {
        let x = 0.0;
        let y = 0.0;

        this.neighbors.forEach((neighbor) => {
            x += neighbor.x;
            y += neighbor.y;
        });

        this.x = x / this.neighbors.size;
        this.y = y / this.neighbors.size;
    }

    isPeak() {
        for (let neighbor of this.neighbors) {
            if (neighbor.height > this.height) {
                return false;
            }
        }

        return true;
    }

    // Calculate the ratio of incoming water that will flow to a neighbor node.
    waterFlowTo(otherNode) {
        // This calculation can be re-used for each neighboring node
        if (otherNode.height >= this.height) {
            return 0.0;
        } else if (this.totalElevationDrop == 0) {
            // If one node is lower than us, and the total elevation drop is 0,
            // we haven't calculated it yet; do so before we return the result
            for (let node of this.neighbors) {
                if (node.height < this.height) {
                    this.totalElevationDrop += this.height - node.height;
                }
            }
        }

        return (this.height - otherNode.height) / this.totalElevationDrop;
    }

    distance(otherNode) {
        return Math.sqrt((this.x - otherNode.x) ** 2 + (this.y - otherNode.y) ** 2);
    }

    addNeighbors(...neighbors) {
        neighbors.forEach((neighbor) => {
            this.neighbors.add(neighbor);
        })
    }
}