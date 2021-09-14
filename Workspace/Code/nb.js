// Add your JavaScript code here
const MAX_WIDTH = Math.max(1200, window.innerWidth);
const MAX_HEIGHT = 720;
const margin = {top: 40, right: 100, bottom: 40, left: 200};

// Assumes the same graph width, height dimensions as the example dashboard. Feel free to change these if you'd like
let graph_1_width = (MAX_WIDTH / 2) - 10, graph_1_height = 350;
let graph_2_width = (MAX_WIDTH / 2) - 10, graph_2_height = 350;
// let graph_3_width = MAX_WIDTH / 2, graph_3_height = 600;

const DOT_R = 2;
const ACC_DOT_COLOR = '#3358ff';
const POS_DOT_COLOR = '#7cabf7';
const NEG_DOT_COLOR = '#003891';
const OTHER_COLOR = '#4287f5';

// make an svg for each graph
let svg1 = d3.select("#graph1")
    .append("svg")
    .attr("width", graph_1_width)
    .attr("height", graph_1_height)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`)
    .attr("align", "center");;

let svg2 = d3.select("#graph2")
    .append("svg")
    .attr("width", graph_2_width)
    .attr("height", graph_2_height)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`)
    .attr("align", "center");

d3.csv("../nb_accuracy.csv").then(function(data) {
    data = getData(data, 'mean_vote');
    let x = d3.scaleLinear()
        .domain([0, 1])
        .range([0, graph_1_width - margin.left - margin.right]);
    svg1.append("g")
        .attr("transform", `translate(0, ${graph_1_height - margin.bottom - 40})`)
        .call(d3.axisBottom(x).tickSize(2).tickPadding([10]));
    let y = d3.scaleLinear()
        .domain([1, 0])
        .range([0, graph_1_height - margin.top - margin.bottom]);
    svg1.append("g").call(d3.axisLeft(y).tickSize(2).tickPadding([10]))

    let acc_dots = svg1.selectAll("acc_dot").data(data);
    acc_dots.enter()
        .append("circle")
        .attr("fill", ACC_DOT_COLOR)
        .attr("cx", function(d) {return x(d.pctile)})
        .attr("cy", function(d) {return y(d.accuracy)})
        .attr("r", DOT_R);
    svg1.append("text")
        .attr("transform", `translate(${graph_1_width - margin.right - 300}, ${margin.top + 68})`)
        .style("text-anchor", "middle")
        .text("Accuracy Rate")
        .style("fill", ACC_DOT_COLOR);

    let pos_dots = svg1.selectAll("acc_dot").data(data);
    pos_dots.enter()
        .append("circle")
        .attr("fill", POS_DOT_COLOR)
        .attr("cx", function(d) {return x(d.pctile)})
        .attr("cy", function(d) {return y(d.false_pos)})
        .attr("r", DOT_R);
    svg1.append("text")
        .attr("transform", `translate(${graph_1_width - margin.right - 275}, ${margin.top + 180})`)
        .style("text-anchor", "middle")
        .text("False Positive Rate")
        .style("fill", POS_DOT_COLOR);

    let neg_dots = svg1.selectAll("neg_dot").data(data);
    neg_dots.enter()
        .append("circle")
        .attr("fill", NEG_DOT_COLOR)
        .attr("cx", function(d) {return x(d.pctile)})
        .attr("cy", function(d) {return y(d.false_neg)})
        .attr("r", DOT_R);
    svg1.append("text")
        .attr("transform", `translate(${graph_1_width - margin.right - 275}, ${margin.top + 155})`)
        .style("text-anchor", "middle")
        .text("False Negative Rate")
        .style("fill", NEG_DOT_COLOR);

    svg1.append("text")
        .attr("transform", `translate(${(graph_1_width - margin.left - margin.right) / 2}, ${graph_1_height - margin.bottom})`)
        .style("text-anchor", "middle")
        .text("Threshold Percentile of Mean Vote");
    svg1.append("text")
        .style("text-anchor", "end")
        .attr("transform", `rotate(-90)`)
        .attr("dy", ".75em")
        .attr("y", -60)
        .text("Average Rate");
    svg1.append("text")
        .attr("transform", `translate(${(graph_1_width - margin.left - margin.right) / 2}, -25)`)
        .style("text-anchor", "middle")
        .text("Average Accuracy, False Positive, and False Negative Rates")
        .style("font-size", 15);
    svg1.append("text")
        .attr("transform", `translate(${(graph_1_width - margin.left - margin.right) / 2}, -6)`)
        .style("text-anchor", "middle")
        .text("vs Threshold Percentile of Mean Vote")
        .style("font-size", 15);
})

d3.csv("../nb_accuracy.csv").then(function(data) {
    data = getData(data, 'profit');
    let x = d3.scaleLinear()
        .domain([0, 1])
        .range([0, graph_1_width - margin.left - margin.right]);
    svg2.append("g")
        .attr("transform", `translate(0, ${graph_1_height - margin.bottom - 40})`)
        .call(d3.axisBottom(x).tickSize(2).tickPadding([10]));
    let y = d3.scaleLinear()
        .domain([1, 0])
        .range([0, graph_1_height - margin.top - margin.bottom]);
    svg2.append("g").call(d3.axisLeft(y).tickSize(2).tickPadding([10]))

    let acc_dots = svg2.selectAll("acc_dot").data(data);
    acc_dots.enter()
        .append("circle")
        .attr("fill", ACC_DOT_COLOR)
        .attr("cx", function(d) {return x(d.pctile)})
        .attr("cy", function(d) {return y(d.accuracy)})
        .attr("r", DOT_R);
    svg2.append("text")
        .attr("transform", `translate(${graph_1_width - margin.right - 300}, ${margin.top + 70})`)
        .style("text-anchor", "middle")
        .text("Accuracy Rate")
        .style("fill", ACC_DOT_COLOR);

    let pos_dots = svg2.selectAll("acc_dot").data(data);
    pos_dots.enter()
        .append("circle")
        .attr("fill", POS_DOT_COLOR)
        .attr("cx", function(d) {return x(d.pctile)})
        .attr("cy", function(d) {return y(d.false_pos)})
        .attr("r", DOT_R);
    svg2.append("text")
        .attr("transform", `translate(${graph_1_width - margin.right - 275}, ${margin.top + 180})`)
        .style("text-anchor", "middle")
        .text("False Positive Rate")
        .style("fill", POS_DOT_COLOR);

    let neg_dots = svg2.selectAll("neg_dot").data(data);
    neg_dots.enter()
        .append("circle")
        .attr("fill", NEG_DOT_COLOR)
        .attr("cx", function(d) {return x(d.pctile)})
        .attr("cy", function(d) {return y(d.false_neg)})
        .attr("r", DOT_R);
    svg2.append("text")
        .attr("transform", `translate(${graph_1_width - margin.right - 275}, ${margin.top + 160})`)
        .style("text-anchor", "middle")
        .text("False Negative Rate")
        .style("fill", NEG_DOT_COLOR);

    svg2.append("text")
        .attr("transform", `translate(${(graph_1_width - margin.left - margin.right) / 2}, ${graph_1_height - margin.bottom})`)
        .style("text-anchor", "middle")
        .text("Threshold Percentile of Profit");
    svg2.append("text")
        .style("text-anchor", "end")
        .attr("transform", `rotate(-90)`)
        .attr("dy", ".75em")
        .attr("y", -60)
        .text("Average Rate");
    svg2.append("text")
        .attr("transform", `translate(${(graph_1_width - margin.left - margin.right) / 2}, -25)`)
        .style("text-anchor", "middle")
        .text("Average Accuracy, False Positive, and False Negative Rates")
        .style("font-size", 15);
    svg2.append("text")
        .attr("transform", `translate(${(graph_1_width - margin.left - margin.right) / 2}, -6)`)
        .style("text-anchor", "middle")
        .text("vs Threshold Percentile of Profit")
        .style("font-size", 15);
})

function getData(data, desired_y) {
    to_return = [];
    for (let i = 0; i < data.length; i++) {
        datum = data[i];
        if (datum.y == desired_y) {
            to_return.push(datum);
        }
    }
    return to_return;
}

