$(document).ready(function(){function a(){var l=$("#attack-type-ctn");var m=0;for(m=0;m<attackInfoA.length;++m){var n=attackInfoA[m];var k=""+'<div class="box" data-id="'+m+'">'+'<img src="'+n.png+'" class="color">'+'<div class="clr-show" style="background:'+n.color+';"></div>'+'<div class="text">'+n.name+"</div>"+"</div>";var o=$(k);l.append(o)}}a();function d(){var l=new Date();var p=l.getFullYear();var q=l.getMonth()+1;var k=l.getDate();var o=l.getHours();var r=l.getMinutes();var n=l.getSeconds();var m=p+"-";if(q<10){m+="0"}m+=q+"-";if(k<10){m+="0"}m+=k+" ";if(o<10){m+="0"}m+=o+":";if(r<10){m+="0"}m+=r+":";if(n<10){m+="0"}m+=n;return(m)}var j=ShowInfo.createNew({"type":"country","ctn":"#top-info-ctn","trig":"#top-info-min","change":"#top-info-change","title":"#top-info-title",});var f=initPlanet({"showInfo":j});d3.select("#stopRotate").on("click",function(){f.stopRotate()});d3.select("#startRotate").on("click",function(){f.startRotate()});d3.select("#submitInfo").on("click",function(){var l=parseInt($("#srcLat").val());var o=parseInt($("#srcLng").val());var m=parseInt($("#dstLat").val());var k=parseInt($("#dstLng").val());var n=1900;f.attack({src:{lat:l,lng:o},dst:{lat:m,lng:k},color:"#ff1133",circle:{ttl:800,lineWidth:2},line:{ttl:1600,lineWidth:2}})});d3.select("#fixLine").on("click",function(){var l=parseInt($("#srcLat").val());var n=parseInt($("#srcLng").val());var m=parseInt($("#dstLat").val());var k=parseInt($("#dstLng").val());f.fixLine({color:"red",ttl:10000,lat0:l,lng0:n,lat1:m,lng1:k})});d3.select("#graticuleTrigger").on("click",function(){if(d3.select(this).attr("data-need")=="1"){f.hideGraticule();d3.select(this).attr("data-need","0")}else{f.showGraticule();d3.select(this).attr("data-need","1")}});d3.select("#addDot").on("click",function(){f.addDot({color:"red",alpha:1,angle:1.4,ttl:f.ttls(100),lat:40,lng:116,})});controlsFunc();for(var h in stationInfo){f.addDot(stationInfo[h])}var b=AtkCtn.createNew({ctn:"#atk-ctn"});var g=DealWS.createNew({planet:f,host:wsCfg.host,port:wsCfg.port,"atkCtn":b});$("#addDot").click(function(){console.log("add dot");b.addLine({time:"2011-2-21 asdfasfasfasfasdfasdfasfdasfsadfs10:10:10",type:"ARP attack"+num,src:"222.222.222.222:65536 shijiazhuang",dst:"222.222.222.222:65536 shijiazhuang",atkId:num});num+=1});var c=ShowCmdP.createNew({"ctn":"#left-cmd-panel","trig":"#left-cmd-trig","graticule":"#trig-graticule","rotate":"#trig-rotate","planet":f,});$("#trig-graticule").trigger("click");var i=AtkType.createNew({"ctn":"#attack-type-ctn","showInfo":j});function e(m){for(var k=0;k<m.length;++k){var l=m[k];setTimeout(function(){b.addLine({time:l.time,infos:l.infos,src:l.src.ip+":"+l.src.port+" ",dst:l.dst.ip+":"+l.dst.port+" ",atkId:l.attackId,sensorId:l.sensorId,protocalA:l.protocalA,protocalB:l.protocalB,trails:l.trails,references:l.references});f.attack({dotLine:1,src:{lat:parseFloat(l.src.lat),lng:parseFloat(l.src.lng)},dst:{lat:parseFloat(l.dst.lat),lng:parseFloat(l.dst.lng)},color:attackInfoA[l.attackId].color,circle:{ttl:600,lineWidth:2},line:{ttl:1500,lineWidth:2}})},parseInt(Math.random()*2000))}}g.localws.add({"evt":"attack array","hdler":function(k){e(k)}})});
