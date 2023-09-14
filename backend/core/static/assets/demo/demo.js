type = ['primary', 'info', 'success', 'warning', 'danger'];

demo = {
  initPickColor: function() {
    $('.pick-class-label').click(function() {
      var new_class = $(this).attr('new-class');
      var old_class = $('#display-buttons').attr('data-class');
      var display_div = $('#display-buttons');
      if (display_div.length) {
        var display_buttons = display_div.find('.btn');
        display_buttons.removeClass(old_class);
        display_buttons.addClass(new_class);
        display_div.attr('data-class', new_class);
      }
    });
  },

  initDocChart: function() {
    chartColor = "#FFFFFF";

      // General configuration for the charts with Line gradientStroke
      gradientChartOptionsConfiguration = {
	  maintainAspectRatio: false,
	  legend: {
              display: false
	  },
	  tooltips: {
              bodySpacing: 4,
              mode: "nearest",
              intersect: 0,
              position: "nearest",
              xPadding: 10,
              yPadding: 10,
              caretPadding: 10
	  },
	  responsive: true,
	  scales: {
              yAxes: [{
		  display: 0,
		  gridLines: 0,
		  ticks: {
		      display: false
		  },
		  gridLines: {
		      zeroLineColor: "transparent",
		      drawTicks: false,
		      display: false,
		      drawBorder: false
		  }
              }],
              xAxes: [{
		  display: 0,
		  gridLines: 0,
		  ticks: {
		      display: false
		  },
		  gridLines: {
		      zeroLineColor: "transparent",
		      drawTicks: false,
		      display: false,
		      drawBorder: false
		  }
              }]
	  },
	  layout: {
              padding: {
		  left: 0,
		  right: 0,
		  top: 15,
		  bottom: 15
              }
	  }
      };

      ctx = document.getElementById('lineChartExample').getContext("2d");

      gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
      gradientStroke.addColorStop(0, '#80b6f4');
      gradientStroke.addColorStop(1, chartColor);

      gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
      gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
      gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");

      myChart = new Chart(ctx, {
	  type: 'line',
	  responsive: true,
	  data: {
              labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
              datasets: [{
		  label: "Active Users",
		  borderColor: "#f96332",
		  pointBorderColor: "#FFF",
		  pointBackgroundColor: "#f96332",
		  pointBorderWidth: 2,
		  pointHoverRadius: 4,
		  pointHoverBorderWidth: 1,
		  pointRadius: 4,
		  fill: true,
		  backgroundColor: gradientFill,
		  borderWidth: 2,
		  data: [542, 480, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
              }]
	  },
	  options: gradientChartOptionsConfiguration
      });
  },

    initDashboardPageCharts: function() {

	gradientChartOptionsConfigurationWithTooltipBlue = {
	    maintainAspectRatio: false,
	    legend: {
		display: false
	    },

	    tooltips: {
		backgroundColor: '#f5f5f5',
		titleFontColor: '#333',
		bodyFontColor: '#666',
		bodySpacing: 4,
		xPadding: 12,
		mode: "nearest",
		intersect: 0,
		position: "nearest"
	    },
	    responsive: true,
	    scales: {
		yAxes: [{
		    barPercentage: 1.6,
		    gridLines: {
			drawBorder: false,
			color: 'rgba(29,140,248,0.0)',
			zeroLineColor: "transparent",
		    },
		    ticks: {
			suggestedMin: 60,
			suggestedMax: 125,
			padding: 20,
			fontColor: "#2380f7"
		    }
		}],

		xAxes: [{
		    barPercentage: 1.6,
		    gridLines: {
			drawBorder: false,
			color: 'rgba(29,140,248,0.1)',
			zeroLineColor: "transparent",
		    },
		    ticks: {
			padding: 20,
			fontColor: "#2380f7"
		    }
		}]
	    }
	};

	gradientChartOptionsConfigurationWithTooltipPurple = {
	    maintainAspectRatio: false,
	    legend: {
		display: false
	    },

	    tooltips: {
		backgroundColor: '#f5f5f5',
		titleFontColor: '#333',
		bodyFontColor: '#666',
		bodySpacing: 4,
		xPadding: 12,
		mode: "nearest",
		intersect: 0,
		position: "nearest"
	    },
	    responsive: true,
	    scales: {
		yAxes: [{
		    barPercentage: 1.6,
		    gridLines: {
			drawBorder: false,
			color: 'rgba(29,140,248,0.0)',
			zeroLineColor: "transparent",
		    },
		    ticks: {
			suggestedMin: 60,
			suggestedMax: 125,
			padding: 20,
			fontColor: "#9a9a9a"
		    }
		}],

		xAxes: [{
		    barPercentage: 1.6,
		    gridLines: {
			drawBorder: false,
			color: 'rgba(225,78,202,0.1)',
			zeroLineColor: "transparent",
		    },
		    ticks: {
			padding: 20,
			fontColor: "#9a9a9a"
		    }
		}]
	    }
	};

	gradientChartOptionsConfigurationWithTooltipOrange = {
	    maintainAspectRatio: false,
	    legend: {
		display: false
	    },

	    tooltips: {
		backgroundColor: '#f5f5f5',
		titleFontColor: '#333',
		bodyFontColor: '#666',
		bodySpacing: 4,
		xPadding: 12,
		mode: "nearest",
		intersect: 0,
		position: "nearest"
	    },
	    responsive: true,
	    scales: {
		yAxes: [{
		    barPercentage: 1.6,
		    gridLines: {
			drawBorder: false,
			color: 'rgba(29,140,248,0.0)',
			zeroLineColor: "transparent",
		    },
		    ticks: {
			suggestedMin: 50,
			suggestedMax: 110,
			padding: 20,
			fontColor: "#ff8a76"
		    }
		}],

		xAxes: [{
		    barPercentage: 1.6,
		    gridLines: {
			drawBorder: false,
			color: 'rgba(220,53,69,0.1)',
			zeroLineColor: "transparent",
		    },
		    ticks: {
			padding: 20,
			fontColor: "#ff8a76"
		    }
		}]
	    }
	};

	gradientChartOptionsConfigurationWithTooltipGreen = {
	    maintainAspectRatio: false,
	    legend: {
		display: false
	    },

	    tooltips: {
		backgroundColor: '#f5f5f5',
		titleFontColor: '#333',
		bodyFontColor: '#666',
		bodySpacing: 4,
		xPadding: 12,
		mode: "nearest",
		intersect: 0,
		position: "nearest"
	    },
	    responsive: true,
	    scales: {
		yAxes: [{
		    barPercentage: 1.6,
		    gridLines: {
			drawBorder: false,
			color: 'rgba(29,140,248,0.0)',
			zeroLineColor: "transparent",
		    },
		    ticks: {
			suggestedMin: 50,
			suggestedMax: 125,
			padding: 20,
			fontColor: "#9e9e9e"
		    }
		}],

		xAxes: [{
		    barPercentage: 1.6,
		    gridLines: {
			drawBorder: false,
			color: 'rgba(0,242,195,0.1)',
			zeroLineColor: "transparent",
		    },
		    ticks: {
			padding: 20,
			fontColor: "#9e9e9e"
		    }
		}]
	    }
	};


	gradientBarChartConfiguration = {
	    maintainAspectRatio: false,
	    legend: {
		display: false
	    },

	    tooltips: {
		backgroundColor: '#f5f5f5',
		titleFontColor: '#333',
		bodyFontColor: '#666',
		bodySpacing: 4,
		xPadding: 12,
		mode: "nearest",
		intersect: 0,
		position: "nearest"
	    },
	    responsive: true,
	    scales: {
		yAxes: [{

		    gridLines: {
			drawBorder: false,
			color: 'rgba(29,140,248,0.1)',
			zeroLineColor: "transparent",
		    },
		    ticks: {
			suggestedMin: 60,
			suggestedMax: 120,
			padding: 20,
			fontColor: "#9e9e9e"
		    }
		}],

		xAxes: [{

		    gridLines: {
			drawBorder: false,
			color: 'rgba(29,140,248,0.1)',
			zeroLineColor: "transparent",
		    },
		    ticks: {
			padding: 20,
			fontColor: "#9e9e9e"
		    }
		}]
	    }
	};

	var ctx = document.getElementById("chartLinePurple").getContext("2d");

	var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

	gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
	gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
	gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors


var chart_labels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
	
	var chart_data = (document.getElementById("data").textContent === '') ?
	    null : JSON.parse(document.getElementById("data").textContent);

	var ctx = document.getElementById("chartBig1").getContext('2d');

	var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

	gradientStroke.addColorStop(1, 'rgba(72,72,176,0.1)');
	gradientStroke.addColorStop(0.4, 'rgba(72,72,176,0.0)');
	gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
	var config = {
	    type: 'line',
	    data: {
		labels: chart_labels,
		datasets: [{
		    label: "Document uploaded",
		    fill: true,
		    backgroundColor: gradientStroke,
		    borderColor: '#d346b1',
		    borderWidth: 2,
		    borderDash: [],
		    borderDashOffset: 0.0,
		    pointBackgroundColor: '#d346b1',
		    pointBorderColor: 'rgba(255,255,255,0)',
		    pointHoverBackgroundColor: '#d346b1',
		    pointBorderWidth: 20,
		    pointHoverRadius: 4,
		    pointHoverBorderWidth: 15,
		    pointRadius: 4,
		    data: chart_data.tot_month_doc
		}]
	    },
	    options: gradientChartOptionsConfigurationWithTooltipPurple
	};
	var myChartData = new Chart(ctx, config);
	$("#0").click(function() {
	    var data = myChartData.config.data;
	    data.datasets[0].data = chart_data;
	    data.labels = chart_labels;
	    myChartData.update();
	});
	$("#1").click(function() {
	    //var chart_data = [80, 120, 105, 110, 95, 105, 90, 100, 80, 95, 70, 120];
	    var data = myChartData.config.data;
	    data.datasets[0].data = chart_data;
	    data.labels = chart_labels;
	    myChartData.update();
	});

	$("#2").click(function() {
	    //var chart_data = [60, 80, 65, 130, 80, 105, 90, 130, 70, 115, 60, 130];
	    var data = myChartData.config.data;
	    data.datasets[0].data = chart_data;
	    data.labels = chart_labels;
	    myChartData.update();
	});

	var ctx = document.getElementById("CountryChart").getContext("2d");

	var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

	gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
	gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
	gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors


	data_values=[];
	if(chart_data.nlp_data.coll_d){
	    for(const [key,value] of Object.entries(chart_data.nlp_data.coll_d)) {
		data_values.push(value);
		
	    }
	}
	else {
	    
	}

	console.log(data_values);

	var myChart = new Chart(ctx, {
	    type: 'bar',
	    responsive: true,
	    legend: {
		display: false
	    },
	    data: {
		labels: ['ARTICLE', 'CASSATION', 'LOCATION', 'PERSON','DECREE','RG'],
		datasets: [{
		    label: "Metrics",
		    fill: true,
		    backgroundColor: gradientStroke,
		    hoverBackgroundColor: gradientStroke,
		    borderColor: '#1f8ef1',
		    borderWidth: 2,
		    borderDash: [],
		    borderDashOffset: 0.0,
		    data: data_values,
		}]
	    },
	    options: gradientBarChartConfiguration
	});

	
	var ctx = document.getElementById("CountryChart2").getContext("2d");
	
	keys=[];
	values=[];
	for(const [key,value] of Object.entries(chart_data.nlp_data.fname_d)) {
	    keys.push(key);
	    values.push(value);
	}

	var myChart2 = new Chart(ctx, {
	    type: 'bar',
	    responsive: true,
	    legend: {
		display: false
	    },
	    data: {
		labels: keys,
		datasets: [{
		    label: "Metrics",
		    fill: true,
		    backgroundColor: gradientStroke,
		    hoverBackgroundColor: gradientStroke,
		    borderColor: '#1f8ef1',
		    borderWidth: 2,
		    borderDash: [],
		    borderDashOffset: 0.0,
		    data: values,
		}]
	    },
	    options: gradientBarChartConfiguration
	});

    },
};
    
