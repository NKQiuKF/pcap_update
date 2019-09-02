queue()
  .defer(d3.json, "/heatmap")
  .await(makeGraphs);

function makeGraphs(error, recordsJson) {
	
  //Clean data
  var records = recordsJson;
  var dateFormat = d3.time.format("%Y-%m-%d %H:%M:%S");
  
  records.forEach(function(d) {
  	d["timestamp"] = dateFormat.parse(d["timestamp"]);
  	d["timestamp"].setMinutes(0);
  	d["timestamp"].setSeconds(0);
  	d["src_longitude"] = +d["src_longitude"];
  	d["src_latitude"] = +d["src_latitude"];
        d["dst_longitude"] = +d["dst_longitude"];
        d["dst_latitude"] = +d["dst_latitude"];

  });
  
  //Create a Crossfilter instance
  var ndx = crossfilter(records);
  
  //Define Dimensions
  var dateDim = ndx.dimension(function(d) { return d["timestamp"]; });
  var ipDim = ndx.dimension(function(d) { return d["gender"]; });
  var atk_typeDim = ndx.dimension(function(d) { return d["atk_type"]; });
  var infoSrcDim = ndx.dimension(function(d) { return d["top_10_trail"]; });
  var SrclocationdDim = ndx.dimension(function(d) { return d["src_location"]; });
  var DstlocationdDim = ndx.dimension(function(d) { return d["dst_location"]; });

  var allDim = ndx.dimension(function(d) {return d;});
  
  //Group Data
  var numRecordsByDate = dateDim.group();
  var ipGroup = ipDim.group();
  var atk_typeGroup = atk_typeDim.group();
  var infoSrcGroup = infoSrcDim.group();
  var SrclocationGroup = SrclocationdDim.group();
  var DstlocationGroup = DstlocationdDim.group();

  var all = ndx.groupAll();
  
  //Define values (to be used in charts)
  var minDate = dateDim.bottom(1)[0]["timestamp"];
  var maxDate = dateDim.top(1)[0]["timestamp"];

  //Charts
  var numberRecordsND = dc.numberDisplay("#number-records-nd");
  var timeChart = dc.barChart("#time-chart");
  var ipChart = dc.pieChart("#gender-row-chart");
  var atk_typeChart = dc.pieChart("#age-segment-row-chart");
  var infoSrcChart = dc.pieChart("#phone-brand-row-chart");
  var srclocationChart = dc.rowChart("#srclocation-row-chart");
  var dstlocationChart = dc.rowChart("#dstlocation-row-chart");

  
  numberRecordsND
    .formatNumber(d3.format("d"))
    .valueAccessor(function(d){return d; })
    .group(all);
  
  
  timeChart
    .width(650)
    .height(140)
    .margins({top: 10, right: 50, bottom: 20, left: 20})
    .dimension(dateDim)
    .group(numRecordsByDate)
    .transitionDuration(500)
    .x(d3.time.scale().domain([minDate, maxDate]))
    .elasticY(true)
    .yAxis().ticks(4);
  
  ipChart
    .width(250)
    .height(250)
    .slicesCap(4)
    .innerRadius(100)
    .dimension(ipDim)
    .group(ipGroup)
    .legend(dc.legend())

  atk_typeChart
    .width(250)
    .height(250)
    .slicesCap(4)
    .innerRadius(100)
    .dimension(atk_typeDim)
    .group(atk_typeGroup)
    .legend(dc.legend())

  infoSrcChart
    .width(250)
    .height(250)
    .slicesCap(4)
    .innerRadius(100)
    .dimension(infoSrcDim)
    .group(infoSrcGroup)
    .legend(dc.legend())

  srclocationChart
    .width(200)
    .height(510)
    .dimension(SrclocationdDim)
    .group(SrclocationGroup)
    .ordering(function(d) { return -d.value })
    .colors(['#6baed6'])
    .elasticX(true)
    .labelOffsetY(10)
    .xAxis().ticks(4);
  dstlocationChart
    .width(200)
    .height(510)
    .dimension(DstlocationdDim)
    .group(DstlocationGroup)
    .ordering(function(d) { return -d.value })
    .colors(['#6baed6'])
    .elasticX(true)
    .labelOffsetY(10)
    .xAxis().ticks(4);


    var map = L.map('map');

    var drawMap = function(){
    
      map.setView([31.75, 110], 4);
      mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
      L.tileLayer(
      	'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    	attribution: '&copy; ' + mapLink + ' Contributors',
      	maxZoom: 15,
      	}).addTo(map);
      
      //HeatMap
      var geoData = [];
      _.each(allDim.top(Infinity), function (d) {
      	geoData.push([d["src_latitude"], d["src_longitude"], 1]);
      });
      var heat = L.heatLayer(geoData,{
      	radius: 10,
      	blur: 20, 
      	maxZoom: 1,
      }).addTo(map);
    
    };
    
    //Draw Map
    drawMap();
    
    //Update the heatmap if any dc chart get filtered
    dcCharts = [timeChart, ipChart, atk_typeChart, infoSrcChart, srclocationChart, dstlocationChart];
    
    _.each(dcCharts, function (dcChart) {
     dcChart.on("filtered", function (chart, filter) {
       map.eachLayer(function (layer) {
       map.removeLayer(layer)
       }); 
     drawMap();
     });
    });

dc.renderAll();

};
