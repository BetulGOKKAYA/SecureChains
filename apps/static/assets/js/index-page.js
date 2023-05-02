'use strict';

const url = window.location.href
const modalBody = document.getElementById('modal-body-confirm')
const hardwareRiskBtn = document.getElementById('hardwareRisk-btn')
const userRiskBtn = document.getElementById('userRisk-btn') 
const swRiskBtn = document.getElementById('swRisk-btn')
const startBtn = document.getElementById('start-button')
const progressBar = document.getElementById('progress-bar')
const Progressvery_high = document.getElementById("progress-very_high")
const Progresshigh = document.getElementById("progress-high")
const Progressmedium = document.getElementById("progress-medium")
const Progresslow = document.getElementById("progress-low")
const Progress_very_low = document.getElementById("progress_very_low")


 

const hardwareRiskLevel = "high"

const chrt = document.getElementById('chart');
const ctx = document.getElementById('myChart');
const bubble = document.getElementById('bubbleChart');
const chartBar = document.getElementById('chartBar');

const softwareRisk = {
  type: "Software Risk",
  lowRisk: 0,
  mediumRisk: 0,
  highRisk: 0,
  very_highRisk: 0,
  score: 0
};
const hardwareRisk = {
  type: "Hardware Risk",
  lowRisk: 0,
  mediumRisk: 0,
  highRisk: 0,
  very_highRisk: 0,
  score: 0
};
const userRisk = {
  type: "User Risk",
  lowRisk: 0,
  mediumRisk: 0,
  highRisk: 0,
  very_highRisk: 0,
  score: 0
};
 
 

const types = [ "Software Risk", "Hardware Risk", "User Risk"];




 $.ajax({
  type: 'GET',
  url: `${url}risk/tree/data/`,
  success: function(response){
    
      const data = response.results

   

      data.forEach(el => {

        if(el.risk_group=='Software Risk'){

          if(el.qualitative_result=='Low'){
            softwareRisk.lowRisk++;
            softwareRisk.score++;
        
             
          }
        if(el.qualitative_result=='medium'){
            softwareRisk.mediumRisk++;
            softwareRisk.score++; 
            
          }
        if(el.qualitative_result=='High'){
            softwareRisk.highRisk++;
            softwareRisk.score++;

          }
        if(el.qualitative_result=='very_high'){
            softwareRisk.very_highRisk++;
            softwareRisk.score++; 
          }
 
 

        }
        if(el.risk_group=='Hardware Risk'){

          if(el.qualitative_result=='Low'){
            hardwareRisk.lowRisk++;
            hardwareRisk.score++;
        
             
          }
        if(el.qualitative_result=='medium'){
            hardwareRisk.mediumRisk++;
            hardwareRisk.score++; 
            
          }
        if(el.qualitative_result=='High'){
            hardwareRisk.highRisk++;
            hardwareRisk.score++;

          }
        if(el.qualitative_result=='very_high'){
            hardwareRisk.very_highRisk++;
            hardwareRisk.score++; 
          }
 
 

        }
        if(el.risk_group=='User Risk'){

          if(el.qualitative_result=='Low'){
            userRisk.lowRisk++;
            userRisk.score++;
        
             
          }
        if(el.qualitative_result=='medium'){
          userRisk.mediumRisk++;
          userRisk.score++; 
            
          }
        if(el.qualitative_result=='High'){
          userRisk.highRisk++;
          userRisk.score++;

          }
        if(el.qualitative_result=='very_high'){
          userRisk.very_highRisk++;
            userRisk.score++; 
          }
 
 

        }

        
 
      });

 


 

      
  },
  error: function(error){
      console.log(error)
  }
})










 fetch('data/') // progressBar for the total risk values
  .then(response => response.json())
  .then(data => {
    const resultData = data.result_data;
    const risk_results = data.risk_results; 
    const progressBars = document.querySelectorAll('.progress-bar');
    Progressvery_high.innerHTML = resultData.very_high;
    Progresshigh.innerHTML = resultData.high;
    Progressmedium.innerHTML = resultData.medium;
    Progresslow.innerHTML = resultData.low;
    Progress_very_low.innerHTML = resultData.very_low;

    progressBars.forEach(progressBar => {
      const progressBarValue = progressBar.getAttribute('aria-valuenow');
      switch (progressBarValue) {
        case 'very_high':
          progressBar.style.width = resultData.very_high + '%';
          break;
        case 'high':
          progressBar.style.width = resultData.high + '%';
          break;
        case 'medium':
          progressBar.style.width = resultData.medium + '%';
          break;
        case 'low':
          progressBar.style.width = resultData.low + '%';
          break;
        case 'very_low':
          progressBar.style.width = resultData.very_low + '%';
          break;
        default:
          break;
      }
    });

    const jsondata = data.jsonData;
    function getBackgroundColor(risk) {
      switch (risk) {
        case 1:
          return 'rgba(144, 238, 144, 0.4)'; // Light green
        case 2:
          return 'rgba(0, 128, 0, 0.4)'; // Green
        case 3:
          return 'rgba(255, 165, 0, 0.4)'; // Orange
        case 4:
          return 'rgba(255, 99, 71, 0.4)'; // Light red
        case 5:
          return 'rgba(255, 0, 0, 0.4)'; // Dark red
        default:
          return 'rgba(0, 0, 0, 0.4)'; // Black for unexpected values
      }
    }
    
     
    function getBackgroundColors(data) {
      return data.map(row => getBackgroundColor(row.risk));
    }
    
 /*
    const createBubbleChart = () => {

    const dataBubble = {
      labels: jsondata.map(x => x.type),
      datasets: [
      {
        label: 'IoT',
        borderColor: 'rgba(208,149,145)',
        backgroundColor: getBackgroundColors(jsondata.filter(row => row.type === 'hardware IoT')),
        borderWidth: 3, // Add this line to set the border width
        data: jsondata.filter(row => row.type === 'hardware IoT').map(row => ({
          x: row.impact,
          y: row.likelihood,
          r: row.count
        }))
      },
      {
        label: 'User Electronic (hardware)',
        backgroundColor: getBackgroundColors(jsondata.filter(row => row.type === 'hardware user electronic')),
        borderColor: 'rgba(200,98,73)',
        borderWidth: 3, // Add this line to set the border width
        data: jsondata.filter(row => row.type === 'hardware user electronic').map(row => ({
          x: row.impact,
          y: row.likelihood,
          r: row.count
        }))
      },
      {
        label: 'Hardware',
        backgroundColor: getBackgroundColors(jsondata.filter(row => row.type === 'hardware')),
        borderColor: 'rgba(204,0,0)',
        borderWidth: 3, // Add this line to set the border width
        data: jsondata.filter(row => row.type === 'hardware').map(row => ({
          x: row.impact,
          y: row.likelihood,
          r: row.count
        }))
      },{
        label: 'Third-party Software',
        backgroundColor: getBackgroundColors(jsondata.filter(row => row.type === 'software third-party')),
        borderColor: 'rgba(51,153,0)',
        borderWidth: 3, // Add this line to set the border width
        data: jsondata.filter(row => row.type === 'software third-party').map(row => ({
          x: row.impact,
          y: row.likelihood,
          r: row.count
        }))
      },{
        label: 'Software Hoested on Organization Machines',
        backgroundColor: getBackgroundColors(jsondata.filter(row => row.type === 'software hosted on organization')),
        borderColor: 'rgba(255,208,71)',
        borderWidth: 3, // Add this line to set the border width
        data: jsondata.filter(row => row.type === 'software hosted on organization').map(row => ({
          x: row.impact,
          y: row.likelihood,
          r: row.count
        }))
      },{
        label: 'Internal Users',
        backgroundColor: getBackgroundColors(jsondata.filter(row => row.type === 'user internal')),
        borderColor: 'rgba(180,130,194)',
        borderWidth: 3, // Add this line to set the border width
        data: jsondata.filter(row => row.type === 'user internal').map(row => ({
          x: row.impact,
          y: row.likelihood,
          r: row.count
        }))
      },{
        label: 'External Users',
        backgroundColor: getBackgroundColors(jsondata.filter(row => row.type === 'user external')),
        borderColor: 'rgba(56,134,181)',
        borderWidth: 3, // Add this line to set the border width
        data: jsondata.filter(row => row.type === 'user external').map(row => ({
          x: row.impact,
          y: row.likelihood,
          r: row.count
        }))
      }
    ]
  };


  const configBubble = {
    type: 'bubble',
    data: dataBubble,
    options: {
      responsive: true,
      legend: {
        position: 'top',
        onClick: function(e, legendItem) {
          const index = legendItem.index;
          const chartInstance = this.chart;
          const datasetMeta = chartInstance.getDatasetMeta(index);
        
          // Toggle the visibility of the dataset
          datasetMeta.hidden = !datasetMeta.hidden;
        
          // Update the chart to reflect the change
          chartInstance.update();
        // Update the legend item
        const updatedLegendItem = chartInstance.legend.legendItems[index];
        if (datasetMeta.hidden) { 
          updatedLegendItem.strokeStyle = 'rgb(105,105,105)';
        } else { 
           
          } 
        },
        labels: {
          usePointStyle: false, // Use the same style as the points in the chart
          boxWidth: 10, // Customize the size of the box
          fontSize: 12, // Customize the font size of the labels
          fontColor: '#666', // Customize the font color of the labels
          padding: 10, // Customize the padding between the labels
          generateLabels: function(chart) {
            const datasets = chart.data.datasets;
            return datasets.map(function(dataset, i) {
              return {
                text: dataset.label,
                fillStyle: 'transparent', // Set the background color to transparent
                strokeStyle: dataset.borderColor, // Use the borderColor of the dataset
                lineWidth: 2, // Customize the border width
                hidden: false,
                index: i
              };
            });
          }
          
        }
      },
      title: {
        display: true,
        text: 'Chart.js Bubble Chart'
      },
      scales: {
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Impact Score '
          },
          ticks: {
            min: 0,
            max: 6
          }
        }],
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Likelihood (threat x vulnerability) score'
          },
          ticks: {
            min: 0,
            max: 6
          }
        }]
      },
      tooltips: {
        callbacks: {
          label: function(tooltipItem, data) {
            const datasetLabel = data.datasets[tooltipItem.datasetIndex].label;
            const impact = tooltipItem.xLabel;
            const likelihood = tooltipItem.yLabel;
            const dataIndex = tooltipItem.index;
            const datasetIndex = tooltipItem.datasetIndex;
            const r = data.datasets[datasetIndex].data[dataIndex].r;
            return `${datasetLabel}: Final risk ${r}, Risk Value ${r}`;
          }
        }
      }      
      
    }
  };
 
  const chartCanvas = document.getElementById('dimensions');
  //new Chart(chartCanvas, configBubble);

  // Add text under the chart
  const textDiv = document.createElement('div');
  textDiv.innerHTML = '1: very low 2: low 3: medium 4: high 5: very high';
  chartCanvas.parentNode.insertBefore(textDiv, chartCanvas.nextSibling);
    };
 
    createBubbleChart()
*/


    // Create a dictionary to map asset types to risk scores
    var riskScores = {}; 
    risk_results.forEach(function(item) {
      riskScores[item.name] = item.risk_score;
    }); 
    // Your existing progress bar and bubble chart code

    function getTreeBackgroundColor(riskScore) {
      switch (riskScore) {
        case "Very Low":
          return 'rgba(144, 238, 144)'; // Light green
        case "Low":
          return 'rgba(19, 127, 19)'; // Green
        case "Medium":
          return 'rgba(255, 174, 26)'; // Orange
        case "High":
          return 'rgba(238, 145, 145)'; // Light red
        case "Very High":
          return 'rgba(204, 0, 0)'; // Dark red
        default:
          return 'rgba(141, 141, 141)'; // Black for unexpected values
      }
    }


    function createTreeChart(riskScores) {
      
          //risk results on tree illustration starts from here
          var root = {
            "name": "Supply Chain RISK",
            "children": [
              {
                "name": "Hardware Risk",
                "children": [
                  { "name": "USER ELECTRONICS" },
                  { "name": "COMPANY HARDWARE" },
                  { "name": "IoT" }
                ]
              },
              {
                "name": "User Risk",
                "children": [
                  { "name": "EXTERNAL USER" },
                  { "name": "INTERNAL USER" }
                ]
              },
              {
                "name": "Software Risk",
                "children": [
                  { "name": "THIRD-PARTY SOFTWARE" },
                  { "name": "SOFTWARE HOSTED on ORGANIZATION MACHINES" }
                ]
              }
            ]
          };

          

          var diameter = 760;

          var tree = d3.layout.tree()
          .size([360, diameter / 2 - 180])
          .separation(function(a, b) { return (a.parent == b.parent ? 1.5 : 2.5) / a.depth; });


          var diagonal = d3.svg.diagonal.radial()
          .projection(function(d) { return [d.y, d.x / 180 * Math.PI]; });

          var svg = d3.select("#tree-container").append("svg")
          .attr("width", diameter + 20)
          .attr("height", diameter - 40)
          .append("g")
          .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

          var nodes = tree.nodes(root),
          links = tree.links(nodes);

          var link = svg.selectAll(".link")
          .data(links)
          .enter().append("path")
          .attr("class", "link")
          .attr("d", diagonal);

          var node = svg.selectAll(".node")
          .data(nodes)
          .enter().append("g")
          .attr("class", "node")
          .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

          node.append("circle")
            .attr("r", function(d){
              return d.depth === 0 ? 15 : (d.depth === 1 ? 10 : 5);
            })
            .style("fill", function(d) {
              // Map the risk scores to the respective nodes using the riskScores dictionary
              var riskScore = riskScores[d.name];

              // Use the getTreeBackgroundColor function to set the background color based on risk score
              return getTreeBackgroundColor(riskScore);
            })
            .on("click", function(d) {
              if (d.name === "User Risk") {
                window.location.href = url + 'risk/tree/';
              } else if (d.name === "Software Risk") {
                window.location.href = url + 'risk/tree/';
              } else if (d.name === "Hardware Risk") {
                window.location.href = url + 'risk/tree/';
              }else if (d.name === "Supply Chain RISK") {
                window.location.href = url + 'risk/tree/';
              }
            })
            .on("mouseover", function (d) {
              d3.select(this).attr("r", function (d) {
                return d.depth === 0 ? 25 : (d.depth === 1 ? 20 : 15);
              });
              d3.select(this.nextSibling).style("font-size", function (d) {
                return d.depth === 0 ? "18px" : "16px";
              });
            })
            .on("mouseout", function (d) {
              d3.select(this).attr("r", function (d) {
                return d.depth === 0 ? 15 : (d.depth === 1 ? 10 : 5);
              });
              d3.select(this.nextSibling).style("font-size", function (d) {
                return d.depth === 0 ? "18px" : "11px";
              });
            });
            function wrap(text, width) {
              text.each(function () {
                var text = d3.select(this),
                  words = text.text().split(/\s+/).reverse(),
                  word,
                  line = [],
                  lineNumber = 0,
                  lineHeight = 0.8,  // ems
                  y = text.attr("y"),
                  dy = parseFloat(text.attr("dy")),
                  tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
                while (word = words.pop()) {
                  line.push(word);
                  tspan.text(line.join(" "));
                  if (tspan.node().getComputedTextLength() > width) {
                    line.pop();
                    tspan.text(line.join(" "));
                    line = [word];
                    tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
                  }
                }
              });
            }
            

            node.append("text")
            .attr("dy", function(d) {
              if (d.depth === 0) {
                return "0.3em";
              } else {
                return d.depth === 1 ? "-.15em" : ".31em";
              }
            })
            .attr("text-anchor", function(d) {
              return d.x < 180 ? (d.depth === 1 ? "middle" : "start") : "end";
            })
            .attr("transform", function(d) {
              if (d.depth === 0) {
                return "rotate(-90)";
              } else if (d.depth === 1) {
                return d.x < 180 ? "translate(0)" : "rotate(180)translate(0)";
              } else {
                return d.x < 180 ? "translate(8)" : "rotate(180)translate(-8)";
              }
            })
            .style("font-size", function(d) {
              return d.depth === 0 ? "18px" : "11px";
            })
            .html(function(d) {
              if (d.name === 'SOFTWARE HOSTED on ORGANIZATION MACHINES') {
                return 'SOFTWARE HOSTED on<tspan x="0" dy="1.1em">ORGANIZATION<tspan x="0" dy="1.1em">MACHINES</tspan></tspan>';
              } else if (d.name === 'Supply Chain RISK') {
                return 'Supply Chain<tspan x="0" dy="1.1em">RISK</tspan>';
              } else {
                return d.name;
              }
            });
            
            



            d3.select(self.frameElement).style("height", diameter - 150 + "px");


    }
    // Call the createTreeChart function with the riskScores object
    createTreeChart(riskScores);

  })
  .catch(error => console.error(error));



hardwareRiskBtn.addEventListener('click', ()=>{

    const dataInfra = hardwareRiskBtn.getAttribute('data-infra')
    const dataHardware = hardwareRiskBtn.getAttribute('data-hardware')


    modalBody.innerHTML = `
    <div class="h5 mb-3">Are you sure you want to submit your responses ?</div>
    <div class="text-muted">
        <ul>
                <li>Completed Infrastructure Questions: <b>${dataInfra}%</b></li>
                <li>Completed Hardware Questions: <b>${dataHardware}%</b></li>

                

     </ul>
    </div>
`

startBtn.addEventListener('click', ()=>{
    
    window.location.href = url + 'risk/results/hardware/'


 
})

})


swRiskBtn.addEventListener('click', ()=>{

 const dataInfra = swRiskBtn.getAttribute('data-infra')


  modalBody.innerHTML = `
  <div class="h5 mb-3">Are you sure you want to submit your responses ?</div>
  <div class="text-muted">
      <ul>
              <li>Completed Infrastructure Questions: <b>${dataInfra}%</b></li>

   </ul>
  </div>
`

startBtn.addEventListener('click', ()=>{
  
  window.location.href = url + 'risk/results/software/'



})

})

userRiskBtn.addEventListener('click', ()=>{

  const dataInfra = userRiskBtn.getAttribute('data-infra')
 
 
   modalBody.innerHTML = `
   <div class="h5 mb-3">Are you sure you want to submit your responses ?</div>
   <div class="text-muted">
       <ul>
               <li>Completed Infrastructure Questions: <b>${dataInfra}%</b></li>
 
    </ul>
   </div>
 `
 
 startBtn.addEventListener('click', ()=>{
   
   window.location.href = url + 'risk/results/user/'
 
 
 
 })
 
 })

// end    

