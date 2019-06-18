//// GENRE LIST ////
function listGenres() {
  var url = "/api/genres";
  d3.json(url).then(response => {
    var data = response[0].Genres
    // console.log(data)
    var genre_list = d3.select("#genre_list")

    data.forEach((genre) => {
      genre_list.append("li")
                .append("a")
                .attr("href", "/genre/" + genre)
                .text(genre)})
  })
}

listGenres()

//// TOP GENRES ////
function defineGenres() {
  var url = "/api/top_genres"
  d3.json(url).then(response => {
    // console.log(response)
    var data = response.Top_Genres;
    // console.log(data)
    var genre_definitions = d3.select("#genre_definitions");
    data.forEach((top_genre) => {
      
      genre_definitions.append("dt")
                      .attr("class", "offset-md-1 col-3 d-flex")
                      .append("div")
                      .attr("class", "ml-auto")
                      .append("a")
                      .attr("href", "/genre/" + top_genre.Genre)
                      .text(top_genre.Genre)
      genre_definitions.append("dd")
                      .attr("class", "col-7")
                      .text(top_genre.Description);
      genre_definitions.append("div")
      .style("position", "relative")
      .append("a")
      .attr("name", top_genre.Genre)
      .style("position", "absolute")
      .style("top", "-60px")
    });

  });
};
defineGenres();

// function drawTopGenresGraph() {
//   var url = "/api/top_genres"
//   d3.json(url).then(response => {
//     var top_genres_data = response.Top_Genres;
//     var total_album_count = response.Total_Albums;

//     var svgHeight = 600;
//     var svgWidth = 400;

//     var svg = d3
//       .select("#top_genres")
//       .append("svg")
//       .attr("height", svgHeight)
//       .attr("width", svgWidth);

//     var svgGroup = svg.append("g")
//     // .attr("transform", "translate(50, 100)");
//     console.log(top_genres_data)
//     svgGroup.append("rect")
//             .attr("width", 200)
//             .attr("height", 200)
//             .classed("bar", true)
//             .attr("fill", "red");
//     top_genres_data.forEach((top_genre) => {
//       console.log(top_genre.Count);
//       svgGroup.select('rect')
//       .data(top_genre.Count)
//       // .enter()
//       .append('rect')
//       .attr("width", 50)
//       .attr("height", function(data) {
//         return data / 2;
//       })
//       .attr("x", function(data, index) {
//         return index * 60;
//       })
//       .attr("y", function(data) {
//         return 500 - (data / 2);
//       })
//       .attr("class", "bar");
//     })
//   })
// }
// drawTopGenresGraph();

// var svgWidth = 960;
// var svgHeight = 500;

// var margin = {
//   top: 20,
//   right: 40,
//   bottom: 80,
//   left: 100
// };

// var width = svgWidth - margin.left - margin.right;
// var height = svgHeight - margin.top - margin.bottom;

// var svg = d3.select("#top_genres")
//             .append("svg")
//             .attr("width", svgWidth)
//             .attr("height", svgHeight);

// var chartGroup = svg.append("g")
//                     .attr("transform", `translate(${margin.left}, ${margin.top})`);

// // Initial Params
// var chosenXAxis = "top_20";

// // function used for updating x-scale var upon click on axis label
// function xScale(censusData, chosenXAxis) {
//   // create scales
//   var xLinearScale = d3.scaleLinear()
//     .domain([d3.min(censusData, d => d[chosenXAxis]) * 0.8,
//       d3.max(censusData, d => d[chosenXAxis]) * 1.2])
//     .range([0, width]);
//   return xLinearScale;
// }

// // // function used for updating y-scale var upon click on axis label
// // function yScale(censusData, chosenYAxis) {
// //   // create scales
// //   var yLinearScale = d3.scaleLinear()
// //     .domain([d3.min(censusData, d => d[chosenYAxis]) * 0.8,
// //       d3.max(censusData, d => d[chosenYAxis]) * 1.2])
// //     .range([height, 0]);
// //   return yLinearScale;
// // }

// // function used for updating xAxis var upon click on axis label
// // function renderXAxes(newXScale, xAxis) {
// //   var bottomAxis = d3.axisBottom(newXScale);

// //   xAxis.transition()
// //     .duration(1000)
// //     .call(bottomAxis);

// //   return xAxis;
// // }

// // function used for updating circles group with a transition to
// // new circles
// // function renderCircles(circlesGroup, newXScale, chosenXAxis, newYScale, chosenYAxis) {

// //   circlesGroup.transition()
// //     .duration(1000)
// //     .attr("cx", d => newXScale(d[chosenXAxis]))
// //     .attr("cy", d => newYScale(d[chosenYAxis]))

// //   return circlesGroup;
// // }

// // function used for updating circles group with new tooltip
// function updateToolTip(chosenXAxis, chosenYAxis, circlesGroup, textGroup) {

//   if (chosenXAxis === "poverty") {
//     var xLabel = "Poverty Rate (%):";
//   } else if (chosenXAxis === "age"){
//     var xLabel = "Age (Median):"
//   }
//   else {
//     var xLabel = "Income (Median):";
//   }

//   if (chosenYAxis === "healthcare") {
//     var yLabel = "Lacking Healthcare (%):"
//   } else if (chosenYAxis === "obesity") {
//     var yLabel = "Obese (%):"
//   } else {
//     var yLabel = "Smokers (%):"
//   }

//   var toolTip = d3.tip()
//     .attr("class", "tooltip d3-tip")
//     .offset([40, 80])
//     .html(function(d) {
//       return (`<strong>${d.state}</strong><br>${xLabel} ${d[chosenXAxis]}<br>${yLabel} ${d[chosenYAxis]}`);
//     })
//     ;

//   circlesGroup.call(toolTip);

//   circlesGroup.on("mouseover", function(data) {
//     toolTip.show(data, this);})
//     .on("mouseout", function(data) {
//       toolTip.hide(data);});

//   textGroup.call(toolTip);

//   textGroup.on("mouseover", function(data) {
//     toolTip.show(data, this);})
//     // onmouseout event
//     .on("mouseout", function(data) {
//       toolTip.hide(data);
//     });

//   return circlesGroup;
//   // return textGroup;

// }
// var url = "/api/top_genres"
// d3.json(url).then(response => {
//   // if (err) throw err;

//   data = response[0]

//   var total_albums = data.total_albums
//   var top_genres = data.top_genres
//   // // parse CSV data
//   // response.forEach(data => {
//   //   data.poverty = +data.poverty;
//   //   data.age = +data.age;
//   //   data.income = +data.income;
//   //   data.healthcare = +data.healthcare;
//   //   data.obesity = +data.obesity;
//   //   data.smokes = +data.smokes;
//   //   // console.log(data.abbr)
//   // });

//   // // xLinearScale function above csv import
//   // var xLinearScale = xScale(censusData, chosenXAxis);

//   // // Create y scale function
//   // var yLinearScale = yScale(censusData, chosenYAxis);

//   // // Create initial axis functions
//   // var bottomAxis = d3.axisBottom(xLinearScale);
//   // var leftAxis = d3.axisLeft(yLinearScale);

//   // append x axis
//   var xAxis = chartGroup.append("g")
//     .classed("x-axis", true)
//     .attr("transform", `translate(0, ${height})`)
//     .call(bottomAxis);

//   // append y axis
//   var yAxis = chartGroup.append("g")
//     .classed("y-axis", true)
//     .call(leftAxis);

//   // append initial circles
//   var barGroup = chartGroup.selectAll(".genreBar")
//     .data(top_genres)
//     .enter()
//     .append("rect")
//     .attr("x", d => xLinearScale(d[chosenXAxis]))
//     .attr("y", d => yLinearScale(d[chosenYAxis]))
//     .attr("class", "genreBar")
//     // .attr("r", 15)
//     .attr("opacity", ".9");

//   // Create group for 3 x-axis labels
//   var xLabelsGroup = chartGroup.append("g")
//     .attr("transform", `translate(${width / 2}, ${height + 20})`);

//   var top20Label = xLabelsGroup.append("text")
//     .attr("x", 0)
//     .attr("y", 20)
//     .attr("value", "top_20") // value to grab for event listener
//     .classed("active", true)
//     .text("Top 20");

//   var top50Label = xLabelsGroup.append("text")
//     .attr("x", 0)
//     .attr("y", 40)
//     .attr("value", "top_50") // value to grab for event listener
//     .classed("inactive", true)
//     .text("Top 50");

//   var allGenresLabel = xLabelsGroup.append("text")
//     .attr("x", 0)
//     .attr("y", 60)
//     .attr("value", "all_genres")
//     .classed("inactive", true)
//     .text("All Genres");

