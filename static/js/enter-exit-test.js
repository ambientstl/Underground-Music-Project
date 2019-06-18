var top_20 = []
var top_50 = []
var all_genres = []

for (i=0; i<20; i++) {
  top_20.push(i)
}

for (i=0; i<50; i++) {
  top_50.push(i)
}

for (i=0; i<100; i++) {
  all_genres.push(i)
}

var selection_options = [top_20, top_50, all_genres]

function update(data) {

  var selection = d3.select("#fucking_list").selectAll("li")
        .data(data);

  selection.enter()
        .append("li")
        // .classed("temps", true)
        .merge(selection)
        // .style("height", function(d) {
        //   return d + "px";
        // });

  selection.exit().remove();
}

d3.select("#fucking_button").on("click", handleClick)


function handleClick() {
  // alert(`FUCKKKKKKKK`)
  var randomItem = selection_options[Math.floor(Math.random()*selection_options.length)];
  console.log(randomItem)
  // var data = [1,2,3]
  update(randomItem)
}

