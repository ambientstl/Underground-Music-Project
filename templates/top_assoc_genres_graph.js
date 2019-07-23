var svgWidth = 960;
var svgHeight = 660;

var margin = {
  top: 100,
  right: 30,
  bottom: 60,
  left: 50
};

var chartWidth = svgWidth - margin.left - margin.right;
var chartHeight = svgHeight - margin.top - margin.bottom;

var svg1 = d3.select("#associated_genres")
              .append("svg")
              .attr("width", svgWidth)
              .attr("height", svgHeight);

var chartGroup1 = svg1.append("g")
                    .attr("transform", `translate(${margin.left}, ${margin.top})`);


var pathname = window.location.pathname
var splitPath = pathname.split("/")
var selected_genre = splitPath[2]

var url1 = "/api/genres/" + selected_genre
d3.json(url1).then(response => {

  var total_album_count_for_genre = response.Album_Count
  var associated_genre_data = response.Associated_Genre_Counts

  var top_associated_genres = []
  for (i=1; i<21; i++) {
    try {
      top_associated_genres.push(associated_genre_data[i])
    }
    catch(err) {
      break
    }
  }

  console.log(top_associated_genres)

  // Configure a band scale for the horizontal axis with a padding of 0.1 (10%)
  var xBandScale1 = d3.scaleBand()
  .domain(top_associated_genres.map(d => d.Genre))
  .range([0, chartWidth])
  .padding(0.1);

  // Create a linear scale for the vertical axis.
  var yLinearScale1 = d3.scaleLinear()
    .domain([0, total_album_count_for_genre])
    .range([chartHeight, 0]);

  // Create two new functions passing our scales in as arguments
  // These will be used to create the chart's axes
  var bottomAxis1 = d3.axisBottom(xBandScale1);
  var leftAxis1 = d3.axisLeft(yLinearScale1).ticks(10);

  chartGroup1.append("g")
    .call(leftAxis1);

  chartGroup1.append("g")
    .attr("transform", `translate(0, ${chartHeight})`)
    .call(bottomAxis1)
    .selectAll("text")
    .attr("y", 0)
    .attr("x", 9)
    .attr("dy", ".35em")
    .attr("transform", "rotate(90)")
    .style("text-anchor", "start");

  var barGroup1 = chartGroup1.selectAll(".top_genres")
    .data(top_associated_genres)
    .enter()
    .append("a")
    .attr("href", d => `/genre/${d.Genre}`)
    .append("rect")
    .attr("class", "bar")
    .attr("x", d => xBandScale1(d.Genre))
    .attr("y", d => yLinearScale1(d.Associated_Count))
    .attr("width", xBandScale1.bandwidth())
    .attr("height", d => chartHeight - yLinearScale1(d.Associated_Count));

  // Step 1: Initialize Tooltip
  var toolTip1 = d3.tip()
                  .attr("class", "tooltip")
                  // .offset([20, 40])
                  .html(function(d) {
                    return (`<strong>${(d.Genre)}</strong></br>${d.Associated_Count}
                    Albums`);
                  });

  // Step 2: Create the tooltip in chartGroup.
  chartGroup1.call(toolTip1);

  // Step 3: Create "mouseover" event listener to display tooltip
  barGroup1.on("mouseover", function(d) {
    toolTip1.style("display", "block");
    toolTip1.style("background", "DarkGrey");
    toolTip1.style("border-radius", "6px")
    toolTip1.show(d, this);
    })
  // Step 4: Create "mouseout" event listener to hide tooltip
    .on("mouseout", function(d) {
      toolTip1.hide(d);
    });

});
