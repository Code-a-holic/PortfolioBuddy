function render_pie_chart(){
    var xValues = []; //stock_names
    var yValues = []; //quantity_of_each_stock_held
    var barColors = ["#17153B", "#399918", "#FF7777", "#219C90", "#F9E2AF",
                     "#FFF455", "#FFC700", "#EE4E4E", "#4A249D", "#009FBD",
                     "#DC0083", "#304463", "#973131", "#FD9B63", "#F075AA",
                     "#78ABA8", "#003285", "#D2649A", "#FF9F66", "#03AED2",
                     "#640D6B", "#FC4100", "#94FFD8", "#643843", "#F2F597",
                     "#6895D2", "#FF6868", "#B19470", "#76453B", "#1B9C85",
                     "#30A2FF",
                    ];

    let xhr = new XMLHttpRequest();

    xhr.open('GET','get_stock_data', true);

    xhr.onload = function() {
        let response_data = JSON.parse(xhr.responseText);
        chart_data = response_data["stock_data"];
        for (var key in chart_data) { // Ensures own properties only (optional)
            xValues.push(key);
            yValues.push(chart_data[key]);
        }
        make_pie_chart([...xValues], [...yValues], barColors);
    }
    xhr.send();
}

function render_line_chart(){
    let stock_name = document.getElementById("inputGroupSelect01").value;

    let current_price = [];
    let buy_price = [];
    let dates = [];

    let xhr = new XMLHttpRequest();
    let url = 'current_price_vs_buy_price/' + stock_name;

    xhr.open('GET', url, true);

    xhr.onload = function() {
        let response_data = JSON.parse(xhr.responseText);
        stock_name = response_data["stock_name"];

        for (let key in response_data) { // Ensures own properties only (optional)
            if(key == "stock_name"){
                break;
            }else{
                dates.push(key);
                current_price.push(response_data[key]["current_price"]);
                buy_price.push(response_data[key]["buy_price"]);
            }
        }
        make_line_chart_rate_comparison(current_price, buy_price, stock_name, dates);
    }

    xhr.send();
}

function render_one_day_bar_chart(){
    let turn_over = []
    let delivery = []
    let stock_list = []
    let date_received = ""

    let date = document.getElementById("inputGroupSelect02").value

    let xhr = new XMLHttpRequest();
    let url = 'one_day_multiple_stocks/' + date;

    xhr.open('GET',url, true);

    xhr.onload = function() {
        let response_data = JSON.parse(xhr.responseText);


        for (let key in response_data) { // Ensures own properties only (optional)
            stock_list.push(key);
            turn_over.push(response_data[key]["turn_over_in_cr"]);
            delivery.push(response_data[key]["delivery_in_cr"]);
            date_received = response_data[key]["date"]
        }
        console.log(stock_list);
        make_one_date_bar_chart(stock_list, turn_over, delivery, date);
    }
    xhr.send();

}

function render_one_stock_bar_chart(){
    let stock_name = document.getElementById("inputGroupSelect03").value;

    let turn_over = [];
    let delivery = [];
    let dates = [];

    let xhr = new XMLHttpRequest();
    let url = 'current_price_vs_buy_price/' + stock_name;

    xhr.open('GET', url, true);

    xhr.onload = function() {
        let response_data = JSON.parse(xhr.responseText);
        stock_name = response_data["stock_name"];

        for (var key in response_data) { // Ensures own properties only (optional)
            if(key == "stock_name"){
                break;
            }else{
                dates.push(key);
                turn_over.push(response_data[key]["turn_over_in_cr"]);
                delivery.push(response_data[key]["delivery_in_cr"]);
            }
        }
        console.log(dates);
        make_one_stock_bar_chart(turn_over, delivery, dates, stock_name);
    }

    xhr.send();
}

function make_pie_chart(xValues, yValues, colors){
    new Chart(document.getElementById("portfolio_chart"), {
        type: "pie",
        data: {
            labels: xValues,
            datasets: [{
                backgroundColor: colors,
                borderWidth: 0,
                data: yValues,
                hoverOffset: 4,
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: true,
                    position: "left"
                }
            }
        }
    });
}

function make_line_chart_rate_comparison(current_price, buy_price, stock_name, dates){
    var chartInstance = Chart.getChart("rate_comparison_chart");

    // If chart instance exists, destroy it first
    if (chartInstance) {
        chartInstance.destroy();
    }

    new Chart(document.getElementById("rate_comparison_chart"), {
        type: "line",
        data: {
            labels: dates,
            datasets: [{
                label: "Current Price",
                data: current_price,
                borderColor: "blue",
                fill: false
            },{
                label: "Buy Price",
                data: buy_price,
                borderColor: "orange",
                fill: false
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: stock_name
                },
                legend: {
                    display: true // Change this to true if you want to display the legend
                }
            },
            scales: {
                x: {
                    beginAtZero: false // Add this if you want the x-axis to begin at zero
                },
                y: {
                    beginAtZero: false // Add this if you want the y-axis to begin at zero
                }
            }
        }
    });
}

function make_one_date_bar_chart(portfolio_list, turnover_in_cr, delivery_in_cr, date){
    var chartInstance = Chart.getChart("multiple_stocks_bar_chart");

    // If chart instance exists, destroy it first
    if (chartInstance) {
        chartInstance.destroy();
    }

    new Chart(document.getElementById("multiple_stocks_bar_chart"), {
        type: 'bar', // Default type for the chart
        data: {
            labels: portfolio_list,
            datasets: [{
                type: 'bar',
                label: 'Turnover (in Cr.)',
                data: turnover_in_cr,
                backgroundColor: 'blue',
            }, {
                type: 'bar',
                label: 'Delivery (in Cr.)',
                data: delivery_in_cr,
                backgroundColor: 'red'
            }]
        },
        options: {
            // Change the index axis to 'y'
            indexAxis: 'y',
            scales: {
                y: { // 'y' axis configuration
                    beginAtZero: true,
                    ticks: {
                        beginAtZero: true
                    }
                },
                x: { // 'x' axis configuration
                    beginAtZero: true,
                    ticks: {
                        beginAtZero: true
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: date
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });
}

function make_one_stock_bar_chart(turnover_in_cr, delivery_in_cr, date_list, stock_name){

    var chartInstance = Chart.getChart("single_stock_bar_chart");

    // If chart instance exists, destroy it first
    if (chartInstance) {
        chartInstance.destroy();
    }

    new Chart(document.getElementById("single_stock_bar_chart"), {
        type: 'bar', // Default type for the chart
        data: {
            labels: date_list,
            datasets: [{
                type: 'bar',
                label: 'Turnover (in Cr.)',
                data: turnover_in_cr,
                backgroundColor: 'blue',
            }, {
                type: 'bar',
                label: 'Delivery (in Cr.)',
                data: delivery_in_cr,
                backgroundColor: 'red'
            }]
        },
        options: {
            // Change the index axis to 'y'
            indexAxis: 'y',
            scales: {
                y: { // 'y' axis configuration
                    beginAtZero: true,
                    ticks: {
                        beginAtZero: true
                    }
                },
                x: { // 'x' axis configuration
                    beginAtZero: true,
                    ticks: {
                        beginAtZero: true
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: stock_name
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });
}

render_pie_chart();
render_line_chart();
render_one_day_bar_chart();
render_one_stock_bar_chart();
