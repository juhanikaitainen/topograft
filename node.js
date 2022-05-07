
export class Node {

    constructor(id, x, y, height = 0.0) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.height = height;  // || Math.random() * 0.1;

        this.neighbors = new Set()  
    }

    /* Center this node amongst its neighbors. */
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

    distance(other) {
        return Math.sqrt((this.x - other.x) ** 2 + (this.y - other.y) ** 2);
    }

    addNeighbors(...neighbors) {
        neighbors.forEach((neighbor) => {
            this.neighbors.add(neighbor);
        })
    }
}