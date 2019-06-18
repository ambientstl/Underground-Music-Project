d3.select(window).on("resize", handleResize);

// Initial Params
var chosenXAxis = "all_genres";

// When the browser loads, loadChart() is called
loadChart(chosenXAxis);

function handleResize(chosenXAxis) {
  console.log(chosenXAxis)
  var svgArea = d3.select("svg");

  // If there is already an svg container on the page, remove it and reload the chart
  if (!svgArea.empty()) {
    svgArea.remove();
    loadChart(chosenXAxis);
  }
}

function loadChart(chosenXAxis) {
  // Define SVG area dimensions
  var svgWidth = 960;
  var svgHeight = 660;

  // Define the chart's margins as an object
  var margin = {
    top: 100,
    right: 30,
    bottom: 60,
    left: 50
  };

  // Define dimensions of the chart area
  var chartWidth = svgWidth - margin.left - margin.right;
  var chartHeight = svgHeight - margin.top - margin.bottom;

  var svg = d3.select("#top_genres")
              .append("svg")
              .attr("width", svgWidth)
              .attr("height", svgHeight);

  // Append an SVG group
  var chartGroup = svg.append("g")
                      .attr("transform", `translate(${margin.left}, ${margin.top})`);



  // update axis scale
  function xScale(top_genre_data) {
    var xScaleBand = d3.scaleBand()
                      .domain(top_genre_data.map(d => d.Genre))
                      .range([0, chartWidth])
                      .padding(0.1);
    return xScaleBand;        
  };
 

  // function used for updating xAxis var upon click on axis label
  function renderXAxes(newXScale, xAxis) {
    var bottomAxis = d3.axisBottom(newXScale);
    xAxis.transition()
        .duration(1000)
        .call(bottomAxis);
    return xAxis;
  };

  // update graph
  function renderGraph(graphGroup, newXScale, top_genres_data) {

    graphGroup.transition()
              .duration(1000)
              .attr("x", d => newXScale(d.Genre))
              .attr("width", newXScale.bandwidth())

    return graphGroup;
  };

  var url = "/api/top_genres"
  d3.json(url).then(response => {
    var all_top_genres_data = response.Top_Genres;
    var total_album_count = response.Total_Albums;
    var top_genre_data = all_top_genres_data

    // xLinearScale function above csv import
    var xScaleBand = xScale(top_genre_data);
    var yLinearScale = d3.scaleLinear()
                        .domain([0, total_album_count])
                        .range([chartHeight, 0]);

    // Create initial axis functions
    var bottomAxis = d3.axisBottom(xScaleBand);
    var leftAxis = d3.axisLeft(yLinearScale);

    // append x axis
    var xAxis = chartGroup.append("g")
                          .classed("x-axis", true)
                          .attr("transform", `translate(0, ${chartHeight})`)
                          .call(bottomAxis)
                          .selectAll("text")
                          .attr("y", 0)
                          .attr("x", 9)
                          .attr("dy", ".35em")
                          .attr("transform", "rotate(90)")
                          .style("text-anchor", "start");

    // append y axis
    var yAxis = chartGroup.append("g")
                          .classed("y-axis", true)
                          .call(leftAxis);

    var barGroup = chartGroup.append("g")
                            .selectAll("rect")
                            .data(top_genre_data)
                            .enter()
                            .append("a")
                            .attr("href", d => `#${d.Genre}`)
                            .append("rect")
                            // .merge(chartGroup)
                            .attr("x", d => xScaleBand(d.Genre))
                            .attr("y", d => yLinearScale(d.Count))
                            .attr("width", xScaleBand.bandwidth())
                            .attr("height", d => chartHeight - yLinearScale(d.Count))
                            .attr("class", "bar")  
    // chartGroup.exit().remove()            

    var xLabelsGroup = chartGroup.append("g")
                                .attr("transform", `translate(${chartWidth / 2}, -80)`);
                              
    var top20Label = xLabelsGroup.append("text")
                                .attr("x", 0)
                                .attr("y", 20)
                                .attr("value", "top_20")
                                .classed("inactive", true)
                                .text("Top 20 Genres");

    var top50Label = xLabelsGroup.append("text")
                                .attr("x", 0)
                                .attr("y", 40)
                                .attr("value", "top_50")
                                .classed("inactive", true)
                                .text("Top 50 Genres");

    var allGenresLabel = xLabelsGroup.append("text")
                                .attr("x", 0)
                                .attr("y", 60)
                                .attr("value", "all_genres")
                                .classed("active", true)
                                .text("All Genres");


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


  // x axis labels event listener
  xLabelsGroup.selectAll("text")
              .on("click", function() {
                // get value of selection
                var value = d3.select(this).attr("value");
                // if value is diff from chosenXAxis
                if (value !== chosenXAxis) {
                  // alert(`Value: ${value}`);
                  // update chosenXAxis
                  chosenXAxis = value;
                  //// update top_genres_data
                  var top_20_list = []
                  var top_50_list = []
                  // for top 20...
                  if (chosenXAxis == "top_20") {
                    for (var i = 0; i < 20; i++) {
                      top_20_list.push(all_top_genres_data[i])
                    }
                    top_genres_data = top_20_list
                  }
                  // for top 50...
                  else if (chosenXAxis == "top_50") {
                    for (var i = 0; i < 50; i++) {
                      // console.log(all_top_genres_data[i])
                      top_50_list.push(all_top_genres_data[i])
                    }
                    top_genres_data = top_50_list
                  }
                  // for all genres
                  else {
                    // console.log(all_top_genres_data)
                    top_genres_data = all_top_genres_data
                  }

                  // updates x scale for new data
                  xScaleBand = xScale(top_genres_data);
                  // updates x axis with transition
                  xAxis = renderXAxes(xScaleBand, xAxis);
                  // updates circles with new x values
                  barGroup = renderGraph(barGroup, xScaleBand, top_genres_data);
                  if (chosenXAxis === "top_20") {
                    top20Label
                      .classed("active", true)
                      .classed("inactive", false);
                    top50Label
                      .classed("active", false)
                      .classed("inactive", true);
                    allGenresLabel
                      .classed("active", false)
                      .classed("inactive", true)
                  } else if (chosenXAxis === "top_50") {
                    top20Label
                      .classed("active", false)
                      .classed("inactive", true);
                    top50Label
                      .classed("active", true)
                      .classed("inactive", false);
                    allGenresLabel
                      .classed("active", false)
                      .classed("inactive", true)
                  }
                  else {
                    top20Label
                      .classed("active", false)
                      .classed("inactive", true);
                    top50Label
                      .classed("active", false)
                      .classed("inactive", true);
                    allGenresLabel
                      .classed("active", true)
                      .classed("inactive", false)
                  }
                }


              });
  });


}