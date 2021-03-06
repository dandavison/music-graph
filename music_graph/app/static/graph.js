var playArtist = function(id) {
  $.ajax("/play?artist_id=" + id, {
    method: "POST",
  })
}


// http://bl.ocks.org/mbostock/4062045
// https://github.com/d3/d3-plugins/tree/master/fisheye

var width = 1200,
    height = 800;

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-20)
    .linkDistance(40)
    .size([width, height]);

var svg = d3.select("#graph").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("/graph", function(error, graph) {
  if (error) throw error;

  force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

  var link = svg.selectAll(".link")
      .data(graph.links)
    .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.value); });

  var node = svg.selectAll(".node")
      .data(graph.nodes)
    .enter().append("circle")
      .attr("class", "node")
      .attr("r", 5)
      .style("fill", function(d) { return color(d.group); })
      .call(force.drag)
      .on("click", function(d) { playArtist(d.id); });

  node.append("title")
      .text(function(d) { return d.name; });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  });

  var fisheye = d3.fisheye.circular()
      .radius(200)
      .distortion(2);


svg.on("mousemove", function() {
  fisheye.focus(d3.mouse(this));

  node.each(function(d) { d.fisheye = fisheye(d); })
      .attr("cx", function(d) { return d.fisheye.x; })
      .attr("cy", function(d) { return d.fisheye.y; })
      .attr("r", function(d) { return d.fisheye.z * 4.5; });

  link.attr("x1", function(d) { return d.source.fisheye.x; })
      .attr("y1", function(d) { return d.source.fisheye.y; })
      .attr("x2", function(d) { return d.target.fisheye.x; })
      .attr("y2", function(d) { return d.target.fisheye.y; });
  });

});
