$().ready(function() {
var data = [{"number":1, "value":8},{"number":2, "value":16},{"number":3, "value":32},{"number":4, "value":64}];
var w = 515;
var h = 660;
var x = d3.scale.linear()
  .domain([0, d3.max(data, function(d) { return d.value; })])
  .range([0, w]);
var y = d3.scale.ordinal()
  .domain(d3.range(data.length))
  .rangeBands([0, h], 0.1);
var color = d3.scale.ordinal()
  .range(["red", "blue"]);

//initial svg creation
var svg = d3.select("#test-chart")
  .append("svg")
    .attr("width", 815 + 40)
    .attr("height", h + 20)
  .append("g")
    .attr("transform", "translate(20,0)");

//bars
var bars = svg.selectAll(".bar")
    .data(data)
  .enter().append("g")
    .attr("class", "bar")
    .attr("transform", function(d, i) { return "translate(" + 0 + "," + y(i+1) + ")"; });
//bar rectangles
bars.append("rect")
  .attr("fill", function(d, i) { return color(i%2); })
  .attr("width", function(d) { return x(d.value); })
  .attr("height", y.rangeBand());
//bar labels
bars.append("text")
  .attr("x", function(d) { return x(d.value); })
  .attr("y", 0 + y.rangeBand() / 2)
  .attr("dx", -6)
  .attr("dy", ".35em")
  .attr("text-anchor", "end")
  .text(function(d) { return d.value; });



});
