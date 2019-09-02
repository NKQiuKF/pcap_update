/*! Planetary.js v1.1.2
 *  Copyright (c) 2013 Michelle Tilley
 *
 *  Released under the MIT license
 *  Date: 2015-11-22T10:07:37.594Z
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['d3', 'topojson'], function(d3, topojson) {
      return (root.planetaryjs = factory(d3, topojson, root));
    });
  } else if (typeof exports === 'object') {
    module.exports = factory(require('d3'), require('topojson'));
  } else {
    root.planetaryjs = factory(root.d3, root.topojson, root);
  }
}(this, function(d3, topojson, window) {
  'use strict';

  var originalPlanetaryjs = null;
  if (window) originalPlanetaryjs = window.planetaryjs;
  var plugins = [];

  var doDrawLoop = function(planet, canvas, hooks) {
    d3.timer(function() {
      if (planet.stopped) {
        return true;
      }

      planet.context.clearRect(0, 0, canvas.width, canvas.height);
      for (var i = 0; i < hooks.onDraw.length; i++) {
        hooks.onDraw[i]();
      }
    });
  };

  var initPlugins = function(planet, localPlugins) {
    // Add the global plugins to the beginning of the local ones
    for (var i = plugins.length - 1; i >= 0; i--) {
      localPlugins.unshift(plugins[i]);
    }

    // Load the default plugins if none have been loaded so far
    if (localPlugins.length === 0) {
      if (planetaryjs.plugins.earth)
        planet.loadPlugin(planetaryjs.plugins.earth());
      if (planetaryjs.plugins.pings)
        planet.loadPlugin(planetaryjs.plugins.pings());
    }

    for (i = 0; i < localPlugins.length; i++) {
      localPlugins[i](planet);
    }
  };

  var runOnInitHooks = function(planet, canvas, hooks) {
    // onInit hooks can be asynchronous if they take a parameter;
    // iterate through them one at a time
    if (hooks.onInit.length) {
      var completed = 0;
      var doNext = function(callback) {
        var next = hooks.onInit[completed];
        if (next.length) {
          next(function() {
            completed++;
            callback();
          });
        } else {
          next();
          completed++;
          setTimeout(callback, 0);
        }
      };
      var check = function() {
        if (completed >= hooks.onInit.length) doDrawLoop(planet, canvas, hooks);
        else doNext(check);
      };
      doNext(check);
    } else {
      doDrawLoop(planet, canvas, hooks);
    }
  };

  var startDraw = function(planet, canvas, localPlugins, hooks) {
    planet.canvas = canvas;
    planet.context = canvas.getContext('2d');

    if (planet.stopped !== true) {
      initPlugins(planet, localPlugins);
    }

    planet.stopped = false;
    runOnInitHooks(planet, canvas, hooks);
  };

  var planetaryjs = {
    plugins: {},

    noConflict: function() {
      window.planetaryjs = originalPlanetaryjs;
      return planetaryjs;
    },

    loadPlugin: function(plugin) {
      plugins.push(plugin);
    },

    planet: function() {
      var localPlugins = [];
      var hooks = {
        onInit: [],
        onDraw: [],
        onStop: []
      };

      var planet = {
        plugins: {},

        draw: function(canvas) {
          startDraw(planet, canvas, localPlugins, hooks);
        },

        onInit: function(fn) {
          hooks.onInit.push(fn);
        },

        onDraw: function(fn) {
          hooks.onDraw.push(fn);
        },

        onStop: function(fn) {
          hooks.onStop.push(fn);
        },

        loadPlugin: function(plugin) {
          localPlugins.push(plugin);
        },

        stop: function() {
          planet.stopped = true;
          for (var i = 0; i < hooks.onStop.length; i++) {
            hooks.onStop[i](planet);
          }
        },

        withSavedContext: function(fn) {
          if (!this.context) {
            throw new Error("No canvas to fetch context for");
          }

          this.context.save();
          fn(this.context);
          this.context.restore();
        }
      };

      //********projection type**********

      //planet.projection = d3.geo.orthographic()
      //    .clipAngle(90);


      planet.projection = d3.geo.mercator()
        .center([0, 0])
        .scale(100)
        .translate(999/2, 1800/2);


      //planet.projection = d3.geo.stereographic()
      //    .center([0, 0])
      //    .scale(300)
      //    .translate(999/2, 737/2);

      //planet.projection = d3.geo.gnomonic()
      //    .center([0, 0])
      //    .scale(300)
      //    .translate(999/2, 737/2);

      planet.path = d3.geo.path().projection(planet.projection);

      return planet;
    }
  };

  planetaryjs.plugins.topojson = function(config) {
    return function(planet) {
      planet.plugins.topojson = {};

      planet.onInit(function(done) {
        if (config.world) {
          planet.plugins.topojson.world = config.world;
          setTimeout(done, 0);
        } else {
          var file = config.file || 'world-110m.json';
          d3.json(file, function(err, world) {
            if (err) {
              throw new Error("Could not load JSON " + file);
            }
            planet.plugins.topojson.world = world;
            done();
          });
        }
      });
    };
  };

  planetaryjs.plugins.oceans = function(config) {
    return function(planet) {
      planet.onDraw(function() {
        planet.withSavedContext(function(context) {
          context.beginPath();
          planet.path.context(context)({type: 'Sphere'});
          context.fillStyle = config.fill || 'black';
        
          context.fill();
        });
      });
    };
  };

  planetaryjs.plugins.land = function(config) {
    return function(planet) {
      var land = null;

      planet.onInit(function() {
        var world = planet.plugins.topojson.world;
        land = topojson.feature(world, world.objects.land);
      });

      planet.onDraw(function() {
        planet.withSavedContext(function(context) {
          context.beginPath();
          planet.path.context(context)(land);
          if (config.fill !== false) {
            context.fillStyle = config.fill || 'white';
            context.fill();
          }

          if (config.stroke) {
            if (config.lineWidth) context.lineWidth = config.lineWidth;
            context.strokeStyle = config.stroke;
            context.stroke();
          }
        });
      });
    };
  };

  planetaryjs.plugins.borders = function(config) {
    return function(planet) {
      var borders = null;
      var borderFns = {
        internal: function(a, b) {
          return a.id !== b.id;
        },
        external: function(a, b) {
          return a.id === b.id;
        },
        both: function(a, b) {
          return true;
        }
      };

      planet.onInit(function() {
        var world = planet.plugins.topojson.world;
        var countries = world.objects.countries;

        var type = config.type || 'internal';
        borders = topojson.mesh(world, countries, borderFns[type]);
      });

      planet.onDraw(function() {
        planet.withSavedContext(function(context) {
          context.beginPath();

          planet.path.context(context)(borders);
          context.strokeStyle = config.stroke || 'gray';
          if (config.lineWidth) context.lineWidth = config.lineWidth;
          context.stroke();
        });
      });
    };
  };

  planetaryjs.plugins.earth = function(config) {
    config = config || {};
    var topojsonOptions = config.topojson || {};
    var oceanOptions = config.oceans || {};
    var landOptions = config.land || {};
    var bordersOptions = config.borders || {};
    var graticuleOptions=config.graticule||{};
    return function(planet) {
      planetaryjs.plugins.topojson(topojsonOptions)(planet);
      //planetaryjs.plugins.oceans(oceanOptions)(planet);
      planetaryjs.plugins.graticule(graticuleOptions)(planet);
      //planetaryjs.plugins.land(landOptions)(planet);
      //planetaryjs.plugins.borders(bordersOptions)(planet);


    };
  };

  planetaryjs.plugins.pings = function(config) {
    var pings = [];
    config = config || {};

    var addPing = function(options) {
      options = options || {};
      options.color = options.color || config.color || 'white';
      options.angle = options.angle || config.angle || 5;
      options.ttl   = options.ttl   || config.ttl   || 2000;
      var ping = { time: new Date(), options: options };
      if (config.latitudeFirst) {
        ping.lat = options.lat;
        ping.lng = options.lng;
      } else {
        ping.lng = options.lng;
        ping.lat = options.lat;
      }
      pings.push(ping);
    };

    var drawPings = function(planet, context, now) {
      var newPings = [];
      for (var i = 0; i < pings.length; i++) {
        var ping = pings[i];
        var alive = now - ping.time;
        if (alive < ping.options.ttl) {
          newPings.push(ping);
          drawPing(planet, context, now, alive, ping);
        }
      }
      pings = newPings;
    };

    var drawPing = function(planet, context, now, alive, ping) {
    var alpha = 1 - (alive / ping.options.ttl);
    var color = d3.rgb(ping.options.color);
    var lineWidth=ping.options.lineWidth||5;

    color = "rgba(" + color.r + "," + color.g + "," + color.b + "," + alpha + ")";
    context.strokeStyle = color;
    context.lineWidth = lineWidth;
    //console.log("ping.lineWidth: "+context.lineWidth);
    var circle = d3.geo.circle().origin([ping.lng, ping.lat])
       // .angle(alive / ping.options.ttl * ping.options.angle)();
    .angle(alive / 2000 * ping.options.angle)();
    //console.log("alive:"+alive+"  ping.options.ttl:"+ping.options.ttl+" ping.options.angle:"+ping.options.angle);
    context.beginPath();
    planet.path.context(context)(circle);
    context.stroke();
  };

  return function (planet) {
    planet.plugins.pings = {
      add: addPing
    };

    planet.onDraw(function() {
      var now = new Date();
      planet.withSavedContext(function(context) {
        drawPings(planet, context, now);
      });
    });
  };
  };

  planetaryjs.plugins.zoom = function (options) {
    options = options || {};
    var noop = function() {};
    var onZoomStart = options.onZoomStart || noop;
    var onZoomEnd   = options.onZoomEnd   || noop;
    var onZoom      = options.onZoom      || noop;
    var afterZoom   = options.afterZoom   || noop;
    var startScale  = options.initialScale;
    var scaleExtent = options.scaleExtent || [50, 2000];

    return function(planet) {
      planet.onInit(function() {
        var zoom = d3.behavior.zoom()
          .scaleExtent(scaleExtent);

        if (startScale !== null && startScale !== undefined) {
          zoom.scale(startScale);
        } else {
          zoom.scale(planet.projection.scale());
        }

        zoom
          .on('zoomstart', onZoomStart.bind(planet))
          .on('zoomend', onZoomEnd.bind(planet))
          .on('zoom', function() {
            onZoom.call(planet);
            planet.projection.scale(d3.event.scale);
            afterZoom.call(planet);
          });
        d3.select(planet.canvas).call(zoom);
      });
    };
  };

  planetaryjs.plugins.drag = function(options) {
    options = options || {};
    var noop = function() {};
    var onDragStart = options.onDragStart || noop;
    var onDragEnd   = options.onDragEnd   || noop;
    var onDrag      = options.onDrag      || noop;
    var afterDrag   = options.afterDrag   || noop;

    return function(planet) {
      planet.onInit(function() {
        var drag = d3.behavior.drag()
          .on('dragstart', onDragStart.bind(planet))
          .on('dragend', onDragEnd.bind(planet))
          .on('drag', function() {
            onDrag.call(planet);
            var dx = d3.event.dx;
            var dy = d3.event.dy;
            var rotation = planet.projection.rotate();
            var radius = planet.projection.scale();
            var scale = d3.scale.linear()
              .domain([-1 * radius, radius])
              .range([-90, 90]);
            var degX = scale(dx);
            var degY = scale(dy);
            rotation[0] += degX;
            rotation[1] -= degY;
            if (rotation[1] > 90)   rotation[1] = 90;
            if (rotation[1] < -90)  rotation[1] = -90;
            if (rotation[0] >= 180) rotation[0] -= 360;
            planet.projection.rotate(rotation);
            afterDrag.call(planet);
          });
        d3.select(planet.canvas).call(drag);
      });
  };
  };

  //-------------------------------------------------------------
  planetaryjs.plugins.lines = function(config) {
    var lines = [];
    config = config || {};

    var addLine = function(options) {
      options = options || {};
      options.color = options.color || config.color || 'red';
      options.angle = options.angle || config.angle || 5;
      options.ttl   = options.ttl   || config.ttl   || 2000;
      options.lineWidth=options.lineWidth || 2;
      var line = { time: new Date(), options: options };
      //if (config.latitudeFirst) {
      //    ping.lat = lng;
      //    ping.lng = lat;
      //} else {
      //    ping.lng = lng;
      //    ping.lat = lat;
      //}
      options.lng0=(options.lng0+180)%360-180;
      options.lat0=(options.lat0+90)%180-90;
      options.lng1=(options.lng1+180)%360-180;
      options.lat1=(options.lat1+90)%180-90;
      line.lat0=options.lat0;
      line.lng0=options.lng0;
      line.lat1=options.lat1;
      line.lng1=options.lng1;
      lines.push(line);
    };

    var drawLines = function(planet, context, now) {
      var newLines = [];
      for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        var alive = now - line.time;
        if (alive < line.options.ttl) {
          newLines.push(line);
          drawLine(planet, context, now, alive, line);
        }
      }
      lines = newLines;
    };

    var drawLine = function(planet, context, now, alive, line) {

      var alpha = 1 - (alive / line.options.ttl);
      var color = d3.rgb(line.options.color);

      //color = "rgba(" + color.r + "," + color.g + "," + color.b + "," + alpha + ")";
      //context.strokeStyle = line.options.color;
      //console.log("line.options.color: "+line.options.color);
      var alive = now - line.time;
      //console.log("alive: "+alive);
      var preTime=300;
      var allTime=line.options.ttl;
      var diffLat=(line.lat1-line.lat0)/(line.options.ttl-preTime);
      var diffLng=(line.lng1-line.lng0)/(line.options.ttl-preTime);
      var srcP={"lat": 0, "lng": 0};
      var dstP={"lat": 0, "lng": 0};
      var durPFunc=d3.geo.interpolate([line.lng0, line.lat0], [line.lng1, line.lat1]);
      //d3.geo.interpolate(a, b);
      if(alive<preTime)
      {
        srcP.lat=line.lat0;
        srcP.lng=line.lng0;
      }
      else{
        //srcP.lat=line.lat0+(alive-preTime)*diffLat;
        //srcP.lng=line.lng0+(alive-preTime)*diffLng
        var t=1.0*(alive-preTime)/(allTime-preTime);

        var tmpP=durPFunc(t);
        srcP.lat=tmpP[1];
        srcP.lng=tmpP[0];
      }

      if((line.options.ttl-alive)<preTime)
      {
        dstP.lat=line.lat1;
        dstP.lng=line.lng1;
      }
      else{
        //dstP.lat=line.lat0+alive*diffLat;
        //dstP.lng=line.lng0+alive*diffLng;
        var t=1.0*alive/(allTime-preTime);

        var tmpP=durPFunc(t);
        dstP.lat=tmpP[1];
        dstP.lng=tmpP[0];
        //console.log("t:"+JSON.stringify(tmpP));
      }

      //console.log("src: "+JSON.stringify(srcP)+" dst:"+JSON.stringify(dstP));

      var atk ={
        "type": "Feature",
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [srcP.lng, srcP.lat], [dstP.lng, dstP.lat]
          ]
        }
      };

      var srcPxl= planet.projection([srcP.lng, srcP.lat]);
      var dstPxl= planet.projection([dstP.lng, dstP.lat]);
      var grd = context.createLinearGradient(dstPxl[0], dstPxl[1], srcPxl[0], dstPxl[1]);
      var d3color=d3.rgb(line.options.color);
      var strColor1="rgba( "+d3color.r+","+d3color.g+","+d3color.b+", "+1+")";
      var strColor2="rgba( "+d3color.r+","+d3color.g+","+d3color.b+", "+0+")";

      grd.addColorStop(0, strColor1);
      grd.addColorStop(1, strColor2);
      context.save();
      context.strokeStyle=grd;

      context.shadowColor=line.options.color;

      context.shadowBlur=5;
      context.lineJoin="round";
      context.lineCap="round";
      context.lineWidth=line.options.lineWidth;
      context.beginPath();
      planet.path.context(context)(atk);
      //context.closePath();
      context.stroke();
      context.restore();

      //context.save();
      //context.beginPath();
      //context.shadowColor=line.options.color;
      //context.shadowBlur=40;
      //var circle = d3.geo.circle().origin([dstP.lng, dstP.lat])
      //    .angle(0.1)();
      //planet.path.context(context)(circle);
      ////context.closePath();
      //context.stroke();
      //context.restore();

      //var hd ={
      //    "type": "Feature",
      //    "geometry": {
      //        "type": "Point",
      //        "coordinates": [dstP.lng, dstP.lat]
      //
      //    }
      //};
      //context.beginPath();
      //context.shadowColor=line.options.color;
      //context.shadowBlur=40;
      //context.lineWidth=0;
      //planet.path.context(context)(hd);
      ////context.closePath();
      //context.stroke();

      //var hd ={
      //    "type": "Feature",
      //    "geometry": {
      //        "type": "Point",
      //        "coordinates": [dstP.lng, dstP.lat]
      //
      //    }
      //};
      //context.save();
      //context.shadowBlur=20;
      //context.shadowColor="white";
      //context.strokeWidth=10;
      //context.strokeColor="green";
      //context.beginPath();
      //planet.path.context(context)(hd);
      ////context.closePath();
      //context.stroke();
      //context.restore();



      //context.save();
      //context.strokeStyle = line.options.color;
      //context.lineWidth = 2;
      //context.beginPath();
      //console.log("dstPxl[0],dstPxl[1]: "+dstPxl[0]+" "+dstPxl[1]);
      //context.shadowBlur=80;
      //context.shadowColor="white";
      //context.arc(dstPxl[0], dstPxl[1], 0.1, 0, 2 * Math.PI);
      //context.closePath();
      //context.stroke();
      //context.restore();



    };

    return function (planet) {
      planet.plugins.lines = {
        add: addLine
      };

      planet.onDraw(function() {
        var now = new Date();
        planet.withSavedContext(function(context) {
          drawLines(planet, context, now);
        });
      });
    };
  };


  planetaryjs.plugins.fixLines = function(config) {
    var lines = [];
    config = config || {};

    var addLine = function(options) {
      options = options || {};
      options.color = options.color || config.color || 'red';
      options.angle = options.angle || config.angle || 5;
      options.ttl   = options.ttl   || config.ttl   || 2000;
      options.lineWidth=options.lineWidth || 2;
      var line = { time: new Date(), options: options };
      //if (config.latitudeFirst) {
      //    ping.lat = lng;
      //    ping.lng = lat;
      //} else {
      //    ping.lng = lng;
      //    ping.lat = lat;
      //}
      options.lng0=(options.lng0+180)%360-180;
      options.lat0=(options.lat0+90)%180-90;
      options.lng1=(options.lng1+180)%360-180;
      options.lat1=(options.lat1+90)%180-90;
      line.lat0=options.lat0;
      line.lng0=options.lng0;
      line.lat1=options.lat1;
      line.lng1=options.lng1;
      lines.push(line);
    };

    var drawLines = function(planet, context, now) {
      var newLines = [];
      for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        var alive = now - line.time;
        if (alive < line.options.ttl) {
          newLines.push(line);
          drawLine(planet, context, now, alive, line);
        }
      }
      lines = newLines;
    };

    var drawLine = function(planet, context, now, alive, line) {

      var alpha = 1 - (alive / line.options.ttl);
      var color = d3.rgb(line.options.color);

      //color = "rgba(" + color.r + "," + color.g + "," + color.b + "," + alpha + ")";
      //context.strokeStyle = line.options.color;
      //console.log("line.options.color: "+line.options.color);
      var alive = now - line.time;
      //console.log("alive: "+alive);
      var preTime=400;
      var diffLat=(line.lat1-line.lat0)/(line.options.ttl-preTime);
      var diffLng=(line.lng1-line.lng0)/(line.options.ttl-preTime);
      var srcP={"lat": line.options.lat0, "lng": line.options.lng0};
      var dstP={"lat": line.options.lat1, "lng": line.options.lng1};



      //console.log("src: "+JSON.stringify(srcP)+" dst:"+JSON.stringify(dstP));

      var atk ={
        "type": "Feature",
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [srcP.lng, srcP.lat], [dstP.lng, dstP.lat]
          ]
        }
      };


      context.save();
      context.strokeStyle=line.options.color;

      context.shadowColor=line.options.color;
      context.shadowBlur=3;
      context.lineJoin="round";
      context.lineCap="round";
      context.lineWidth=line.options.lineWidth;
      context.lineWIdth=1;
      context.setLineDash([5, 15]);

      context.beginPath();
      planet.path.context(context)(atk);
      //context.closePath();
      context.stroke();
      context.restore();






      /*
       context.save();
       context.globalAlpha = 0.5;
       context.strokeStyle = line.options.color;
       context.lineWidth = 10;
       context.beginPath();
       context.arc(dstPxl[0], dstPxl[1], 1, 0, 2 * Math.PI);
       context.closePath();
       context.stroke();
       context.restore();
       */
    };

    return function (planet) {
      planet.plugins.fixLines = {
        add: addLine
      };

      planet.onDraw(function() {
        var now = new Date();
        planet.withSavedContext(function(context) {
          drawLines(planet, context, now);
        });
      });
    };
  };

  planetaryjs.plugins.dots = function(config) {
    var dots = [];
    config = config || {};

    var addDot = function(options) {
      options = options || {};
      options.color = options.color || config.color || 'white';
      options.angle = options.angle || config.angle || 5;
      options.ttl   = options.ttl   || config.ttl   || 2000;
      var dot = { time: new Date(), options: options };
      if (config.latitudeFirst) {
        dot.lat = options.lat;
        dot.lng = options.lng;
      } else {
        dot.lng = options.lng;
        dot.lat = options.lat;
      }
      dots.push(dot);
    };

    var drawDots = function(planet, context, now) {
      var newDots = [];
      for (var i = 0; i < dots.length; i++) {
        var dot = dots[i];
        var alive = now - dot.time;
        if (alive < dot.options.ttl) {
          newDots.push(dot);
          drawDot(planet, context, now, alive, dot);
        }
      }
      dots = newDots;
    };

    var drawDot = function(planet, context, now, alive, dot) {
      //var alpha = 1 - (alive / ping.options.ttl);




      var alpha=dot.options.alpha||0.5;
      var color = d3.rgb(dot.options.color);
      var angle=dot.options.angle||1;
      var lineWidth=0;
      color = "rgba(" + color.r + "," + color.g + "," + color.b + "," + alpha + ")";
      context.strokeStyle = color;
      context.lineWidth = lineWidth;
      //var circle = d3.geo.circle().origin([dot.lng, dot.lat])
      //    .angle(0.000001)();

      var atk ={
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [dot.lng, dot.lat]
        }
      };

      //console.log("alive:"+alive+"  ping.options.ttl:"+ping.options.ttl+" ping.options.angle:"+ping.options.angle);
      context.beginPath();
      //planet.path.context(context)(atk);
      var circle = d3.geo.circle().origin([dot.lng, dot.lat]).angle(angle)();
      planet.path.context(context)(circle);

      context.fillStyle=color;
      context.stroke();
      context.fill();
    };

    return function (planet) {
      planet.plugins.dots = {
        add: addDot
      };

      planet.onDraw(function() {
        var now = new Date();
        planet.withSavedContext(function(context) {
          drawDots(planet, context, now);
        });
      });
    };
  };

  planetaryjs.plugins.graticule = function(config) {

    var graticuleTrigger=false;
    function changeGraticule(isNeed)
    {
      graticuleTrigger=isNeed;
    }

    return function(planet) {
      var graticule = null;
      planet.plugins.graticule = {
        "changeGraticule": changeGraticule
      };

      planet.onInit(function() {
        graticule = d3.geo.graticule()
          .extent([[-180, -90], [180, 90]])
          .step([10, 10])();
      });

      planet.onDraw(function() {

        if (graticuleTrigger){

          planet.withSavedContext(function (context) {
            context.beginPath();
            planet.path.context(context)(graticule);
            context.strokeStyle = config.stroke || 'gray';
            if (config.lineWidth) context.lineWidth = config.lineWidth;
            context.stroke();
          });
         }
      });
    };

  };

  planetaryjs.plugins.myWorld = function(config) {
    var myWorld=null;
    var baseColor = "#418541";
    var countryColors=[];
    var diff=0;
    var baseR=0;
    var baseG=0;
    var baseB=0;
    var curIndex=-1;
    var num=0;
    var changeCurIndex=function(inColor){
      var diffR = parseInt(inColor.substr(1, 2), 16) - baseR;
      var diffG = parseInt(inColor.substr(3, 2), 16) - baseG;
      var diffB = parseInt(inColor.substr(5, 2), 16) - baseB;
      var index = diffR + diffG + diffB;
      if(index<num && index>-1)
      {
        curIndex=index;
      }
      else{
        curIndex=-1;
      }
      //console.log("curIndex: "+curIndex);
      return curIndex;
    };

    var getCountryInfo=function(inArg){
      if(inArg==-1)
      {
        return {};
      }
      else{
        return countryColors[inArg];
      }
    };

    return function(planet) {
      var countries = null;
      planet.onInit(function(done) {
        d3.json("../../static/json/china.geojson", function(error, data){
          myWorld=data;
          //console.log("myWord: "+JSON.stringify(myWorld));
          var countries=data.features;
          num=countries.length;
          baseR=parseInt(baseColor.substr(1, 2), 16);
          baseG=parseInt(baseColor.substr(3, 2), 16);
          baseB=parseInt(baseColor.substr(5, 2), 16);
          for(var i=0; i<num; ++i)
          {
            var pre=parseInt(i/3);
            var apd=parseInt(i-pre*2);
            var rstR=baseR+pre;
            var rstG=baseG+apd;
            var rstB=baseB+pre;

            var strR=rstR.toString(16);
            if(1==strR.length)
            {
              strR='0'+strR;
            }

            var strG=rstG.toString(16);
            if(1==strR.length)
            {
              strG='0'+strG;
            }

            var strB=rstB.toString(16);
            if(1==strB.length)
            {
              strB='0'+strB;
            }

            var colorStr="#"+strR+strG+strB;
            //console.log("id: "+countries[i].id);
            countryColors.push({
              "id": countries[i].id,
              "name": countries[i].properties.name,
              "color": colorStr
            });
          }
          done();
          //console.log("color: "+JSON.stringify(countryColors));
        });
      });

      planet.onDraw(function() {
        planet.withSavedContext(function(context) {

          for(var i=0; i<myWorld.features.length; ++i) {


            context.beginPath();
            planet.path.context(context)(myWorld.features[i]);
            if (true) {
              if(i==curIndex){
                context.fillStyle = "green";
              }
              else{
                context.fillStyle = countryColors[i].color;
                //context.fillStyle = 'red';
                //console.log(countryColors[i].color);
              }

              context.fill();
            }

            if (config.stroke) {
              if (config.lineWidth) {
                context.lineWidth = config.lineWidth;
              }
              if(i==curIndex){
                context.strokeStyle = "#ffffff";
              }
              else{
                context.strokeStyle = config.stroke;
              }
              context.stroke();
            }

          }

          if(curIndex!=-1){
            context.closePath();
            context.beginPath();
            planet.path.context(context)(myWorld.features[curIndex]);
            //console.log(JSON.stringify('aaa'+JSON.stringify(myWorld.features[curIndex])));

            context.lineWidth = 2;
            context.strokeStyle = "#fff";

            context.stroke();

          }
          });
      });
      planet.plugins.myWorld = {
        "curIndex": changeCurIndex,
        "getCountryInfo": getCountryInfo
      };

    };
  };
  planetaryjs.plugins.myWorld2 = function(config) {
    var myWorld=null;
    var baseColor = "#418541";
    var countryColors=[];
    var diff=0;
    var baseR=0;
    var baseG=0;
    var baseB=0;
    var curIndex=-1;
    var num=0;
    var changeCurIndex=function(inColor){
      var diffR = parseInt(inColor.substr(1, 2), 16) - baseR;
      var diffG = parseInt(inColor.substr(3, 2), 16) - baseG;
      var diffB = parseInt(inColor.substr(5, 2), 16) - baseB;
      var index = diffR + diffG + diffB;
      if(index<num && index>-1)
      {
        curIndex=index;
      }
      else{
        curIndex=-1;
      }
      //console.log("curIndex: "+curIndex);
      return curIndex;
    };

    var getCountryInfo=function(inArg){
        if(inArg==-1)
        {
          return {};
        }
        else{
          return countryColors[inArg];
        }
    };

    return function(planet) {
      var countries = null;
      planet.onInit(function(done) {
        d3.json("../../static/json/china.geojson", function(error, data){
          myWorld=data;
          //console.log("myWord: "+JSON.stringify(myWorld));
          var countries=data.features;
          num=countries.length;
          baseR=parseInt(baseColor.substr(1, 2), 16);
          baseG=parseInt(baseColor.substr(3, 2), 16);
          baseB=parseInt(baseColor.substr(5, 2), 16);
          for(var i=0; i<num; ++i)
          {
            var pre=parseInt(i/3);
            var apd=parseInt(i-pre*2);
            var rstR=baseR+pre;
            var rstG=baseG+apd;
            var rstB=baseB+pre;

            var strR=rstR.toString(16);
            if(1==strR.length)
            {
              strR='0'+strR;
            }

            var strG=rstG.toString(16);
            if(1==strR.length)
            {
              strG='0'+strG;
            }

            var strB=rstB.toString(16);
            if(1==strB.length)
            {
              strB='0'+strB;
            }

            var colorStr="#"+strR+strG+strB;
            //console.log("id: "+countries[i].id);
            countryColors.push({
              "id": countries[i].id,
              "name": countries[i].properties.name,
              "color": config.fill||'#444444'
            });
          }
          done();
          //console.log("color: "+JSON.stringify(countryColors));
        });
      });

      planet.onDraw(function() {
        planet.withSavedContext(function(context) {

          for(var i=0; i<myWorld.features.length; ++i) {

              context.beginPath();

              planet.path.context(context)(myWorld.features[i]);
              if (true) {
                if(i==curIndex){
                  context.fillStyle = "green";
                }
                else{
                  context.fillStyle = countryColors[i].color;
                  //context.fillStyle = 'red';
                  //console.log(countryColors[i].color);
                }
                context.fill();
              }

              if (config.stroke) {
                if (config.lineWidth) {
                  context.lineWidth = config.lineWidth;
                }
                if(i==curIndex){
                  context.strokeStyle = "#ffffff";
                }
                else{
                  context.strokeStyle = config.stroke;
                }
                context.stroke();
              }

          }

          if(curIndex!=-1){
            context.closePath();
            context.beginPath();
            planet.path.context(context)(myWorld.features[curIndex]);
            context.lineWidth = 2;
            context.strokeStyle = "#fff";
            context.stroke();
          }
        });
      });
      planet.plugins.myWorld = {
        "curIndex": changeCurIndex,
        "getCountryInfo": getCountryInfo
      };
    };
  };
  //--------------------------------------------------------------
  return planetaryjs;
}));

