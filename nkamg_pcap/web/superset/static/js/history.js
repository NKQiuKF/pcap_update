queue()
  .defer(d3.json,'/tmp/history')
  .await(makeTables);

var volume_chart = dc.barChart('#monthly-volume-chart');
//var volume_chart = dc.barChart('#monthly-volume-chart')
var table_chart = dc.dataTable('.dc-data-table');

var ndx;

function makeTables(error, recordsJson){
  var records = recordsJson;
  //format the data
  var dateFormat = d3.time.format('%Y-%m-%d %H:%M:%S');
  
  records.forEach(function(d) { 
    d['date']=dateFormat.parse(d['timestamp']);
  });

  console.log(records);
  
  //create crossfilter dimensions and groups
  ndx = crossfilter(records);
  
  var date_dim = ndx.dimension(function(d){  console.log(d['date']); return d['date']; });

  console.log(date_dim);
  var move_day = ndx.dimension(function(d){ return d['date'].getDate();});
  console.log(move_day);

  var date_records = date_dim.group();

  var min_date = date_dim.bottom(1)[0]['date'];
  var max_date = date_dim.top(1)[0]['date'];

  
  volume_chart
    .width(990)
    .height(200)
    .transitionDuration(1000)
    .margins({top:30, right:50, bottom:25, left:40})
    .dimension(date_dim)
    .x(d3.time.scale().domain([new Date(2016, 09, 1),max_date]))
    .group(date_records);

  table_chart
    .dimension(move_day)
    .group(function(d){
      var format = d3.format('02d');
      return d['date'].getFullYear()+'-'+format(d['date'].getMonth()+1)+'-'+format(d['date'].getDate());
    })
    .size(Infinity)
    .columns([
      {
        label:'日期',
        format:function(d){return d['timestamp'];}
      },
      {
        label:'攻击类型',
        format:function(d){return d['atk_type'];}
      },
      {
        label:'传感器',
        format:function(d){return d['sensor_number'];}
      },
      {
        label:'源IP',
        format:function(d){return d['src_ip'];}
      },
      {
        label:'目的IP',
        format:function(d){return d['dst_ip'];}
      },
      {
        label:'协议',
        format:function(d){return d['protocol'];}
      },
      {
        label:'威胁信息',
        format:function(d){return d['info'];}
      },
      {
        label:'信息来源',
        format:function(d){return d['reference'];}
      }
    ])
    .sortBy(function(d){
      return d['date'];
    })
    .order(d3.ascending);
  update();
  dc.renderAll();
  d3.select('#download')
    .on('click', function() {
        console.log(date_dim);
        var data = date_dim.top(Infinity);
        console.log(data);
        data.forEach(function(d) {
          console.log(d)
          delete d.date
      //    if(d['date']){data.pop()};
        });

        console.log(data);
        var blob = new Blob([d3.csv.format(data)], {type: "text/csv;charset=utf-8"});
        saveAs(blob, 'data.csv');
    });
};


var ofs = 0, pag = 10;
function display() {
    d3.select('#last')
        .attr('disabled', ofs-pag<0 ? 'true' : null);
    d3.select('#next')
        .attr('disabled', ofs+pag>=ndx.size() ? 'true' : null);
}
function update() {
    table_chart.beginSlice(ofs);
    table_chart.endSlice(ofs+pag);
    display();
}
function next() {
    ofs += pag;
    update();
    table_chart.redraw();
}
function last() {
    ofs -= pag;
    update();
    table_chart.redraw();
};
