$(document).ready(function(){

  function manageAttackTypeShow(){
    var atkTypeCtn=$("#attack-type-ctn");
    var i=0;
    for(i=0; i<attackInfoA.length; ++i){
      var tmpData=attackInfoA[i];

      var tmpStr='' +
        '<div class="box" data-id="'+i+'">' +
          '<img src="'+tmpData.png+'" class="color">' +
          '<div class="clr-show" style="background:'+tmpData.color+';"></div>'+
          '<div class="text">' +
            tmpData.name +
          '</div>' +
        '</div>';
      var tmpBox=$(tmpStr);
      atkTypeCtn.append(tmpBox);
    }
  }
  manageAttackTypeShow();

  function getCurStrTime() {
    var now = new Date();

    var year = now.getFullYear();       //年
    var month = now.getMonth() + 1;     //月
    var day = now.getDate();            //日

    var hh = now.getHours();            //时
    var mm = now.getMinutes();          //分
    var ss = now.getSeconds();            //秒

    var clock = year + "-";

    if (month < 10) clock += "0";
    clock += month + "-";

    if (day < 10) clock += "0";
    clock += day + " ";

    if (hh < 10) clock += "0";
    clock += hh + ":";

    if (mm < 10) clock += '0';
    clock += mm + ":";

    if (ss < 10) clock += '0';
    clock += ss;

    return (clock);
  }

  var showInfo = ShowInfo.createNew({
    'type': 'country',
    'ctn': '#top-info-ctn',
    'trig': '#top-info-min',
    'change': '#top-info-change',
    'title': "#top-info-title"
  });

  var myPlanet=initPlanet({
    'showInfo': showInfo
  });
  d3.select("#stopRotate").on("click", function(){
    myPlanet.stopRotate();
  });
  d3.select("#startRotate").on("click", function(){
    myPlanet.startRotate();
  });
  d3.select("#submitInfo").on("click", function(){
    var srcLat=parseInt($("#srcLat").val());
    var srcLng=parseInt($("#srcLng").val());
    var dstLat=parseInt($("#dstLat").val());
    var dstLng=parseInt($("#dstLng").val());
    var durTime=1900;
    /*
     * inObj{
     *   srcP: {lat, lng},
     *   dstP; {lat, lng},
     *   color,
     *   ttl: {circle, line}
     *   type,
     *   angle,
     * }
     * */
    myPlanet.attack({
      src:{
        lat: srcLat,
        lng: srcLng
      },
      dst:{
        lat: dstLat,
        lng: dstLng
      },
      color: "#ff1133",
      circle:{
        ttl: 800,
        lineWidth: 2
      },
      line:{
        ttl: 1600,
        lineWidth: 2
      }

    });
  });
  d3.select("#fixLine").on("click", function(){
    var srcLat=parseInt($("#srcLat").val());
    var srcLng=parseInt($("#srcLng").val());
    var dstLat=parseInt($("#dstLat").val());
    var dstLng=parseInt($("#dstLng").val());

    myPlanet.fixLine({
      // Here we use the `angles` and `colors` scales we built earlier
      // to convert magnitudes to appropriate angles and colors.
      color: "red",
      ttl:  10000,
      lat0: srcLat,
      lng0: srcLng,
      lat1: dstLat,
      lng1: dstLng
    });
  });
  d3.select("#graticuleTrigger").on("click", function(){
    if(d3.select(this).attr("data-need")=="1") {
      myPlanet.hideGraticule();
      d3.select(this).attr("data-need", "0");
    }
    else{
      myPlanet.showGraticule();
      d3.select(this).attr("data-need", "1");
    }
  });

  d3.select("#addDot").on("click", function(){

    myPlanet.addDot({
      // Here we use the `angles` and `colors` scales we built earlier
      // to convert magnitudes to appropriate angles and colors.
      color: "red",
      alpha: 0.5,
      angle: 0.4,
      ttl:   myPlanet.ttls(100),
      lat: 40,
      lng: 116,
    });
  });

  controlsFunc();
  //simulationAttack(myPlanet);
//----------------------------------------------
  var deal_ws=DealWS.createNew({
    planet: myPlanet
  });

  $("#addDot").click(function(){
    console.log("add dot");

    var atkCtn=AtkCtn.createNew({
      ctn: "#atk-ctn"
    });
    atkCtn.addLine({
      time: "2011-2-21 10:10:10",
      type: "ARP attack"+num,
      src: "222.222.222.222:65536 shijiazhuang",
      dst: "222.222.222.222:65536 shijiazhuang",
      atkType: num
    });
    num+=1;
  });

  var showCmdP=ShowCmdP.createNew({
    'ctn': '#left-cmd-panel',
    'trig': '#left-cmd-trig',
    'graticule': '#trig-graticule',
    'rotate': '#trig-rotate',
    'planet': myPlanet,
  });

  var atkType=AtkType.createNew({
    'ctn': '#attack-type-ctn',
    'showInfo': showInfo
  });

  var atkCtn = AtkCtn.createNew({
    ctn: "#atk-ctn"
  });

  function attackFunc(data) {

    for (var i = 0; i < data.length; ++i) {
      var tmpData=data[i];

      setTimeout(function () {

        atkCtn.addLine({
          time: tmpData.time,
          infos: tmpData.infos,
          //src: tmpData.src.name + "(" + tmpData.src.lng + "," + tmpData.src.lat + ") " + tmpData.src.ip + ":" + tmpData.src.port + " ",
          src: tmpData.src.ip + ":" + tmpData.src.port + " ",
          //dst: tmpData.dst.name + "(" + tmpData.dst.lng + "," + tmpData.dst.lat + ") " + tmpData.dst.ip + ":" + tmpData.dst.port + " ",
          dst: tmpData.dst.ip + ":" + tmpData.dst.port + " ",
          atkId: tmpData.attackId,
          sensorId: tmpData.sensorId,
          protocalA: tmpData.protocalA,
          protocalB: tmpData.protocalB,
          trails: tmpData.trails,
          references: tmpData.references

        });

        myPlanet.attack({
          dotLine: 1,
          src: {
            lat: parseFloat(tmpData.src.lat),
            lng: parseFloat(tmpData.src.lng)
          },
          dst: {
            lat: parseFloat(tmpData.dst.lat),
            lng: parseFloat(tmpData.dst.lng)
          },
          color: attackInfoA[tmpData.attackId].color,
          circle: {
            ttl: 800,
            lineWidth: 3
          },
          line: {
            ttl: 1600,
            lineWidth: 2
          }
        });
      }, parseInt(Math.random()*2000));

      //console.log("num:" + num);
      //atkCtn.addLine({
      //    time: tmpData.time,
      //    infos: tmpData.infos,
      //    //src: tmpData.src.name+"("+tmpData.src.lng+","+tmpData.src.lat+") "+tmpData.src.ip+":"+tmpData.src.port+" ",
      //    src: tmpData.src.ip+':'+tmpData.src.port,
      //    //dst: tmpData.dst.name+"("+tmpData.dst.lng+","+tmpData.dst.lat+") "+tmpData.dst.ip+":"+tmpData.dst.port+" ",
      //    dst: tmpData.dst.ip+':'+tmpData.dst.port,
      //    atkId: tmpData.attackId,
      //    sensorId: tmpData.sensorId,
      //    protocalA: tmpData.protocalA,
      //    protocalB: tmpData.protocalB,
      //    trails: tmpData.trails,
      //    references: tmpData.references
      //
      //});
      //
      //myPlanet.attack({
      //    src: {
      //        lat: parseFloat(tmpData.src.lat),
      //        lng: parseFloat(tmpData.src.lng)
      //    },
      //    dst: {
      //        lat: parseFloat(tmpData.dst.lat),
      //        lng: parseFloat(tmpData.dst.lng)
      //    },
      //    color: attackInfoA[tmpData.attackId].color,
      //    circle: {
      //        ttl: 800,
      //        lineWidth: 2
      //    },
      //    line: {
      //        ttl: 1600,
      //        lineWidth: 2
      //    }
      //
      //});
      //sleep(100);
    }

  };

  deal_ws.localws.add({
    'evt': 'attack array',
    'hdler': function(data){
      attackFunc(data);
    }
  });


});
