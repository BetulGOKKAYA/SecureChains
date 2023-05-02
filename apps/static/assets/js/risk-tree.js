'use strict';
const url = window.location.href


 


 

const types = [ "Software Risk", "Hardware Risk", "User Risk"];





 $.ajax({
  type: 'GET',
  url: `${url}data/`,
  success: function(response){
    
      const treeData = response.hierarchical_data;
 


   
      createTree(treeData)

 

      
  },
  error: function(error){
      console.log(error)
  }
})

var svg;

// Set the dimensions and margins of the diagram
var margin = {top: 20, right: 80, bottom: 30, left: 60},
width = 1060 - margin.left - margin.right,
height = 1000 - margin.top - margin.bottom;

const createTree = (treeData) =>{




// append the svg object to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
svg = d3.select("#tree-container").append("svg")
.attr("width", width * 2) // Double the width of the SVG element
.attr("height", height + margin.top + margin.bottom)
.append("g")
.attr("transform", "translate("
      + (margin.left + 102) + "," + margin.top + ")");


var i = 0,
duration = 450,
root;

// declares a tree layout and assigns the size
var treemap = d3.tree().size([height * 0.6, width]);


// Assigns parent, children, height, depth
root = d3.hierarchy(treeData, function(d) { return d.children; });
root.x0 = height / 2;
root.y0 = 0;

// Collapse after the second level
root.children.forEach(collapse);

update(root);

// Collapse the node and all it's children
function collapse(d) {
if(d.children) {
d._children = d.children
d._children.forEach(collapse)
d.children = null
}
}

function update(source) {

// Assigns the x and y position for the nodes
var treeData = treemap(root);

// Compute the new tree layout.
var nodes = treeData.descendants(),
  links = treeData.descendants().slice(1);

// Normalize for fixed-depth.
nodes.forEach(function(d) {
  if (d.parent === root) { // If the node is a direct child of the root node
    d.y = d.depth * 180;
  } else if (d.parent && d.parent.parent === root) { // If the node is a child of the root's child
    d.y = d.parent.y + 220; // Change the value here to adjust the distance
  } else {
    d.y = d.depth * 320;
  }
});

// ****************** Nodes section ***************************

// Update the nodes...
var node = svg.selectAll('g.node')
  .data(nodes, function(d) {return d.id || (d.id = ++i); });

// Enter any new modes at the parent's previous position.
var nodeEnter = node.enter().append('g')
  .attr('class', 'node')
  .attr("transform", function(d) {
    return "translate(" + source.y0 + "," + source.x0 + ")";
})
.on('click', click);

// Add Circle for the nodes
nodeEnter.append('circle')
  .attr('class', 'node')
  .attr('r', 1e-6)
  .style("fill", function(d) {
      return d._children ? "lightsteelblue" : "#fff";
  });

// Add labels for the nodes
nodeEnter.append('text')
  .attr("dy", ".35em")
  .attr("x", function(d) {
      return d.children || d._children ? -13 : 13;
  })
  .attr("text-anchor", function(d) {
      return d.children || d._children ? "end" : "start";
  })
  .text(function(d) {
      if (d.data.score) {
          return `${d.data.name}: ${d.data.score}`;
      } else {
          return d.data.name;
      }
  });


// UPDATE
var nodeUpdate = nodeEnter.merge(node);

// Transition to the proper position for the node
nodeUpdate.transition()
.duration(duration)
.attr("transform", function(d) { 
    return "translate(" + d.y + "," + d.x + ")";
 });

// Update the node attributes and style
nodeUpdate.select('circle.node')
    .attr('r', 10)
    .style("fill", function(d) {
        if (d.data.value) {
            return getColor(d.data.value);
        } else if (d.data.threat_score) {
            return getColor(d.data.threat_score);
        } else if (d.data.score) { // Add this condition to handle the score property
            return getColor(d.data.score);
        } else {
            return d._children ? "gray" : "#fff";
        }
    })
    .attr('cursor', 'pointer');

function getColor(score) {
  if (score == 'Very Low') { // Very low
      return "lightgreen";
  } else if (score == 'Low') { // Low
      return "green";
  } else if (score == 'Medium') { // Medium
      return "orange";
  } else if (score == 'High') { // High
      return "red";
  } else if (score == 'Very High') { // High
      return "darkred";
  }
}


// Remove any exiting nodes
var nodeExit = node.exit().transition()
  .duration(duration)
  .attr("transform", function(d) {
      return "translate(" + source.y + "," + source.x + ")";
  })
  .remove();

// On exit reduce the node circles size to 0
nodeExit.select('circle')
.attr('r', 1e-6);

// On exit reduce the opacity of text labels
nodeExit.select('text')
.style('fill-opacity', 1e-6);

// ****************** links section ***************************

// Update the links...
var link = svg.selectAll('path.link')
  .data(links, function(d) { return d.id; });

// Enter any new links at the parent's previous position.
var linkEnter = link.enter().insert('path', "g")
  .attr("class", "link")
  .attr('d', function(d){
    var o = {x: source.x0, y: source.y0}
    return diagonal(o, o)
  }); 
// UPDATE
var linkUpdate = linkEnter.merge(link);

// Transition back to the parent element position
linkUpdate.transition()
  .duration(duration)
  .style("stroke", "#8a8989")
  .attr('d', function(d){ return diagonal(d, d.parent) });

// Remove any exiting links
var linkExit = link.exit().transition()
  .duration(duration)
  .attr('d', function(d) {
    var o = {x: source.x, y: source.y}
    return diagonal(o, o)
  })
  .remove();

// Store the old positions for transition.
nodes.forEach(function(d){
d.x0 = d.x;
d.y0 = d.y;
});

// Creates a curved (diagonal) path from parent to the child nodes
function diagonal(s, d) {
  // Check if the source node is the main root node
  const isMainRootNode = s.parent === null;

  // If it's the main root node, reduce the distance between the main root and its children
  const newY = isMainRootNode ? s.y + (d.y - s.y) * 0.2 : d.y;

  let path = `M ${s.y} ${s.x}
        C ${(s.y + newY) / 2} ${s.x},
          ${(s.y + newY) / 2} ${d.x},
          ${newY} ${d.x}`;
  return path;
}


// Toggle children on click.
function click(d) {
if (d.children) {
    d._children = d.children;
    d.children = null;
  } else {
    d.children = d._children;
    d._children = null;
  }
update(d);
}
}

}

const slider = document.getElementById("myRange");
const sliderValue = document.getElementById("slider-value");
sliderValue.innerHTML = slider.value;

slider.oninput = function() {
  sliderValue.innerHTML = this.value;
  const scaleFactor = this.value / 100;
  updateTreeScale(scaleFactor);
}

function updateTreeScale(scaleFactor) {
  svg.attr("transform", "translate(" + (margin.left + 102) + "," + margin.top + ") scale(" + scaleFactor + ")");
}
