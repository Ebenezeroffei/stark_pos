let analysisInit = (url = null,csrfmiddlewaretoken = null) => {
    let analysis = $('#active').parents('ul').find('li').eq(3).find('a');
    // Make the analysis section be active
    $('#active').removeAttr('id');
    analysis.attr('id','active');
    if(url && csrfmiddlewaretoken){

        // Start the loader
        $('#loader').css('display','block');
        $('body').css('overflow','hidden');
        $.post(
            url,
            {
                csrfmiddlewaretoken
            },
            function(data){
                // Sop the loader
                $('#loader').css('display','none');
                $('body').css('overflow','auto');
    //            console.log(data);
                // Modify the card headers containing the graph
    //            $('#chart2, #chart5, #chart6').parents('div.card').find('div.card-header').text()
                // Product Analysis
    
                // Sales Made For The Past 7 Days
                allGraphs('chart1',data['sales_data_for_7_days'],data['days_of_the_week'],'Sales Made For The Past 7 Days','Quantity')
    
                // Sales Made For Last Month
                allGraphs('chart2',data['sales_data_for_last_month'],data['weeks'],`Sales Made For Last Month - ${data['past_month']}`,'Quantity')
    
                // Highest Item Sold For The Past 7 Days
                allGraphs('chart3',data['data_for_maximum_item_sold_last_7_days'],data['days_of_the_week'],'Highest Item Sold For The Past 7 Days','Quantity','Quantity',true,data['product_name_for_maximum_item_sold_last_7_days'],0)
    
                // Least Item Sold For The Past 7 Days
                allGraphs('chart4',data['data_for_minimum_item_sold_last_7_days'],data['days_of_the_week'],'Least Item Sold For The Past 7 Days','Quantity','Quantity',true,data['product_name_for_minimum_item_sold_last_7_days'],1)
    
                // Highest Item Sold For Last Month
                allGraphs('chart5',data['data_for_maximum_item_sold_last_month'],data['weeks'],`Highest Item Sold For Last Month - ${data['past_month']}`,'Quantity','Quantity',true,data['product_name_for_maximum_item_sold_last_month'],2)
    
                // Least Item Sold For Last Month
                allGraphs('chart6',data['data_for_minimum_item_sold_last_month'],data['weeks'],`Least Item Sold For Last Month - ${data['past_month']}`,'Quantity','Quantity',true,data['product_name_for_minimum_item_sold_last_month'],3)
    
                // Cost, Revenue And Profit For The Past 7 Days
                specialGraph('chart7',data['cost_for_the_past_7_days'],data['revenue_for_the_past_7_days'],data['profit_for_the_past_7_days'],data['days_of_the_week'],'Cost, Revenue And Profit For The Past 7 Days')
    
                // Cost, Revenue And Profit For Last Month
                specialGraph('chart8',data['cost_for_last_month'],data['revenue_for_last_month'],data['profit_for_last_month'],data['weeks'],'Cost, Revenue And Profit For Last Month')
    
            },
            'json'
        );
    }
}

// A function that draws all the graphs needed for the analysis section
let allGraphs = (el,data,labels,title,label,yAxesLabel = 'Quantity',customTooltip = false,customLabel = null,datasetIndex = 0) => {
    let chart1 = document.getElementById(el);

    // A function for creating custom tooltips
    let customTooltips = function(tooltip) {
        $(this._chart.canvas).css('cursor', 'pointer');

        var positionY = this._chart.canvas.offsetTop;
        var positionX = this._chart.canvas.offsetLeft;

        $('.chartjs-tooltip').css({
            opacity: 0,
        });


        if (!tooltip || !tooltip.opacity) {
            return;
        }

        if (tooltip.dataPoints.length > 0) {
            tooltip.dataPoints.forEach(function(dataPoint) {
                var content = [customLabel[dataPoint.index], dataPoint.yLabel].join(': ');
                var $tooltip = $('#tooltip-' + datasetIndex);
//                console.log(`Content = ${content}`);
                $tooltip.html(content);
                $tooltip.css({
                    opacity: 1,
                    top: positionY + dataPoint.y + 'px',
                    left: positionX + dataPoint.x - 35 + 'px',
                });
            });
        }
    };


    // A function that will create a custom tooltip based on the parameters provided by the user
    function tooltips(){
        if(customTooltip){
            return {
                mode: 'index',
                intersect: false,
                enabled: false,
                custom: customTooltips
            }
        }
        else{
            return {
                mode: 'index',
                intersect: false,
            }
        }
    }

    // Configurations
    let config = {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: label,
                    data:data,
                    backgroundColor: 'rgba(255, 206, 86, 0.5)',
//                    fill:false,
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(255, 206, 86, 1)',
                }
            ]
        },

        // Options
        options: {
            responsive: true,
            title: {
                display: true,
                text: title
            },
            tooltips: tooltips(),
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                yAxes: [
                    {
                        ticks: {
                            beginAtZero: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: yAxesLabel
                        }
                    }
                ]
            },
        }
    }

    let mychart = new Chart(chart1,config);
}


// A function that creates a special graph for elements with two or more datasets
let specialGraph = (el,cost,revenue,profit,labels,title) => {
    let chart1 = document.getElementById(el);

    // Configurations
    let config = {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Cost",
                    data:cost,
                    borderColor: 'rgb(255, 99, 132)',
                    borderWidth: 2,
                    fill:false,
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                },
                {
                    label: "Revenue",
                    data:revenue,
                    borderColor: 'rgb(54, 162, 235)',
                    borderWidth: 2,
                    fill:false,
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                },
                {
                    label: "Profit/Loss",
                    data:profit,
                    borderColor: 'rgb(255, 159, 64)',
                    borderWidth: 2,
                    fill:false,
                    pointBackgroundColor:'rgb(255, 159, 64)',
                }
            ]
        },

        // Options
        options: {
            responsive: true,
            title: {
                display: true,
                text: title
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                yAxes: [
                    {
                        ticks: {
                            beginAtZero: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'GHC'
                        }
                    }
                ]
            },
        }
    }

    let mychart = new Chart(chart1,config);
}
