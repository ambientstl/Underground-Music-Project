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

var svg = d3.select("#top_genres")
              .append("svg")
              .attr("width", svgWidth)
              .attr("height", svgHeight);

var chartGroup = svg.append("g")
                    .attr("transform", `translate(${margin.left}, ${margin.top})`);

var url = "/api/top_genres"
d3.json(url).then(response => {
  var total_album_count = response.Total_Albums
  var top_genre_data = response.Top_Genres
  
  var top_20_genres = []
  for (i=0; i<20; i++) {
    top_20_genres.push(top_genre_data[i])
  }

  // Configure a band scale for the horizontal axis with a padding of 0.1 (10%)
  var xBandScale = d3.scaleBand()
  .domain(top_20_genres.map(d => d.Genre))
  .range([0, chartWidth])
  .padding(0.1);

  // Create a linear scale for the vertical axis.
  var yLinearScale = d3.scaleLinear()
    .domain([0, total_album_count])
    .range([chartHeight, 0]);

  // Create two new functions passing our scales in as arguments
  // These will be used to create the chart's axes
  var bottomAxis = d3.axisBottom(xBandScale);
  var leftAxis = d3.axisLeft(yLinearScale).ticks(10);

  chartGroup.append("g")
    .call(leftAxis);

  chartGroup.append("g")
    .attr("transform", `translate(0, ${chartHeight})`)
    .call(bottomAxis)
    .selectAll("text")
    .attr("y", 0)
    .attr("x", 9)
    .attr("dy", ".35em")
    .attr("transform", "rotate(90)")
    .style("text-anchor", "start");

  var barGroup = chartGroup.selectAll(".top_genres")
    .data(top_20_genres)
    .enter()
    .append("a")
    .attr("href", d => `#${d.Genre}`)
    .append("rect")
    .attr("class", "bar")
    .attr("x", d => xBandScale(d.Genre))
    .attr("y", d => yLinearScale(d.Count))
    .attr("width", xBandScale.bandwidth())
    .attr("height", d => chartHeight - yLinearScale(d.Count));

  // Step 1: Initialize Tooltip
  var toolTip = d3.tip()
                  .attr("class", "tooltip")
                  // .offset([20, 40])
                  .html(function(d) {
                    return (`<strong>${(d.Genre)}</strong></br>${d.Count}
                    Albums`);
                  });

  // Step 2: Create the tooltip in chartGroup.
  chartGroup.call(toolTip);

  // Step 3: Create "mouseover" event listener to display tooltip
  barGroup.on("mouseover", function(d) {
    toolTip.style("display", "block");
    toolTip.style("background", "DarkGrey");
    toolTip.style("border-radius", "6px")
    toolTip.show(d, this);
    })
  // Step 4: Create "mouseout" event listener to hide tooltip
    .on("mouseout", function(d) {
      toolTip.hide(d);
    });

});
