// A function that get called whenever we are at the inventory section of the website
let inventoryInit = () => {
    let inventory = $('#active').parents('ul').find('li').eq(1).find('a');
    // Make the inventory section be active
    $('#active').removeAttr('id');
    inventory.attr('id','active');
}

// A function that searches the inventory
let searchInventory = (url,detailPath,editPath) => {
    $('#search-inventory').keyup(function(e){
        let q = $(this).val();
        $('#products').empty();
        $.post(
            url,
            {
                q,
                'csrfmiddlewaretoken': $('input[name = csrfmiddlewaretoken]').val()
            },
            function(data){
                let products = data.products;
                if(products.length > 0){
                    $('#no-products').empty();
                    for(product of products){
                        modifiedDetailPath = detailPath.split('/');
                        modifiedDetailPath[2] = String(product.id);
                        modifiedEditPath = editPath.split('/');
                        modifiedEditPath[2] = String(product.id);
                        $('#products').append(
                            `<div class="col-6 col-sm-6 col-md-4 col-xl-3 mt-2">
                                <div class="card h-100">
                                    <div class = 'options'>
                                       <a href="${modifiedEditPath.join('/')}">Edit</a>
                                       <span id = "${product.id}" class="delete-product">Delete</span>
                                    </div>
                                    <a href="${modifiedDetailPath.join('/')}">
                                        <img src="${ product.image }" height="250px" class="card-img-top" alt="">
                                        <div class="card-body p-2">
                                            <h6 class="text-dark" style="text-overflow: ellipsis;width: 100%;white-space: nowrap;overflow: hidden;">${ product.name }</h6>
                                            <p class="text-dark small m-auto">
                                               Quantity Left:
                                                <span class = 'text-primary'>${ product.qty }</span>
                                            </p>
                                            <p class="text-dark small m-auto">
                                               Unit Cost:
                                                <span class = 'text-primary'>GH&#8373; ${product.cost}</span>
                                            </p>
                                            <p class="text-dark small m-auto">
                                               Unit Price:
                                                <span class = 'text-primary'>GH&#8373; ${ product.price }</span>
                                            </p>
                                        </div>
                                    </a>
                                </div>
                            </div>`
                        );
                    }
                    // Add an event to the element
                    $('.delete-product').click(function(){
                        let productId = $(this).attr('id');
                        let productName = $(this).parents('div.card').find('div.card-body > h6').text();
                        $('#deleteProductLabel').text(`Delete ${productName}`); // Update the product name
                        $('#delete').data('productId',productId); // Store the product id
                        $('#deleteProduct').modal('show'); // Show the modal
                    });
                }
                else{
                    let newInventoryUrl = $('#new-inventory-create-url').attr('href');
                    $('#no-products').html(
                        `<h4 class="text-center" style="color: #535353">No Results Found</h4>
                        <a class='btn btn-primary d-block mt-3 m-auto' href='${newInventoryUrl}' style='max-width:400px'>Add Inventory</a>`
                    );
                }
            },
            'json'
        );
    });
}


// A function that deletes a product
let deleteProduct = (url) => {
    $(".delete-product").click(function(){
        let productId = $(this).attr('id');
        let productName = $(this).parents('div.card').find('div.card-body > h6').text();
        $('#deleteProductLabel').text(`Delete ${productName}`); // Update the product name
        $('#delete').data('productId',productId); // Store the product id
        $('#deleteProduct').modal('show'); // Show the modal
    });

    $('#delete').click(function(){
        let productId = $(this).data('productId');
        let csrfmiddlewaretoken = $('input[name = csrfmiddlewaretoken]').val();

        $.post(
            url,
            {
                productId,
                csrfmiddlewaretoken
            },
            function(data){
                // Hide the modal
                $('#deleteProduct').modal('hide');
                // Remove the element containing the product
                $(`.delete-product[id = ${productId}]`).parents('div.col-6').fadeOut(function(){
                    $(this).remove();
                })
            },
            'json'
        );
    });
}

// A function that provides information about a product for analysis
let productAnalysis = (url,productId,csrfmiddlewaretoken) => {

    $.post(
        url,
        {
            productId,
            csrfmiddlewaretoken
        },
        function(data){
            // Display past month
            $('#past-month').text(data['past_month']);
            // Create the chart

            // Sales Made For The Past 7 Days
            allGraphs('product-chart-7-days',data['data_for_7_days'],data['days_of_the_week'],'Sales Made For The Past 7 Days','Quantity')

            // Sales Made For Last Month
            allGraphs('product-chart-monthly',data['data_for_last_month'],data['weeks'],`Sales Made For Last Month -  ${data['past_month']}`,'Quantity')
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



// A function that gets called in the inventory create or update page
let inventoryCreateUpdateInit = () => {
    // Add bootsrap styles
    $('#id_name, #id_quantity, #id_unit_price, #id_unit').attr('class','form-control')
}

// A function that updates it's relative preview
let updatePreview = () => {
    // A function that formats the price and quantity
    let numberFormat = (value) => {
        let valueLst = String(value).split('.');
        if(valueLst.length > 1){
            valueLst[1] = valueLst[1].slice(0,2).padEnd(2,'0');
        }
        else{
            valueLst[1] = '00';
        }
        return `GH&#8373; ${valueLst.join('.')}`
    }

    // Product Name
    $('#id_name').keyup(function(){
        let value = $(this).val();
        value ? $("#name").text(value) : $("#name").text("Product Name");
    });

    // Product Quantity
    $('#id_quantity').keyup(function(){
        let value = $(this).val();
        value ? $("#qty").text(value) : $("#qty").text("1");
    });

    // Product Price
    $('#id_unit_price').keyup(function(){
        let value = $(this).val();
        value ? $("#price").html(numberFormat(value)) : $("#price").html("GH&#8373; 0.00");
    });

    // Product Image
    $('#id_image').change(function(){
        let image = document.getElementById('id_image').files[0];
        let file = new FileReader();
        file.onload = () => {
            $('#image').attr('src',file.result);
        }

        file.readAsDataURL(image)
    });

}


// A function that calcultes the profit of a product
let calculateProfit = () => {
    let cost = Number($('#cost').text().substring(4,).trim());
    let price = Number($('#price').text().substring(4,).trim());
    let profit = String(price - cost);
    let profitLst = profit.split('.');
    profitLst.length > 1 ? profitLst[1] = profitLst[1].slice(0,2).padEnd(2,'0') : profitLst[1] = '00';
    $('#profit').html(`GH&#8373; ${profitLst.join('.')}`)
}

