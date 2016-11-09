/* script which generate the different charts with the parameters *
and all the options */
function oldCreateRequests() {
    /*
    example of creation for a simple serial chart, unused for now
    */
    "use strict";

    var chart, graph, categoryAxis, chartScrollbar;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmSerialChart();
    chart.pathToImages = "/static/optools/kpi/js/images/";
    chart.dataProvider = chartDataRequest;
    chart.categoryField = "date";

// CATEGORY AXIS ////////////////////////////
    categoryAxis = chart.categoryAxis;
    categoryAxis.parseDates = true;
    categoryAxis.equalSpacing = true;
    categoryAxis.minPeriod = "DD";

// GRAPH ////////////////////////////////////
    graph = new AmCharts.AmGraph();
    graph.valueField = "remained";
    graph.type = "line";

// SCROLLBAR ////////////////////////////////
    chartScrollbar = new AmCharts.ChartScrollbar();
    chartScrollbar.graph = graph;
    chartScrollbar.scrollbarHeight = 25;
    chart.addChartScrollbar(chartScrollbar);

    chart.addGraph(graph);
    chart.write('graphRequest');
}

/////////////////// REQUESTS ///////////////////////////////////////////////////

function createRequests(tv_view) {
    "use strict";

    var chart, graphRemained, graphRemained_external, dataset, categoryAxesSettings,
        stockPanelRemained, scrollbarSettings, cursorSettings, periodSelector,
        panelsSettings, graphOpened, stockPanelOpened, graphClosed,
        stockPanelClosed, stockLegendRemained, stockLegendOpened,
        stockLegendClosed, period_value, graphLifetimeGlobal,
        stockPanelLifetime, stockLegendLifetime, graphLifetimeNormal,
        graphLifetimeHigh, graphLifetimeUrgent, graphWaiting, graphWaiting_external,
        graphOpened_external, graphClosed_external, graphLifetimeGlobal_external;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/optools/kpi/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "remained",
        toField: "remained"
    }, {
        fromField: "remained_external",
        toField: "remained_external"
    },{
        fromField: "opened",
        toField: "opened"
    },{
        fromField: "opened_external",
        toField: "opened_external"
    }, {
        fromField: "closed",
        toField: "closed"
    }, {
        fromField: "closed_external",
        toField: "closed_external"
    }, {
        fromField: "global",
        toField: "global"
    }, {
        fromField: "lifetime_external",
        toField: "lifetime_external"
    },  {
        fromField: "normal",
        toField: "normal"
    }, {
        fromField: "high",
        toField: "high"
    }, {
        fromField: "urgent",
        toField: "urgent"
    }, {
        fromField: "url",
        toField: "url"
    }, {
        fromField: "comment_lifetime",
        toField: "comment_lifetime"
    }, {
        fromField: "lifetime_aim",
        toField: "lifetime_aim"
    }, {
        fromField: "requests_waiting",
        toField: "requests_waiting"
    },{
        fromField: "requests_waiting_external",
        toField: "requests_waiting_external"
    }];

    dataset.dataProvider = chartDataRequest;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];
    chart.balloon.showBullet = false;
    // Allow the user to click on the graph bullet to open an url and not on the balloon bullet

// PANELS ///////////////////////////////////

//  1.1) graph Remained
    period_value = "Average";

    graphRemained = new AmCharts.StockGraph();
    graphRemained.valueField = "remained"; // Field used to draw the graph
    graphRemained.urlField = "url"; // Field containing the url to open if the user click on the graph
    graphRemained.urlTarget = "_blank"; // Open the url into a new tab
    graphRemained.type = "line"; // Draw the graph with a line form. others options are smoothedLine and columns
    graphRemained.title = "Remained"; // Title of the graph
    graphRemained.hideBulletsCount = 100; // Show the bullet if there is less than 100 data shown on the graph
    graphRemained.bulletSize = 8; // Increase the default bullet size to allow the users to click more easily on it
    graphRemained.bullet = "bubble"; // Style of the bullets
    graphRemained.lineThickness = 2; // Increase default line thickness
    graphRemained.lineColor = "#FF0000"; // Change the color of the line
    graphRemained.useDataSetColors = false; // Use custom colors and not default colors
    graphRemained.periodValue = "Close"; // When the data are show for each week,
                                         // it will draw the final value of the week
                                         
    //  1.1b) graph Remained_external
    graphRemained_external = new AmCharts.StockGraph();
    graphRemained_external.valueField = "remained_external";
    graphRemained_external.urlField = "url";
    graphRemained_external.urlTarget = "_blank";
    graphRemained_external.type = "line";
    graphRemained_external.title = "Remained External";
    graphRemained_external.hideBulletsCount = 100;
    graphRemained_external.bulletSize = 8;
    graphRemained_external.bullet = "bubble";
    graphRemained_external.fillAlphas = 0.6;
    graphRemained_external.lineThickness = 2;
    graphRemained_external.lineColor = "#FF0055";
    graphRemained_external.useDataSetColors = false;
    graphRemained_external.periodValue = "Close";
    
//  1.1b) graph waiting
    graphWaiting = new AmCharts.StockGraph();
    graphWaiting.valueField = "requests_waiting";
    graphWaiting.urlField = "url";
    graphWaiting.urlTarget = "_blank";
    graphWaiting.type = "line";
    graphWaiting.title = "Waiting";
    graphWaiting.hideBulletsCount = 35;
    graphWaiting.bulletSize = 8;
    graphWaiting.bullet = "bubble";
    graphWaiting.fillAlphas = 0.8;
    graphWaiting.lineThickness = 2;
    graphWaiting.lineColor = "#666699";
    graphWaiting.useDataSetColors = false;
    graphWaiting.periodValue = "Close";
    
    //  1.1b) graph waiting_external
    graphWaiting_external = new AmCharts.StockGraph();
    graphWaiting_external.valueField = "requests_waiting_external";
    graphWaiting_external.urlField = "url";
    graphWaiting_external.urlTarget = "_blank";
    graphWaiting_external.type = "line";
    graphWaiting_external.title = "Waiting External";
    graphWaiting_external.hideBulletsCount = 35;
    graphWaiting_external.bulletSize = 8;
    graphWaiting_external.bullet = "bubble";
    graphWaiting_external.fillAlphas = 0.8;
    graphWaiting_external.lineThickness = 2;
    graphWaiting_external.lineColor = "#666655";
    graphWaiting_external.useDataSetColors = false;
    graphWaiting_external.periodValue = "Close";

//  1.1) stockPanel Remained
    stockPanelRemained = new AmCharts.StockPanel();
    stockPanelRemained.title = "Requests"; // Title of the panel
    stockPanelRemained.percentHeight = 25; // Height of the panel over 100
    stockPanelRemained.addStockGraph(graphRemained); // Add the graph to the panel
    stockPanelRemained.addStockGraph(graphWaiting); // Add the graph to the panel
    stockPanelRemained.addStockGraph(graphRemained_external);
    stockPanelRemained.addStockGraph(graphWaiting_external);
    stockPanelRemained.showCategoryAxis = true; // hide the dates under this panel

//  1.1) stockLegend Remained
    stockLegendRemained = new AmCharts.StockLegend();
    stockLegendRemained.switchable = true; // Disable the options to hide the graph by clicking on his name
    stockPanelRemained.stockLegend = stockLegendRemained;

//  1.2) graph Opened
    graphOpened = new AmCharts.StockGraph();
    graphOpened.valueField = "opened";
    graphOpened.urlField = "url";
    graphOpened.urlTarget = "_blank";
    graphOpened.type = "column";
    graphOpened.title = "Opened";
    // graphOpened.hideBulletsCount = 50;
    // graphOpened.bullet = "bubble";
    graphOpened.lineThickness = 2;
    graphOpened.lineColor = "#FF9900";
    graphOpened.useDataSetColors = false;
    graphOpened.fillAlphas = 1;
    graphOpened.periodValue = "Sum"; // When the data are show for each week,
                                     // it will draw the sum of all the values of the week
    graphOpened.cornerRadiusTop = 2; // round the corners of the columns
    
    graphOpened_external = new AmCharts.StockGraph();
    graphOpened_external.valueField = "opened_external";
    graphOpened_external.urlField = "url";
    graphOpened_external.urlTarget = "_blank";
    graphOpened_external.type = "column";
    graphOpened_external.title = "Opened External";
    // graphOpened.hideBulletsCount = 50;
    // graphOpened.bullet = "bubble";
    graphOpened_external.lineThickness = 2;
    graphOpened_external.lineColor = "#C4300C";
    graphOpened_external.useDataSetColors = false;
    graphOpened_external.fillAlphas = 1;
    graphOpened_external.periodValue = "Sum"; // When the data are show for each week,
                                     // it will draw the sum of all the values of the week
    graphOpened_external.cornerRadiusTop = 2; // round the corners of the columns

//  1.2) stockPanel Opened (& Closed)
    stockPanelOpened = new AmCharts.StockPanel();
    stockPanelOpened.percentHeight = 25;
    stockPanelOpened.showCategoryAxis = true;
    stockPanelOpened.addStockGraph(graphOpened);
    stockPanelOpened.addStockGraph(graphOpened_external);

//  1.2) stockLegend Opened (& Closed)
    stockLegendOpened = new AmCharts.StockLegend();
    stockPanelOpened.stockLegend = stockLegendOpened;

//  1.3) graph Closed
    graphClosed = new AmCharts.StockGraph();
    graphClosed.valueField = "closed";
    graphClosed.urlField = "url";
    graphClosed.urlTarget = "_blank";
    graphClosed.title = "Closed";
    graphClosed.hideBulletsCount = 35;
    graphClosed.bullet = "bubble";
    graphClosed.lineThickness = 2;
    graphClosed.type = "line";
    graphClosed.fillColor = "#00CC00";
    graphClosed.lineColor = "#00CC00";
    graphClosed.useDataSetColors = false;
//    graphClosed.fillAlphas = 0.15;
    graphClosed.cornerRadiusTop = 2;
    graphClosed.periodValue = "Sum";
    stockPanelOpened.addStockGraph(graphClosed);
    
    graphClosed_external = new AmCharts.StockGraph();
    graphClosed_external.valueField = "closed_external";
    graphClosed_external.urlField = "url";
    graphClosed_external.urlTarget = "_blank";
    graphClosed_external.title = "Closed External";
    graphClosed_external.hideBulletsCount = 35;
    graphClosed_external.bullet = "bubble";
    graphClosed_external.lineThickness = 2;
    graphClosed_external.type = "line";
    graphClosed_external.fillColor = "#DC60AF";
    graphClosed_external.lineColor = "#DC60AF";
    graphClosed_external.useDataSetColors = false;
//    graphClosed.fillAlphas = 0.15;
    graphClosed_external.cornerRadiusTop = 2;
    graphClosed_external.periodValue = "Sum";
    stockPanelOpened.addStockGraph(graphClosed_external);


//  2.1) graph Lifetime Global
    period_value = "Average";

    graphLifetimeGlobal = new AmCharts.StockGraph();
    graphLifetimeGlobal.valueField = "global";
    graphLifetimeGlobal.type = "line";
    graphLifetimeGlobal.title = "Global";
    graphLifetimeGlobal.descriptionField = "comment_lifetime";
    graphLifetimeGlobal.balloonText += "\n[[description]]";
    graphLifetimeGlobal.hideBulletsCount = 35;
    graphLifetimeGlobal.bullet = "bubble";
    graphLifetimeGlobal.lineThickness = 2;
    graphLifetimeGlobal.hidden = false;
    graphLifetimeGlobal.lineColor = "#84815B";
    graphLifetimeGlobal.useDataSetColors = false;
    graphLifetimeGlobal.fillAlphas = 0.1;
    graphLifetimeGlobal.periodValue = period_value;
    
    graphLifetimeGlobal_external = new AmCharts.StockGraph();
    graphLifetimeGlobal_external.valueField = "lifetime_external";
    graphLifetimeGlobal_external.type = "line";
    graphLifetimeGlobal_external.title = "Global External";
    graphLifetimeGlobal_external.descriptionField = "comment_lifetime";
    graphLifetimeGlobal_external.balloonText += "\n[[description]]";
    graphLifetimeGlobal_external.hideBulletsCount = 35;
    graphLifetimeGlobal_external.bullet = "bubble";
    graphLifetimeGlobal_external.lineThickness = 2;
    graphLifetimeGlobal_external.hidden = false;
    graphLifetimeGlobal_external.lineColor = "#855166";
    graphLifetimeGlobal_external.useDataSetColors = false;
    graphLifetimeGlobal_external.fillAlphas = 0.1;
    graphLifetimeGlobal_external.periodValue = period_value;

// graph Lifetime Aim
    var graphLifetimeAim = new AmCharts.StockGraph();
    graphLifetimeAim.valueField = "lifetime_aim";
    graphLifetimeAim.type = "line";
    graphLifetimeAim.title = "Aim";
    graphLifetimeAim.lineThickness = 2;
    graphLifetimeAim.lineColor = "#00FF00";
    graphLifetimeAim.useDataSetColors = false;
    //graphLifetimeAim.visibleInLegend = false;
    graphLifetimeAim.periodValue = period_value;

//  2.1) stockPanel Lifetime (all)
    stockPanelLifetime = new AmCharts.StockPanel();
    stockPanelLifetime.title = "Lifetime";
    stockPanelLifetime.percentHeight = 50;
    stockPanelLifetime.addStockGraph(graphLifetimeAim);
    stockPanelLifetime.addStockGraph(graphLifetimeGlobal);
    stockPanelLifetime.addStockGraph(graphLifetimeGlobal_external);

//  2.1) stockLegend Lifetime (all)
    stockLegendLifetime = new AmCharts.StockLegend();
    stockPanelLifetime.stockLegend = stockLegendLifetime;

//  2.2) graph Lifetime Normal
    graphLifetimeNormal = new AmCharts.StockGraph();
    graphLifetimeNormal.valueField = "normal";
    graphLifetimeNormal.type = "line";
    graphLifetimeNormal.title = "Normal";
    graphLifetimeNormal.hideBulletsCount = 35;
    graphLifetimeNormal.bullet = "bubble";
//    graphLifetimeNormal.balloonText += " days";
    graphLifetimeNormal.hidden = true;
    graphLifetimeNormal.lineThickness = 2;
    graphLifetimeNormal.lineColor = "#0066FF";
    graphLifetimeNormal.useDataSetColors = false;
    graphLifetimeNormal.fillAlphas = 0.1;
    graphLifetimeNormal.periodValue = period_value;
    graphLifetimeNormal.cornerRadiusTop = 2;

    stockPanelLifetime.addStockGraph(graphLifetimeNormal);

//  2.3) graph Lifetime High
    graphLifetimeHigh = new AmCharts.StockGraph();
    graphLifetimeHigh.valueField = "high";
    graphLifetimeHigh.type = "line";
    graphLifetimeHigh.title = "High";
    graphLifetimeHigh.hideBulletsCount = 35;
    graphLifetimeHigh.bullet = "bubble";
//    graphLifetimeHigh.balloonText += " days";
    graphLifetimeHigh.hidden = true;
    graphLifetimeHigh.lineThickness = 2;
    graphLifetimeHigh.lineColor = "#FF9900";
    graphLifetimeHigh.useDataSetColors = false;
    graphLifetimeHigh.fillAlphas = 0.1;
    graphLifetimeHigh.periodValue = period_value;
    graphLifetimeHigh.cornerRadiusTop = 2;

    stockPanelLifetime.addStockGraph(graphLifetimeHigh);

//  2.4) graph Lifetime Urgent
    graphLifetimeUrgent = new AmCharts.StockGraph();
    graphLifetimeUrgent.valueField = "urgent";
    graphLifetimeUrgent.type = "line";
    graphLifetimeUrgent.title = "Urgent";
    graphLifetimeUrgent.hideBulletsCount = 35;
    graphLifetimeUrgent.bullet = "bubble";
    graphLifetimeUrgent.hidden = true;
    graphLifetimeUrgent.lineThickness = 2;
    graphLifetimeUrgent.lineColor = "#FF0000";
    graphLifetimeUrgent.useDataSetColors = false;
    graphLifetimeUrgent.fillAlphas = 0.1;
    graphLifetimeUrgent.periodValue = period_value;
    graphLifetimeUrgent.cornerRadiusTop = 2;

    stockPanelLifetime.usePrefixes = true;
    stockPanelLifetime.prefixesOfBigNumbers = [{number:24,prefix:" days"}];
    stockPanelLifetime.addStockGraph(graphLifetimeUrgent);



    chart.panels = [stockPanelRemained, stockPanelOpened, stockPanelLifetime];
// OTHER SETTINGS (scrollBar & cursor)
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.graph = graphRemained;
    scrollbarSettings.updateOnReleaseOnly = false;
    chart.chartScrollbarSettings = scrollbarSettings;

    cursorSettings = new AmCharts.ChartCursorSettings();
    cursorSettings.valueBalloonsEnabled = true;
    chart.chartCursorSettings = cursorSettings;

// PERIOD SELECTOR //////////////////////////
    periodSelector = new AmCharts.PeriodSelector();
    periodSelector.periods = [{
			period : "DD",
			count : 10,
			label : "10 days"
		}, 
		{
	        period: "DD",
	        count: 15,
	        label: "2 Weeks"
	    },{
			period : "MM",
			count : 1,
			label : "1 month"
		},
		 {
	        period: "MM",
	        selected : true,
	        count: 3,
	        label: "3 Month"

	    }, {
	        period: "MM",
	        count: 6,
	        label: "6 Months"
	    }, {
			period : "YYYY",
			count : 1,
			label : "1 year"
		}, {
        period: "MAX",
        label: "MAX",
        selected: false
    }];
    
    	chart.periodSelector = periodSelector;
	
// PANEL SETTING ////////////////////////////
    panelsSettings = new AmCharts.PanelsSettings();
    panelsSettings.usePrefixes = true;
    panelsSettings.panEventsEnabled = true;
//    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' ', decimalSeparator: '.'};
//    panelsSettings.usePrefixes = false;

    chart.panelsSettings = panelsSettings;
 
    chart.balloon.bulletSize = 4;
    chart.addListener('dataUpdated', function (event){
        deleteAmChart();
    });
    chart.addListener('zoomed', function (event) {
        deleteAmChart();
    });
    chart.write('graphRequest');
    deleteAmChart();
}

function createHosts(tv_view) {
    "use strict";
    var chart, categoryAxesSettings, dataset, graphHosts, stockPanelHosts,
        stockLegendHosts, graphServices, stockPanelServices,
        stockLegendServices, scrollbarSettings, cursorSettings, periodSelector,
        panelsSettings, graphApps, stockPanelApps, stockLegendApps,
        graphHostsDown, stockPanelHostsDown,
        stockLegendHostsDown;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/optools/kpi/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "total_host",
        toField: "total_host"
    }, {
        fromField: "total_services",
        toField: "total_services"
    },{
        fromField: "total_app",
        toField: "total_app"
    },{
    	fromField: "nb_host_down",
    	toField: "nb_host_down"
    }, {
        fromField: "comment_host",
        toField: "comment_host"
    }, {
        fromField: "comment_service",
        toField: "comment_service"
    }];
    dataset.dataProvider = chartDataNagios;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

    // PANELS ///////////////////////////////////

//  1) graph Hosts

    graphHosts = new AmCharts.StockGraph();
    graphHosts.valueField = "total_host";
    graphHosts.descriptionField = "comment_host";
    graphHosts.balloonText += "\n[[description]]";
    graphHosts.type = "line";
    graphHosts.title = "Hosts";
    graphHosts.hideBulletsCount = 35;
    graphHosts.bullet = "bubble";
    graphHosts.lineThickness = 2;
    graphHosts.lineColor = "#0066FF";
    graphHosts.useDataSetColors = false;
    graphHosts.periodValue = "Average";

//  1) stockPanel Hosts
    stockPanelHosts = new AmCharts.StockPanel();
    stockPanelHosts.title = "Total Hosts";
    stockPanelHosts.percentHeight = 50;
    stockPanelHosts.addStockGraph(graphHosts);
    stockPanelHosts.showCategoryAxis = false;

//  1) stockLegend Hosts
    stockLegendHosts = new AmCharts.StockLegend();
    stockLegendHosts.switchable = false;
    stockPanelHosts.stockLegend = stockLegendHosts;

//  2) graph Services

    graphServices = new AmCharts.StockGraph();
    graphServices.valueField = "total_services";
    graphServices.descriptionField = "comment_service";
    graphServices.balloonText += "\n[[description]]";
    graphServices.type = "line";
    graphServices.hideBulletsCount = 35;
    graphServices.bullet = "bubble";
    graphServices.title = "Services";
    graphServices.lineThickness = 2;
    graphServices.useDataSetColors = true;
    graphServices.periodValue = "Average";

//  2) stockPanel Services
    stockPanelServices = new AmCharts.StockPanel();
    stockPanelServices.title = "Total Services";
    stockPanelServices.percentHeight = 50;
    stockPanelServices.addStockGraph(graphServices);
    stockPanelServices.showCategoryAxis = false;

//  2) stockLegend Services
    stockLegendServices = new AmCharts.StockLegend();
    stockLegendServices.switchable = false;
    stockPanelServices.stockLegend = stockLegendServices;

    
//  3) graph Apps

    graphApps = new AmCharts.StockGraph();
    graphApps.valueField = "total_app";
    graphApps.descriptionField = "comment_service";
    graphApps.balloonText += "\n[[description]]";
    graphApps.type = "line";
    graphApps.hideBulletsCount = 35;
    graphApps.bullet = "bubble";
    graphApps.title = "Apps";
    graphApps.lineColor = "#186111";
    graphApps.lineThickness = 2;
    graphApps.useDataSetColors = false;
    graphApps.periodValue = "Average";

//  3) stockPanel Apps
    stockPanelApps = new AmCharts.StockPanel();
    stockPanelApps.title = "Total Apps";
    stockPanelApps.percentHeight = 50;
    stockPanelApps.addStockGraph(graphApps);
    stockPanelApps.showCategoryAxis = false;

//  3) stockLegend Apps
    stockLegendApps = new AmCharts.StockLegend();
    stockLegendApps.switchable = false;
    stockPanelApps.stockLegend = stockLegendApps;
    
//  3) graph nb_host_down

    graphHostsDown = new AmCharts.StockGraph();
    graphHostsDown.valueField = "nb_host_down";
    graphHostsDown.descriptionField = "nb_host_down";
//    graphHostsDown.balloonText += "\n[[nb_host_down]]";
    graphHostsDown.type = "line";
    graphHostsDown.hideBulletsCount = 35;
    graphHostsDown.bullet = "bubble";
    graphHostsDown.title = "Hosts Down";
    graphHostsDown.lineColor = "#CC0000";
    graphHostsDown.lineThickness = 2;
    graphHostsDown.useDataSetColors = false;
    graphHostsDown.periodValue = "Average";

//  3) stockPanel nb_host_down
    stockPanelHostsDown = new AmCharts.StockPanel();
    stockPanelHostsDown.title = "Total Hosts Down ";
    stockPanelHostsDown.percentHeight = 50;
    stockPanelHostsDown.addStockGraph(graphHostsDown);

//  3) stockLegend nb_host_down
    stockLegendHostsDown = new AmCharts.StockLegend();
    stockLegendHostsDown.switchable = false;
    stockPanelHostsDown.stockLegend = stockLegendHostsDown;

    chart.panels = [stockPanelHosts, stockPanelServices, stockPanelApps, stockPanelHostsDown];
// OTHER SETTINGS (scrollBar & cursor)
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.graph = graphServices;
    scrollbarSettings.updateOnReleaseOnly = false;
    chart.chartScrollbarSettings = scrollbarSettings;

    cursorSettings = new AmCharts.ChartCursorSettings();
    cursorSettings.valueBalloonsEnabled = true;
    chart.chartCursorSettings = cursorSettings;

// PERIOD SELECTOR //////////////////////////
    periodSelector = new AmCharts.PeriodSelector();
    periodSelector.periods = [{
			period : "DD",
			count : 10,
			label : "10 days"
		}, 
		{
	        period: "DD",
	        count: 15,
	        label: "2 Weeks"
	    },{
			period : "MM",
			count : 1,
			label : "1 month"
		},
		 {
	        period: "MM",
	        selected : true,
	        count: 3,
	        label: "3 Month"

	    }, {
	        period: "MM",
	        count: 6,
	        label: "6 Months"
	    }, {
			period : "YYYY",
			count : 1,
			label : "1 year"
		}, {
        period: "MAX",
        label: "MAX",
        selected: false
    }];
    chart.periodSelector = periodSelector;

// PANEL SETTING ////////////////////////////
    panelsSettings = new AmCharts.PanelsSettings();
    panelsSettings.usePrefixes = true;
    panelsSettings.panEventsEnabled = true;
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' ', decimalSeparator: '.'};
    panelsSettings.usePrefixes = false;
    
    chart.panelsSettings = panelsSettings;
    chart.balloon.bulletSize = 4;
    chart.addListener('dataUpdated', function (event){
        deleteAmChart();
    });
    chart.addListener('zoomed', function (event) {
        deleteAmChart();
    });
    chart.write('graphHosts');
    deleteAmChart();
}

function createWritten() {
    "use strict";
    var chart, categoryAxesSettings, dataset, graphWritten, stockPanelWritten,
        stockLegendWritten, graphMissing, scrollbarSettings, cursorSettings,
        periodSelector, panelsSettings, valueAxesSettings;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/optools/kpi/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// valueAxesSettings
    valueAxesSettings = new AmCharts.ValueAxesSettings();
    valueAxesSettings.stackType = "regular";
    chart.valueAxesSettings = valueAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "written_procedures",
        toField: "written_procedures"
    }, {
        fromField: "total_written",
        toField: "total_written"
    }, {
        fromField: "missing_procedures",
        toField: "missing_procedures"
    }, {
        fromField: "total_missing",
        toField: "total_missing"
    },{
        fromField: "comment_procedure",
        toField: "comment_procedure"
    }];
    dataset.dataProvider = chartDataProcedures;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

// PANELS ///////////////////////////////////

//  1) graph Written

    graphWritten = new AmCharts.StockGraph();
    graphWritten.valueField = "written_procedures";
    graphWritten.descriptionField = "comment_procedure";
    graphWritten.type = "line";
    graphWritten.title = "Written procedures";
    graphWritten.balloonText += " ([[percents]]%)";
    graphWritten.balloonText += " related services: [[total_written]]";
    graphWritten.balloonText += "\n[[description]]";
    graphWritten.lineColor = "#00CC00";
    graphWritten.lineThickness = 2;
    graphWritten.fillColor = "#00CC00";
    graphWritten.useDataSetColors = false;
    graphWritten.periodValue = "Average";
    graphWritten.fillAlphas = 0.7;
    graphWritten.stacked = true;
    graphWritten.hideBulletsCount = 35;
    graphWritten.bullet = "bubble";

//  1) stockPanel Written
    stockPanelWritten = new AmCharts.StockPanel();
    stockPanelWritten.title = "Total Written & Missing procedures";
    stockPanelWritten.percentHeight = 50;

//  1) stockLegend Written
    stockLegendWritten = new AmCharts.StockLegend();
    stockLegendWritten.valueTextRegular = "[[percents]]%";
    stockPanelWritten.stockLegend = stockLegendWritten;

//  2) graph Missing

    graphMissing = new AmCharts.StockGraph();
    graphMissing.valueField = "missing_procedures";
//    graphMissing.descriptionField = "comment_procedure";
    graphMissing.type = "line";
    graphMissing.title = "Missing procedures";
    graphMissing.balloonText += " ([[percents]]%)";
    graphMissing.balloonText += " related services: [[total_missing]]";
    graphMissing.balloonText += "\n[[description]]";
    graphMissing.lineColor = "#FF0000";
    graphMissing.lineThickness = 2;
    graphMissing.fillColor = "#FF0000";
    graphMissing.useDataSetColors = false;
    graphMissing.periodValue = "Average";
    graphMissing.fillAlphas = 0.7;
    graphMissing.stacked = true;
    graphMissing.hideBulletsCount = 35;
    graphMissing.bullet = "bubble";

    stockPanelWritten.addStockGraph(graphWritten);
    stockPanelWritten.addStockGraph(graphMissing);

    chart.panels = [stockPanelWritten];

// OTHER SETTINGS (scrollBar & cursor)
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.updateOnReleaseOnly = false;
    chart.chartScrollbarSettings = scrollbarSettings;

    cursorSettings = new AmCharts.ChartCursorSettings();
    cursorSettings.valueBalloonsEnabled = true;
    chart.chartCursorSettings = cursorSettings;

// PERIOD SELECTOR //////////////////////////
    periodSelector = new AmCharts.PeriodSelector();
    periodSelector.periods = [{
			period : "DD",
			count : 10,
			label : "10 days"
		}, 
		{
	        period: "DD",
	        count: 15,
	        label: "2 Weeks"
	    },{
			period : "MM",
			count : 1,
			label : "1 month"
		},
		 {
	        period: "MM",
	        selected : true,
	        count: 3,
	        label: "3 Month"

	    }, {
	        period: "MM",
	        count: 6,
	        label: "6 Months"
	    }, {
			period : "YYYY",
			count : 1,
			label : "1 year"
		}, {
        period: "MAX",
        label: "MAX",
        selected: false
    }];
    chart.periodSelector = periodSelector;

// PANEL SETTING ////////////////////////////
    panelsSettings = new AmCharts.PanelsSettings();
    panelsSettings.usePrefixes = true;
    panelsSettings.panEventsEnabled = true;
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' ', decimalSeparator: '.'};
    panelsSettings.usePrefixes = false;

    chart.panelsSettings = panelsSettings;
    chart.balloon.bulletSize = 4;
    chart.addListener('dataUpdated', function (event){
        deleteAmChart();
    });
    chart.addListener('zoomed', function (event) {
        deleteAmChart();
    });
    chart.write('graphWritten');
    deleteAmChart();
}

function createEquipements(tv_view) {
    "use strict";
    var chart, categoryAxesSettings, dataset, graphLinux, stockPanelLinux,
        stockLegendLinux, graphWindows, graphAix, scrollbarSettings,
        cursorSettings, periodSelector, panelsSettings, valueAxesSettings;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/optools/kpi/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// valueAxesSettings
    valueAxesSettings = new AmCharts.ValueAxesSettings();
    valueAxesSettings.stackType = "regular";
    chart.valueAxesSettings = valueAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "linux",
        toField: "linux"
    }, {
        fromField: "windows",
        toField: "windows"
    }, {
        fromField: "aix",
        toField: "aix"
    }];
    dataset.dataProvider = chartDataNagios;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

// PANELS ///////////////////////////////////

//  1) graph Linux

    graphLinux = new AmCharts.StockGraph();
    graphLinux.valueField = "linux";
    graphLinux.type = "line";
    graphLinux.title = "Linux";
    graphLinux.balloonText += " ([[percents]]%)";
    graphLinux.lineColor = "#FFCC00";
    graphLinux.lineThickness = 2;
    graphLinux.fillColor = "#FFCC00";
    graphLinux.useDataSetColors = false;
    graphLinux.periodValue = "Average";
    graphLinux.fillAlphas = 0.7;
    graphLinux.stacked = false;
    graphLinux.hideBulletsCount = 35;
    graphLinux.bullet = "bubble";

//  1) stockPanel Linux
    stockPanelLinux = new AmCharts.StockPanel();
    stockPanelLinux.title = "Number Of Equipement";
    stockPanelLinux.percentHeight = 50;

//  1) stockLegend Linux
    stockLegendLinux = new AmCharts.StockLegend();
    stockLegendLinux.valueTextRegular = "[[percents]]%";
    stockPanelLinux.stockLegend = stockLegendLinux;

//  2) graph Windows

    graphWindows = new AmCharts.StockGraph();
    graphWindows.valueField = "windows";
    graphWindows.type = "line";
    graphWindows.title = "Windows";
    graphWindows.balloonText += " ([[percents]]%)";
    graphWindows.lineColor = "#0066FF";
    graphWindows.lineThickness = 2;
    graphWindows.fillColor = "#0066FF";
    graphWindows.useDataSetColors = false;
    graphWindows.periodValue = "Average";
    graphWindows.fillAlphas = 0.7;
    graphWindows.stacked = false;
    graphWindows.hideBulletsCount = 35;
    graphWindows.bullet = "bubble";

//  3) graph Aix

    graphAix = new AmCharts.StockGraph();
    graphAix.valueField = "aix";
    graphAix.type = "line";
    graphAix.title = "Aix";
    graphAix.balloonText += " ([[percents]]%)";
    graphAix.lineColor = "#FF0000";
    graphAix.lineThickness = 2;
    graphAix.fillColor = "#FF0000";
    graphAix.useDataSetColors = false;
    graphAix.periodValue = "Average";
    graphAix.fillAlphas = 0.7;
    graphAix.stacked = false;
    graphAix.hideBulletsCount = 35;
    graphAix.bullet = "bubble";

    stockPanelLinux.addStockGraph(graphWindows);
    stockPanelLinux.addStockGraph(graphAix);
    stockPanelLinux.addStockGraph(graphLinux);


    chart.panels = [stockPanelLinux];
// OTHER SETTINGS (scrollBar & cursor)
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.updateOnReleaseOnly = false;
    chart.chartScrollbarSettings = scrollbarSettings;

    cursorSettings = new AmCharts.ChartCursorSettings();
    cursorSettings.valueBalloonsEnabled = true;
    chart.chartCursorSettings = cursorSettings;

// PERIOD SELECTOR //////////////////////////
    periodSelector = new AmCharts.PeriodSelector();
    periodSelector.periods = [{
			period : "DD",
			count : 10,
			label : "10 days"
		}, 
		{
	        period: "DD",
	        count: 15,
	        label: "2 Weeks"
	    },{
			period : "MM",
			count : 1,
			label : "1 month"
		},
		 {
	        period: "MM",
	        selected : true,
	        count: 3,
	        label: "3 Month"

	    }, {
	        period: "MM",
	        count: 6,
	        label: "6 Months"
	    }, {
			period : "YYYY",
			count : 1,
			label : "1 year"
		}, {
        period: "MAX",
        label: "MAX",
        selected: false
    }];
    chart.periodSelector = periodSelector;

// PANEL SETTING ////////////////////////////
    panelsSettings = new AmCharts.PanelsSettings();
    panelsSettings.usePrefixes = true;
    panelsSettings.panEventsEnabled = true;
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' ', decimalSeparator: '.'};
    panelsSettings.usePrefixes = false;

    chart.panelsSettings = panelsSettings;
    chart.balloon.bulletSize = 4;
    chart.addListener('dataUpdated', function (event){
        deleteAmChart();
    });
    chart.addListener('zoomed', function (event) {
        deleteAmChart();
    });
    chart.write('graphEquipement');
    deleteAmChart();
}

function createAlerts(tv_view) {
    "use strict";

    var chart, categoryAxesSettings, dataset, graphWarning, stockPanelAlert,
        stockLegendWarning, graphWarningAck, graphCritical, stockLegendAlert,
        stockLegendCritical, graphCriticalAck, scrollbarSettings,
        cursorSettings, periodSelector, panelsSettings, valueAxesSettings,
        stockPanelWarning, graphWarning, stockPanelWarning, stockLegendWarning,
        stockPanelWarning, graphWarningAck, stockPanelWarning,graphUnknown, graphTotalApps;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/optools/kpi/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// valueAxesSettings
    valueAxesSettings = new AmCharts.ValueAxesSettings();
    valueAxesSettings.stackType = "regular";
    chart.valueAxesSettings = valueAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "warning",
        toField: "warning"
    }, {
        fromField: "critical",
        toField: "critical"
    }, {
        fromField: "unknown",
        toField: "unknown"
    },
    {
        fromField: "total_alerts_ack",
        toField: "total_alerts_ack"
    }];
    dataset.dataProvider = chartDataAlerts;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

// PANELS ///////////////////////////////////

//  1) graph Linux

    graphCritical = new AmCharts.StockGraph();
    graphCritical.valueField = "critical";
    graphCritical.type = "line";
    graphCritical.title = "Critical";
    graphCritical.balloonText = "  [[critical]]";
    graphCritical.lineColor = "#FF3300";
    graphCritical.lineThickness = 2;
    graphCritical.fillColor = "#FF3300";
    graphCritical.useDataSetColors = false;
    graphCritical.periodValue = "Sum";
    graphCritical.fillAlphas = 0.9;
    graphCritical.stacked = false;
    graphCritical.hideBulletsCount = 35;
    graphCritical.bullet = "bubble";

//  1) stockPanel Alert
    stockPanelAlert = new AmCharts.StockPanel();
    stockPanelAlert.title = "Number Of Alerts";
    stockPanelAlert.percentHeight = 50;

//  1) stockLegend Alert
    stockLegendAlert = new AmCharts.StockLegend();
    // stockLegendAlert.valueTextRegular = "[[percents]]%";
    stockPanelAlert.stockLegend = stockLegendAlert;

//  2) graph Windows

    graphWarning = new AmCharts.StockGraph();
    graphWarning.valueField = "warning";
    graphWarning.type = "line";
    graphWarning.title = "Warning";
    graphWarning.balloonText = " [[warning]]";
    graphWarning.lineColor = "#FFA500";
    graphWarning.lineThickness = 2;
    graphWarning.fillColor = "#FFA500";
    graphWarning.useDataSetColors = false;
    graphWarning.periodValue = "Sum";
    graphWarning.fillAlphas = 0.9;
    graphWarning.stacked = false;
    graphWarning.hideBulletsCount = 35;
    graphWarning.bullet = "bubble";

//  3) graph Aix

    graphUnknown = new AmCharts.StockGraph();
    graphUnknown.valueField = "unknown";
    graphUnknown.type = "line";
    graphUnknown.title = "Unknown";
    graphUnknown.balloonText = " [[unknown]]";
    graphUnknown.lineColor = "#C555B9";
    graphUnknown.lineThickness = 2;
    graphUnknown.fillColor = "#C555B9";
    graphUnknown.useDataSetColors = false;
    graphUnknown.periodValue = "Sum";
    graphUnknown.fillAlphas = 0.9;
    graphUnknown.stacked = false;
    graphUnknown.hideBulletsCount = 35;
    graphUnknown.bullet = "bubble";
    
    graphTotalApps = new AmCharts.StockGraph();
    graphTotalApps.valueField = "total_alerts_ack";
    graphTotalApps.balloonText = "[[total_alerts_ack]]";
    graphTotalApps.type = "line";
    graphTotalApps.title = "Acknowledged";
    graphTotalApps.hideBulletsCount = 35;
    graphTotalApps.bullet = "bubble";
    graphTotalApps.lineThickness = 2;
    graphTotalApps.lineColor = "#17D117";
    graphTotalApps.useDataSetColors = false;
    graphTotalApps.stackable=false;
	
    stockPanelAlert.addStockGraph(graphCritical);
    stockPanelAlert.addStockGraph(graphWarning);
    stockPanelAlert.addStockGraph(graphUnknown);
    stockPanelAlert.addStockGraph(graphTotalApps);
    

    chart.panels = [stockPanelAlert];
// OTHER SETTINGS (scrollBar & cursor)
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.updateOnReleaseOnly = false;
    chart.chartScrollbarSettings = scrollbarSettings;

    cursorSettings = new AmCharts.ChartCursorSettings();
    cursorSettings.valueBalloonsEnabled = true;
    chart.chartCursorSettings = cursorSettings;

// PERIOD SELECTOR //////////////////////////
    periodSelector = new AmCharts.PeriodSelector();
    periodSelector.periods = [{
			period : "DD",
			count : 10,
			label : "10 days"
		}, 
		{
	        period: "DD",
	        count: 15,
	        label: "2 Weeks"
	    },{
			period : "MM",
			count : 1,
			label : "1 month"
		},
		 {
	        period: "MM",
	        selected : true,
	        count: 3,
	        label: "3 Month"

	    }, {
	        period: "MM",
	        count: 6,
	        label: "6 Months"
	    }, {
			period : "YYYY",
			count : 1,
			label : "1 year"
		}, {
        period: "MAX",
        label: "MAX",
        selected: false
    }];
    chart.periodSelector = periodSelector;

// PANEL SETTING ////////////////////////////
    panelsSettings = new AmCharts.PanelsSettings();
    panelsSettings.usePrefixes = true;
    panelsSettings.panEventsEnabled = true;
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' ', decimalSeparator: '.'};
    panelsSettings.usePrefixes = false;

    chart.panelsSettings = panelsSettings;
    chart.balloon.bulletSize = 4;
    chart.addListener('dataUpdated', function (event){
        deleteAmChart();
    });
    chart.addListener('zoomed', function (event) {
        deleteAmChart();
    });
    

    chart.write('graphAlerts');
    deleteAmChart();

}

function createRecurrentsAlerts() {
    "use strict";
    var chart, legend, host;

// CHART ///////////////////////////////////
    chart = new AmCharts.AmPieChart();
    chart.dataProvider = chartDataRecurrentsAlerts;
    chart.titleField = "name";
    chart.valueField = "repetitions";
    chart.descriptionField= "date_last_alert";
    chart.balloonText = "[[title]]: [[value]]/" + other + "<br> Last alert: [[description]]";
    chart.labelText = "[[title]]: [[value]]";
    chart.urlField = "url";
    chart.urlTarget = "_blank";
    chart.pullOutRadius = "0%";
    chart.radius = "30%";
    chart.outlineThickness = 1.2;
    chart.outlineAlpha = 1;
    chart.outlineColor = "#FFFFFF";
    chart.depth3D = 15;
    chart.angle = 30;
    chart.startDuration = 0;
    
    chart.write('graphRecurrentsAlerts');
    deleteAmChart();
}

function createRecurrentsAlertsWeek() {
    "use strict";
    var chart, legend, host;

// CHART ///////////////////////////////////
    chart = new AmCharts.AmPieChart();
    chart.dataProvider = chartDataRecurrentsAlertsWeek;
    chart.titleField = "name";
    chart.valueField = "repetitions";
    chart.descriptionField= "date_last_alert";
    chart.balloonText = "[[title]]: [[value]]/" + others_weeks + "<br> Last alert: [[description]]";
    chart.labelText = "[[title]]: [[value]]";
    chart.urlField = "url";
    chart.urlTarget = "_blank";
    chart.pullOutRadius = "0%";
    chart.radius = "30%";
    chart.outlineThickness = 1.2;
    chart.outlineAlpha = 1;
    chart.outlineColor = "#FFFFFF";
    chart.depth3D = 15;
    chart.angle = 30;
    chart.startDuration = 0;
    chart.write('graphRecurrentsAlertsWeek');
    deleteAmChart();
}

function createOldestsAlerts() {
    "use strict";
    var chart;

// CHART ///////////////////////////////////
    chart = new AmCharts.AmSerialChart();
    chart.dataProvider = chartDataOldestsAlerts;
    chart.categoryField = "name";
    chart.rotate = true;
    chart.depth3D = 20;
    chart.angle = 30;

    // AXES
    // category
    var categoryAxis = chart.categoryAxis;
    categoryAxis.gridAlpha = 0;
    

    // GRAPH            
    var graph = new AmCharts.AmGraph();
    graph.valueField = "days";
    graph.colorField = "color_graph";
    graph.type = "column";
    graph.descriptionField = "date_error";
    graph.balloonText = "[[category]]: [[value]] days ([[description]])";
    graph.lineAlpha = 0;
    graph.fillAlphas = 1;
    graph.urlField = "url";
    graph.urlTarget = "_blank";
    chart.addGraph(graph);

    // WRITE
    chart.write('graphOldestsAlerts');
    deleteAmChart();
}

function createFailedServices(tv_view){
	"use strict";
    var chart, categoryAxesSettings, dataset, graphWarning, graphCritical, graphUnknown, graphAcknowledged, graphAcknowledged, graphNotAcknowledged, stockPanelFailed,
        stockLegendFailed, 
        stockLegendServices, scrollbarSettings, cursorSettings, periodSelector,
        panelsSettings ;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/optools/kpi/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "nb_warning",
        toField: "nb_warning"
    }, {
        fromField: "nb_critical",
        toField: "nb_critical"
    },{
        fromField: "nb_unknown",
        toField: "nb_unknown"
    }, {
        fromField: "nb_acknowledged",
        toField: "nb_acknowledged"
    }, {
        fromField: "nb_not_acknowledged",
        toField: "nb_not_acknowledged"
    }, {
        fromField: "nb_host_down",
        toField: "nb_host_down"
    }];
    dataset.dataProvider = chartFailedServices;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

    // PANELS ///////////////////////////////////

//  1) graph nb_warning

    graphWarning = new AmCharts.StockGraph();
    graphWarning.valueField = "nb_warning";
    graphWarning.descriptionField = "nb_warning";
    // graphWarning.balloonText += "\n[[nb_warning]]";
    graphWarning.urlField = "url"; // Field containing the url to open if the user click on the graph
    graphWarning.urlTarget = "_blank"; // Open the url into a new tab
    graphWarning.type = "line";
    graphWarning.title = "Warning";
    graphWarning.hideBulletsCount = 35;
    graphWarning.bullet = "bubble";
    graphWarning.lineThickness = 2;
    graphWarning.lineColor = "#FFA500";
    graphWarning.useDataSetColors = false;
    graphWarning.periodValue = "Average";
    
//  2) graph nb_critical

    graphCritical = new AmCharts.StockGraph();
    graphCritical.valueField = "nb_critical";
    graphCritical.descriptionField = "nb_critical";
    // graphCritical.balloonText += "\n[[nb_critical]]";
    graphCritical.urlField = "url"; // Field containing the url to open if the user click on the graph
    graphCritical.urlTarget = "_blank"; // Open the url into a new tab
    graphCritical.type = "line";
    graphCritical.title = "Critical";
    graphCritical.hideBulletsCount = 35;
    graphCritical.bullet = "bubble";
    graphCritical.lineThickness = 2;
    graphCritical.lineColor = "#FF3300";
    graphCritical.useDataSetColors = false;
    graphCritical.periodValue = "Average";
    
//  3) graph nb_unknown

	graphUnknown = new AmCharts.StockGraph();
    graphUnknown.valueField = "nb_unknown";
    graphUnknown.descriptionField = "nb_unknown";
  //  graphUnknown.balloonText += "\n[[nb_unknown]]";
    graphUnknown.urlField = "url"; // Field containing the url to open if the user click on the graph
    graphUnknown.urlTarget = "_blank"; // Open the url into a new tab
    graphUnknown.type = "line";
    graphUnknown.title = "Unknown";
    graphUnknown.hideBulletsCount = 35;
    graphUnknown.bullet = "bubble";
    graphUnknown.lineThickness = 2;
    graphUnknown.lineColor = "#C555B9";
    graphUnknown.useDataSetColors = false;
    graphUnknown.periodValue = "Average";
    
//  4) graph nb_acknowledged

    graphAcknowledged = new AmCharts.StockGraph();
    graphAcknowledged.valueField = "nb_acknowledged";
    graphAcknowledged.descriptionField = "nb_acknowledged";
   //  graphAcknowledged.balloonText += "\n[[nb_acknowledged]]";
    graphAcknowledged.urlField = "url"; // Field containing the url to open if the user click on the graph
    graphAcknowledged.urlTarget = "_blank"; // Open the url into a new tab
    graphAcknowledged.type = "line";
    graphAcknowledged.title = "Acknowledged";
    graphAcknowledged.hideBulletsCount = 35;
    graphAcknowledged.bullet = "bubble";
    graphAcknowledged.lineThickness = 2;
    graphAcknowledged.lineColor = "#17D117";
    graphAcknowledged.useDataSetColors = false;
    graphAcknowledged.periodValue = "Average";
    
//  5) graph nb_not_acknowledged

    graphNotAcknowledged = new AmCharts.StockGraph();
    graphNotAcknowledged.valueField = "nb_not_acknowledged";
    graphNotAcknowledged.descriptionField = "nb_not_acknowledged";
 //   graphNotAcknowledged.balloonText += "\n[[nb_not_acknowledged]]";
    graphNotAcknowledged.urlField = "url"; // Field containing the url to open if the user click on the graph
    graphNotAcknowledged.urlTarget = "_blank"; // Open the url into a new tab
    graphNotAcknowledged.type = "line";
    graphNotAcknowledged.title = "Not Acknowledged";
    graphNotAcknowledged.hideBulletsCount = 35;
    graphNotAcknowledged.bullet = "bubble";
    graphNotAcknowledged.lineThickness = 2;
    graphNotAcknowledged.lineColor = "#6EC2FD";
    graphNotAcknowledged.useDataSetColors = false;
    graphNotAcknowledged.periodValue = "Average";
    

//  1) stockPanel Hosts
    stockPanelFailed = new AmCharts.StockPanel();
    stockPanelFailed.title = "Failed Services";
    stockPanelFailed.percentHeight = 50;
    stockPanelFailed.addStockGraph(graphWarning);
    stockPanelFailed.addStockGraph(graphCritical);
    stockPanelFailed.addStockGraph(graphUnknown);
    stockPanelFailed.addStockGraph(graphAcknowledged);
    stockPanelFailed.addStockGraph(graphNotAcknowledged);
    stockPanelFailed.showCategoryAxis = true;

//  1) stockLegend Hosts
    stockLegendFailed = new AmCharts.StockLegend();
    stockPanelFailed.stockLegend = stockLegendFailed;
	
	
	chart.panels = [stockPanelFailed];
// OTHER SETTINGS (scrollBar & cursor)
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.graph = graphWarning;
    scrollbarSettings.updateOnReleaseOnly = false;
    chart.chartScrollbarSettings = scrollbarSettings;

    cursorSettings = new AmCharts.ChartCursorSettings();
    cursorSettings.valueBalloonsEnabled = true;
    chart.chartCursorSettings = cursorSettings;

// PERIOD SELECTOR //////////////////////////
    periodSelector = new AmCharts.PeriodSelector();
    periodSelector.periods = [{
			period : "DD",
			count : 10,
			label : "10 days"
		}, 
		{
	        period: "DD",
	        count: 15,
	        label: "2 Weeks"
	    },{
			period : "MM",
			count : 1,
			selected : true,
			label : "1 month"
		},
		 {
	        period: "MM",
	        count: 3,
	        label: "3 Month"

	    }, {
	        period: "MM",
	        count: 6,
	        label: "6 Months"
	    }, {
			period : "YYYY",
			count : 1,
			label : "1 year"
		}, {
        period: "MAX",
        label: "MAX",
        selected: false
    }];
    chart.periodSelector = periodSelector;

// PANEL SETTING ////////////////////////////
    panelsSettings = new AmCharts.PanelsSettings();
    panelsSettings.usePrefixes = true;
    panelsSettings.panEventsEnabled = true;
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' ', decimalSeparator: '.'};
    panelsSettings.usePrefixes = false;

    chart.panelsSettings = panelsSettings;
    chart.balloon.bulletSize = 4;
    chart.addListener('dataUpdated', function (event){
        deleteAmChart();
    });
    chart.addListener('zoomed', function (event) {
        deleteAmChart();
    });
    chart.write('graphFailed');
    deleteAmChart();
}

function createCountFailedServices(tv_view){
	"use strict";
    var chart, categoryAxesSettings, dataset, graph_nb_failed_day, graph_nb_failed_week, graph_nb_failed_month, graph_nb_failed_some_month, graphAcknowledged, graphNotAcknowledged, stockPanelFailed,
        stockLegendFailed, 
        stockLegendServices, scrollbarSettings, cursorSettings, periodSelector,
        panelsSettings ;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/optools/kpi/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "nb_failed_day",
        toField: "nb_failed_day"
    }, {
        fromField: "nb_failed_week",
        toField: "nb_failed_week"
    },{
        fromField: "nb_failed_month",
        toField: "nb_failed_month"
    }, {
        fromField: "nb_failed_some_month",
        toField: "nb_failed_some_month"
    }];
    dataset.dataProvider = chartCountFailedServices;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

    // PANELS ///////////////////////////////////

//  1) graph nb_failed_day

    graph_nb_failed_day = new AmCharts.StockGraph();
    graph_nb_failed_day.valueField = "nb_failed_day";
    graph_nb_failed_day.descriptionField = "nb_failed_day";
    // graph_nb_failed_day.balloonText += "\n[[nb_warning]]";
    graph_nb_failed_day.type = "line";
    graph_nb_failed_day.title = "Failed Services (0-1 day)";
    graph_nb_failed_day.hideBulletsCount = 35;
    graph_nb_failed_day.bullet = "bubble";
    graph_nb_failed_day.lineThickness = 2;
    graph_nb_failed_day.lineColor = "#6EC2FD";
    graph_nb_failed_day.useDataSetColors = false;
    graph_nb_failed_day.periodValue = "Average";
    
//  2) graph nb_failed_week

    graph_nb_failed_week = new AmCharts.StockGraph();
    graph_nb_failed_week.valueField = "nb_failed_week";
    graph_nb_failed_week.descriptionField = "nb_failed_week";
    // graph_nb_failed_week.balloonText += "\n[[nb_critical]]";
    graph_nb_failed_week.type = "line";
    graph_nb_failed_week.title = "Failed Services (1-5 days)";
    graph_nb_failed_week.hideBulletsCount = 35;
    graph_nb_failed_week.bullet = "bubble";
    graph_nb_failed_week.lineThickness = 2;
    graph_nb_failed_week.lineColor = "#C555B9";
    graph_nb_failed_week.useDataSetColors = false;
    graph_nb_failed_week.periodValue = "Average";
    
//  3) graph_nb_failed_month

	graph_nb_failed_month = new AmCharts.StockGraph();
    graph_nb_failed_month.valueField = "nb_failed_month";
    graph_nb_failed_month.descriptionField = "nb_failed_month";
  //  graph_nb_failed_month.balloonText += "\n[[nb_unknown]]";
    graph_nb_failed_month.type = "line";
    graph_nb_failed_month.title = "Failed Services (5-50 days)";
    graph_nb_failed_month.hideBulletsCount = 35;
    graph_nb_failed_month.bullet = "bubble";
    graph_nb_failed_month.lineThickness = 2;
    graph_nb_failed_month.lineColor = "#FFA500";
    graph_nb_failed_month.useDataSetColors = false;
    graph_nb_failed_month.periodValue = "Average";
    
//  4) graph_nb_failed_some_month

    graph_nb_failed_some_month = new AmCharts.StockGraph();
    graph_nb_failed_some_month.valueField = "nb_failed_some_month";
    graph_nb_failed_some_month.descriptionField = "nb_failed_some_month";
   //  graph_nb_failed_some_month.balloonText += "\n[[nb_acknowledged]]";
    graph_nb_failed_some_month.type = "line";
    graph_nb_failed_some_month.title = "Failed Services (> 50 days)";
    graph_nb_failed_some_month.hideBulletsCount = 35;
    graph_nb_failed_some_month.bullet = "bubble";
    graph_nb_failed_some_month.lineThickness = 2;
    graph_nb_failed_some_month.lineColor = "#FF3300";
    graph_nb_failed_some_month.useDataSetColors = false;
    graph_nb_failed_some_month.periodValue = "Average";
    

    

//  1) stockPanel Hosts
    stockPanelFailed = new AmCharts.StockPanel();
    stockPanelFailed.title = "Count Failed Services";
    stockPanelFailed.percentHeight = 50;
    stockPanelFailed.addStockGraph(graph_nb_failed_day);
    stockPanelFailed.addStockGraph(graph_nb_failed_week);
    stockPanelFailed.addStockGraph(graph_nb_failed_month);
    stockPanelFailed.addStockGraph(graph_nb_failed_some_month);
    stockPanelFailed.showCategoryAxis = true;

//  1) stockLegend Hosts
    stockLegendFailed = new AmCharts.StockLegend();
    stockPanelFailed.stockLegend = stockLegendFailed;
	
	
	chart.panels = [stockPanelFailed];
// OTHER SETTINGS (scrollBar & cursor)
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.graph = graph_nb_failed_day;
    scrollbarSettings.updateOnReleaseOnly = false;
    chart.chartScrollbarSettings = scrollbarSettings;

    cursorSettings = new AmCharts.ChartCursorSettings();
    cursorSettings.valueBalloonsEnabled = true;
    chart.chartCursorSettings = cursorSettings;

// PERIOD SELECTOR //////////////////////////
    periodSelector = new AmCharts.PeriodSelector();
    periodSelector.periods = [{
			period : "DD",
			count : 10,
			label : "10 days"
		}, 
		{
	        period: "DD",
	        count: 15,
	        label: "2 Weeks"
	    },{
			period : "MM",
			selected : true,
			count : 1,
			label : "1 month"
		},
		 {
	        period: "MM",
	        count: 3,
	        label: "3 Month"

	    }, {
	        period: "MM",
	        count: 6,
	        label: "6 Months"
	    }, {
			period : "YYYY",
			count : 1,
			label : "1 year"
		}, {
        period: "MAX",
        label: "MAX",
        selected: false
    }];
    chart.periodSelector = periodSelector;

// PANEL SETTING ////////////////////////////
    panelsSettings = new AmCharts.PanelsSettings();
    panelsSettings.usePrefixes = true;
    panelsSettings.panEventsEnabled = true;
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' ', decimalSeparator: '.'};
    panelsSettings.usePrefixes = false;

    chart.panelsSettings = panelsSettings;
    chart.balloon.bulletSize = 4;
    chart.addListener('dataUpdated', function (event){
        deleteAmChart();
    });
    chart.addListener('zoomed', function (event) {
        deleteAmChart();
    });
    chart.write('graphCountFailed');
    deleteAmChart();	
}

function createOldAlertVsHostDown(tv_view){
		"use strict";
    var chart, categoryAxesSettings, dataset, graph_nb_host_down, graph_nb_oldest_alert, graph_nb_failed_month, graph_nb_failed_some_month, graphAcknowledged, graphNotAcknowledged, stockPanelFailed,
        stockLegendFailed, 
        stockLegendServices, scrollbarSettings, cursorSettings, periodSelector,
        panelsSettings ;

// CHART ////////////////////////////////////
    chart = new AmCharts.AmStockChart();
    chart.pathToImages = "/static/optools/kpi/js/images/";

// categoryAxesSettings
    categoryAxesSettings = new AmCharts.CategoryAxesSettings();
    categoryAxesSettings.minPeriod = "DD";
    chart.categoryAxesSettings = categoryAxesSettings;

// DATASET //////////////////////////////////
    dataset = new AmCharts.DataSet();
    dataset.fieldMappings = [{
        fromField: "nb_host_down",
        toField: "nb_host_down"
    }, {
        fromField: "nb_oldest_alert",
        toField: "nb_oldest_alert"
    }];
    dataset.dataProvider = chartCountOldAlertVsHostDown;
    dataset.categoryField = "date";

    chart.dataSets = [dataset];

    // PANELS ///////////////////////////////////

//  1) graph nb_host_down

    graph_nb_host_down = new AmCharts.StockGraph();
    graph_nb_host_down.valueField = "nb_host_down";
    graph_nb_host_down.descriptionField = "nb_host_down";
    // graph_nb_host_down.balloonText += "\n[[nb_warning]]";
    graph_nb_host_down.type = "line";
    graph_nb_host_down.title = "Hosts Down";
    graph_nb_host_down.hideBulletsCount = 35;
    graph_nb_host_down.bullet = "bubble";
    graph_nb_host_down.lineThickness = 2;
    graph_nb_host_down.lineColor = "#6EC2FD";
    graph_nb_host_down.useDataSetColors = false;
    graph_nb_host_down.periodValue = "Average";
    
//  2) graph nb_oldest_alert

    graph_nb_oldest_alert = new AmCharts.StockGraph();
    graph_nb_oldest_alert.valueField = "nb_oldest_alert";
    graph_nb_oldest_alert.descriptionField = "nb_oldest_alert";
    // graph_nb_oldest_alert.balloonText += "\n[[nb_critical]]";
    graph_nb_oldest_alert.type = "line";
    graph_nb_oldest_alert.title = "Oldest Alerts";
    graph_nb_oldest_alert.hideBulletsCount = 35;
    graph_nb_oldest_alert.bullet = "bubble";
    graph_nb_oldest_alert.lineThickness = 2;
    graph_nb_oldest_alert.lineColor = "#C555B9";
    graph_nb_oldest_alert.useDataSetColors = false;
    graph_nb_oldest_alert.periodValue = "Average";
    

//  1) stockPanel Hosts
    stockPanelFailed = new AmCharts.StockPanel();
    stockPanelFailed.title = "Oldest Alerts vs Hosts Down";
    stockPanelFailed.percentHeight = 50;
    stockPanelFailed.addStockGraph(graph_nb_host_down);
    stockPanelFailed.addStockGraph(graph_nb_oldest_alert);
    stockPanelFailed.showCategoryAxis = true;

//  1) stockLegend Hosts
    stockLegendFailed = new AmCharts.StockLegend();
    stockPanelFailed.stockLegend = stockLegendFailed;
	
	
	chart.panels = [stockPanelFailed];
// OTHER SETTINGS (scrollBar & cursor)
    scrollbarSettings = new AmCharts.ChartScrollbarSettings();
    scrollbarSettings.graph = graph_nb_host_down;
    scrollbarSettings.updateOnReleaseOnly = false;
    chart.chartScrollbarSettings = scrollbarSettings;

    cursorSettings = new AmCharts.ChartCursorSettings();
    cursorSettings.valueBalloonsEnabled = true;
    chart.chartCursorSettings = cursorSettings;

// PERIOD SELECTOR //////////////////////////
    periodSelector = new AmCharts.PeriodSelector();
    periodSelector.periods = [{
			period : "DD",
			count : 10,
			label : "10 days"
		}, 
		{
	        period: "DD",
	        count: 15,
	        label: "2 Weeks"
	    },{
			period : "MM",
			selected : true,
			count : 1,
			label : "1 month"
		},
		 {
	        period: "MM",
	        count: 3,
	        label: "3 Month"

	    }, {
	        period: "MM",
	        count: 6,
	        label: "6 Months"
	    }, {
			period : "YYYY",
			count : 1,
			label : "1 year"
		}, {
        period: "MAX",
        label: "MAX",
        selected: false
    }];
    chart.periodSelector = periodSelector;

// PANEL SETTING ////////////////////////////
    panelsSettings = new AmCharts.PanelsSettings();
    panelsSettings.usePrefixes = true;
    panelsSettings.panEventsEnabled = true;
    panelsSettings.numberFormatter = {precision: 0, thousandsSeparator: ' ', decimalSeparator: '.'};
    panelsSettings.usePrefixes = false;

    chart.panelsSettings = panelsSettings;
    chart.balloon.bulletSize = 4;
    chart.addListener('dataUpdated', function (event){
        deleteAmChart();
    });
    chart.addListener('zoomed', function (event) {
        deleteAmChart();
    });
    chart.write('graphOldAlertVsHostDown');
    deleteAmChart();	
}









function deleteAmChart() {
    "use strict";
    var node, tspan, i, bad;
    tspan = document.getElementsByTagName("tspan");
    for (i = 0; i < tspan.length; i += 1) {
        if (tspan[i].textContent === "chart by amcharts.com") {
            bad = tspan[i].parentNode.parentNode;
            bad.removeChild(bad.childNodes[0]);
            bad.removeChild(bad.childNodes[0]);
        }

    }
}
