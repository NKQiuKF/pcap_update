function controlsFunc(){
  $("#leftCtlMin").click(function(){
    var minJq=$("#leftCtlMin");
    var mainJq=$("#leftCtl");
    var minRight=parseInt(minJq.css("right"));
    var minWidth=parseFloat(minJq.css("width"));
    var mainWidth=parseFloat(mainJq.css("width"));
    var changeNum=mainWidth-2*minRight-minWidth;
    if(mainJq.attr("data-trig")=="1")
    {
      mainJq.animate({"left": -1*changeNum+"px"}, 200);
      mainJq.attr("data-trig", "0");
    }
    else{
      mainJq.animate({"left": "0"}, 200);
      mainJq.attr("data-trig", "1");
    }
  });

  $("#panelMin").click(function(){
    var panelMinJq=$("#panelMin");
    var panelJq=$("#panel");
    var btnTop=parseInt(panelMinJq.css("top"));
    var btnHeight=parseFloat(panelMinJq.css("height"));
    var panelHeight=parseFloat(panelJq.css("height"));
    var changeNum=panelHeight-2*btnTop-btnHeight;
    if(panelJq.attr("data-trig")=="1")
    {
      panelJq.animate({"bottom": -1*changeNum+"px"}, 200);
      panelJq.attr("data-trig", "0");
    }
    else{
      panelJq.animate({"bottom": "0"}, 200);
      panelJq.attr("data-trig", "1");
    }
  });
}

function initPlanet (inArg){
  var retObj={};
  var canvas = document.getElementById('mapCanvas');
  //console.log($("#mapCanvas").attr("width"));
  // Create our Planetary.js planet and set some initial values;
  // we use several custom plugins, defined at the bottom of the file
  var planet = planetaryjs.planet();
  retObj.planet=planet;

  planet.loadPlugin(autocenter({extraHeight: -120}));
  //planet.loadPlugin(autocenter_2({extraHeight: -120}));

  //planet.loadPlugin(autoscale({extraHeight: -120}));
  planet.loadPlugin(autoscale_2({extraHeight: -120}));

  planet.loadPlugin(planetaryjs.plugins.earth({
    topojson: { file:   '../../static/json/world-110m.json' },
    //topojson: { file:   './world2topo.json' },

    oceans:   { fill:   '#111' },

    land:     { fill:   '#161A18', stroke: '#4Bffff'},
    borders:  { stroke: '#4Bffff' },
    graticlue: {
      stroke: "white"
    }
  }));

  planet.loadPlugin(planetaryjs.plugins.myWorld2({
       fill: "#292929",
    //fill: 'rgba(1, 1, 1, 1)',
   stroke: '#36e0e0'
  }));

  planet.loadPlugin(planetaryjs.plugins.pings());
  planet.loadPlugin(planetaryjs.plugins.lines());
  planet.loadPlugin(planetaryjs.plugins.dots());
  planet.loadPlugin(planetaryjs.plugins.fixLines());

  planet.loadPlugin(planetaryjs.plugins.zoom({
    scaleExtent: [50, 50000]
  }));
  planet.loadPlugin(planetaryjs.plugins.drag({
    onDragStart: function() {
      //this.plugins.autorotate.pause();
    },
    onDragEnd: function() {
      //this.plugins.autorotate.resume();
    }
  }));
  //planet.loadPlugin(autorotate(3));
  planet.projection.rotate([256, -35, 0]);
  planet.projection.translate([116, 40]);
  planet.draw(canvas);

  retObj.countryInfo=planet.plugins.myWorld.countryInfo;
  retObj.stopRotate=function(){planet.plugins.autorotate.pause()};
  retObj.startRotate=function(){planet.plugins.autorotate.resume()};

  //d3.select("#stopRotate").on("click", function(){
  //  planet.plugins.autorotate.pause();
  //});
  //d3.select("#startRotate").on("click", function(){
  //  planet.plugins.autorotate.resume();
  //});

  /*      // Here we use the `angles` and `colors` scales we built earlier
   // to convert magnitudes to appropriate angles and colors.
   color: "red",
   alpha: 0.5,
   angle: 1,
   ttl:   ttls(100),
   lat: 40,
   lng: 116,
   }
  * */
  retObj.addDot=function(inArg){
    planet.plugins.dots.add(inArg);
  };

  /*
  * inObj{
  *   color,
  *   src: {lat, lng},
  *   dst: {lat, lng},
  *   circle:{ttl, angle, lineWidth},
  *   line{ttl, angle, lineWidth}
  * }
  * */
  retObj.attack=function (inObj){
    inObj.circle.angle=inObj.circle.angle||10;
    inObj.line.lineWidth=inObj.line.lineWidth||3;
    inObj.circle.lineWidth=inObj.circle.lineWidth||3;
    inObj.src.lng=(inObj.src.lng+180)%360-180;
    inObj.src.lat=(inObj.src.lat+90)%180-90;
    inObj.dst.lng=(inObj.dst.lng+180)%360-180;
    inObj.dst.lat=(inObj.dst.lat+90)%180-90;
    planet.plugins.pings.add({
      // Here we use the `angles` and `colors` scales we built earlier
      // to convert magnitudes to appropriate angles and colors.
      //angle: angles(9),
      angles: inObj.circle.angle,
      color: inObj.color,
      lineWidth: inObj.circle.lineWidth||5,
      //color: "red",
      //ttl:   ttls(4),
      ttl: inObj.circle.ttl,
      lat: inObj.src.lat,
      lng: inObj.src.lng,

    });

    planet.plugins.lines.add({
      // Here we use the `angles` and `colors` scales we built earlier
      // to convert magnitudes to appropriate angles and colors.
      //color: colors(4),
      color: inObj.color,
      ttl:   inObj.line.ttl,
      lat0: inObj.src.lat,
      lng0: inObj.src.lng,
      lat1: inObj.dst.lat,
      lng1: inObj.dst.lng,
      lineWidth: inObj.line.lineWidth||3
    });
    setTimeout(function(){
      planet.plugins.pings.add({
        // Here we use the `angles` and `colors` scales we built earlier
        // to convert magnitudes to appropriate angles and colors.
        angles: inObj.circle.angle,
        color: inObj.color,
        lineWidth: inObj.circle.lineWidth||5,
        ttl:   inObj.circle.ttl,
        lat: inObj.dst.lat,
        lng: inObj.dst.lng
      });
    }, inObj.line.ttl-400);
  }

  retObj.fixLine=function(inArg){
    planet.plugins.fixLines.add(inArg);
  };

  retObj.showGraticule=function(){
    planet.plugins.graticule.changeGraticule(true);
  };

  retObj.hideGraticule=function(){
    planet.plugins.graticule.changeGraticule(false);
  };

  // Create a color scale for the various earthquake magnitudes; the
  // minimum magnitude in our data set is 2.5.
  retObj.colors = d3.scale.pow()
    .exponent(3)
    .domain([2, 4, 6, 8, 10])
      .range(['white', 'yellow', 'orange', 'red', 'purple']);
  // Also create a scale for mapping magnitudes to ping angle sizes
  retObj.angles = d3.scale.pow()
    .exponent(3)
    .domain([2.5, 10])
    .range([0.5, 15]);
  // And finally, a scale for mapping magnitudes to ping TTLs
  retObj.ttls = d3.scale.pow()
    .exponent(3)
    .domain([2.5, 10])
    .range([2000, 5000]);

  // Plugin to resize the canvas to fill the window and to
  // automatically center the planet when the window size changes
  function autocenter(options) {
    options = options || {};
    var needsCentering = false;
    var globe = null;

    var resize = function() {
      var width  = window.innerWidth + (options.extraWidth || 0);
      var height = window.innerHeight + (options.extraHeight || 0);
      globe.canvas.width = width;
      globe.canvas.height = height;
      globe.projection.translate([width / 3, height / 2]);
    };

    return function(planet) {
      globe = planet;
      planet.onInit(function() {
        needsCentering = true;
        d3.select(window).on('resize', function() {
          needsCentering = true;
        });
      });

      planet.onDraw(function() {
        if (needsCentering) { resize(); needsCentering = false; }
      });
    };
  };


  function autocenter_2(options) {
    options = options || {};
    var needsCentering = false;
    var globe = null;

    var resize = function() {
      var width  = window.innerWidth + (options.extraWidth || 0);
      var height = window.innerHeight + (options.extraHeight || 0);
      globe.canvas.width = width;
      globe.canvas.height = height;
      globe.projection.translate([116, 40]);
    };

    return function(planet) {
      globe = planet;
      planet.onInit(function() {
        needsCentering = true;
        d3.select(window).on('resize', function() {
          needsCentering = true;
        });
      });

      planet.onDraw(function() {
        if (needsCentering) { resize(); needsCentering = false; }
      });
    };
  };

  // Plugin to automatically scale the planet's projection based
  // on the window size when the planet is initialized
  function autoscale(options) {
    options = options || {};
    return function(planet) {
      planet.onInit(function() {
        var width  = window.innerWidth + (options.extraWidth || 0);
        var height = window.innerHeight + (options.extraHeight || 0);
        planet.projection.scale(Math.min(width, height) / 2);
      });
    };
  };

  function autoscale_2(options) {
    options = options || {};
    return function(planet) {
      planet.onInit(function() {
        //var width  = window.innerWidth + (options.extraWidth || 0);
        //var height = window.innerHeight + (options.extraHeight || 0);
        planet.projection.scale(1000);
      });
    };
  };

  // Plugin to automatically rotate the globe around its vertical
  // axis a configured number of degrees every second.
  function autorotate(degPerSec) {
    return function(planet) {
      var lastTick = null;
      var paused = false;
      planet.plugins.autorotate = {
        pause:  function() { paused = true;  },
        resume: function() { paused = false; }
      };
      planet.onDraw(function() {
        if (paused || !lastTick) {
          lastTick = new Date();
        } else {
          var now = new Date();
          var delta = now - lastTick;
          var rotation = planet.projection.rotate();
          rotation[0] += degPerSec * delta / 1000;
          if (rotation[0] >= 180) rotation[0] -= 360;
          planet.projection.rotate(rotation);
          lastTick = now;
        }
      });
    };
  };

  $("#mapCanvas").mousedown(function(e) {
    var curIndex=planet.plugins.myWorld.curIndex(colorData.hex);
    var showInfo=inArg['showInfo'];

    if(-1==curIndex)
    {
      showInfo.hide();
    }
    else {
      var countryData=planet.plugins.myWorld.getCountryInfo(curIndex);
      showInfo.show({
        'type':'country',
        'data':countryData
      });
    }

    console.log("curIndex: "+curIndex);
    console.log(planet.plugins.myWorld.getCountryInfo(curIndex));

  });

  return retObj;
}
