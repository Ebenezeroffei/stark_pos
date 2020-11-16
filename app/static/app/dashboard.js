let dashboardInit = (url,csrfmiddlewaretoken) => {
    let dashboard = $('#active').parents('ul').find('li').eq(0).find('a');
    // Make the dashboard section be active
    $('#active').removeAttr('id');
    dashboard.attr('id','active');

    $.post(
        url,
        {
            csrfmiddlewaretoken
        },
        function(data){
            // Create the graph
            // Sales Made For The Past 7 Days
            allGraphs('chart1',data['data_for_7_days'],data['days_of_the_week'],'Sales Made For The Past 7 Days','Quantity')
            // Highest Item Sold For The Past 7 Days
            allGraphs('chart2',data['data_for_maximum_item_sold'],data['days_of_the_week'],'Highest Item Sold For The Past 7 Days','Quantity','Quantity',true,data['product_name_for_maximum_item_sold'])
        },
        'json'
    );

}

// A function that draws all the graphs needed for the analysis section
let allGraphs = (el,data,labels,title,label,yAxesLabel = 'Quantity',customTooltip = false,customLabel = null) => {
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
                var $tooltip = $('#tooltip-' + dataPoint.datasetIndex);
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
//    console.log(tooltips())
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
