# Topograft - Procedural Terrain Generation

![sample terrain](sample_terrain.gif)

[Play with the demo here!](https://gerhalt.github.io/topograft)

Inspirational 3-dimensional world generation and visualization with tunable parameters as a three dimensional map rendered with pure Javascript in the browser.


## Procedure

This is a work in progress, but the generation mostly works as follows:

1. We begin with a grid of randomized points.
2. Those points are fed into [Delaunator](https://github.com/mapbox/delaunator), a library for quickly generating [Delaunay triangulations](https://en.wikipedia.org/wiki/Delaunay_triangulation). For our purposes, this connects nearby points.
3. From the triangulation, we build a graph of nodes from each raw point, containing default height information and links to the neighboring nodes. It's all graph traversal from here on out.
4. Feature generation 
    1. Randomly generate initial parameters. Peak or trough (below sea level), spread, ridge length, etc.
    2. Choose an initial starting point. Record its distance from the ridge line (as 0). Add it to our node queue.
    3. While the ridge length is less than the desired length, add a neighboring node we haven't seen to our node queue. If we're more than two nodes in, check all neighbors and find the node with the maximum angle between the incoming and outgoing edges. Record these distances as 0.
    4. Once we've collected our ridge, begin pulling nodes off the queue. Set the height based on our height falloff function. If the current distance is less than the maximum feature spread, add the neighboring nodes we haven't operated on yet to our queue. Mark their distances as the current distance plus one.