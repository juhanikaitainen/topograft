export function calculateRainfall(nodes) {
    let rainfallAmt = 2;
    let rainfallRecieved = {};  

    let sortedNodes = nodes.map((x) => x);  // Copy the nodes array
    sortedNodes.sort((a, b) => b.height - a.height);  // Sort it by height, descending

    for (let node of sortedNodes) {
        if (node.isPeak()) {
            rainfallRecieved[node.id] = rainfallAmt;
            continue;
        }

        let water = rainfallAmt;
        for (let neighbor of node.neighbors) {
            if (neighbor.height > node.height) {
                water += neighbor.waterFlowTo(node) * rainfallRecieved[neighbor.id];
            } 
        }

        rainfallRecieved[node.id] = water;
        //console.log(node, "recieved", water, "rainfall");
    }

    return rainfallRecieved;
}