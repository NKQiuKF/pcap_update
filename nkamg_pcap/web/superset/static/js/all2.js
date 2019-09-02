var datenow=["","","","","","",""];
var MakePie=
{createNew:function(b,c){var a={};require(["echarts","echarts/chart/pie"],function(d){a.myChart=d.init(b[0]);a.option={backgroundColor:"#2c343c",tooltip:{trigger:"item",formatter:"{a} <br/>{b} : {c} ({d}%)"},title:{text:c["title"],x:"center",textStyle:{color:"#ccc"}},legend:{x:"center",y:"bottom",data:[],textStyle:{color:"#ccc"}},toolbox:{show:true,feature:{restore:{show:true},saveAsImage:{show:true}}},calculable:false,series:[{name:c["name"],type:"pie",selectedMode:"single",radius:[0,70],roseType:"area",x:"20%",width:"40%",funnelAlign:"right",max:1548,itemStyle:{normal:{label:{show:false},labelLine:{show:false}}},data:[{itemStyle:{normal:{color:"rgb(205,164,158)"}},},{itemStyle:{normal:{color:"rgb(197,31,31)"}},},{itemStyle:{normal:{color:"rgb(255,255,255)"}},},{itemStyle:{normal:{color:"rgb(156,38,50)"}},},{itemStyle:{normal:{color:"rgb(71,31,31)"}},}],},{name:c["name"],type:"pie",radius:[100,140],x:"60%",width:"35%",funnelAlign:"left",max:1048,data:[{itemStyle:{normal:{label:{textStyle:{color:"rgb(3,41,81)"}},labelLine:{lineStyle:{color:"rgb(3,41,81)"}},color:"rgb(3,41,81)"},},},{itemStyle:{normal:{label:{textStyle:{color:"rgb(138,171,202)"}},labelLine:{lineStyle:{color:"rgb(138,171,202)"}},color:"rgb(138,171,202)"},},},{itemStyle:{normal:{label:{textStyle:{color:"rgb(17,64,108)"}},labelLine:{lineStyle:{color:"rgb(17,64,108)"}},color:"rgb(17,64,108)"},},},{itemStyle:{normal:{label:{textStyle:{color:"rgb(255,255,255)"}},labelLine:{lineStyle:{color:"rgb(255,255,255)"}},color:"rgb(255,255,255)"},},},{itemStyle:{normal:{label:{textStyle:{color:"rgb(1,158,213)"}},labelLine:{lineStyle:{color:"rgb(1,158,213)"}},color:"rgb(1,158,213)"},},},]}]};a.myChart.setOption(a.option)});a.interval=function(d,f){var e=0;for(e=0;e<d.length;++e){a.option.series[1].data[e]={};a.option.series[1].data[e].value=d[e]["count"];a.option.series[1].data[e].name=d[e]["name"]}for(e=0;e<f.length;++e){a.option.series[0].data[e]={};a.option.series[0].data[e].value=f[e]["count"];a.option.series[0].data[e].name=f[e]["name"];a.option.legend.data[e]=f[e]["name"]}a.myChart.setOption(a.option)};return a}};function coreFunc(a,c,b,d){$.ajax({type:"GET",url:"/tmp/pie",success:function(e){console.log(JSON.stringify(e));a.interval(e["data"]["agent"],e["data"]["agent2"]);c.interval(e["data"]["host"],e["data"]["host2"]);b.interval(e["data"]["domain"],e["data"]["domain2"]);d.interval(e["data"]["outip"],e["data"]["outip2"])},error:function(f,e){console.log("err: "+JSON.stringify(e))}})}function coreFuncLine(a){$.ajax({type:"GET",url:"/tmp/line",success:function(b){console.log(JSON.stringify(b));a.interval(b["data"])},error:function(c,b){console.log("err: "+JSON.stringify(b))}})}function coreFuncTime(){$.ajax(
{type:"GET",url:"/tmp/time",
success:function(a)
{console.log(JSON.stringify(a));
for(var b=6;b>6-a["data"]["atktype1"].length;b--)
{
    datenow[6-b]=a["data"]["atktype1"][a["data"]["atktype1"].length-b-1]["date"];
}
for(var c=6-a["data"]["atktype1"].length;c>-1;c--)
{
    datenow[6-c]='nodata';
}},error:function(b,a){console.log("err: "+JSON.stringify(a))}}

)}function dealPieData(b,e,d,f,c){var a=setInterval(function(){coreFunc(b,e,d,f)},c)}function dealLineData(a,b){var c=setInterval(function(){coreFuncLine(a)},b)}
var MakeLine=
{createNew:function(b,c){
	var a={};
	require(
		[
		"echarts",
		"echarts/chart/line"
		],
		function(d)
		{
			a.myLine=d.init(b[0]);
			a.option={backgroundColor:'#2c343c',tooltip:{trigger:'axis'},
			textStyle:{color:'#ccc'},


            noDataLoadingOption :{

                    text: '数据量不足七天，无法生成折线图！',

                    effect:'dynamicLine',

    textStyle : {
        fontSize : 20
    }
},
			legend:{data:['恶意软件','黑客攻击','垃圾邮件','网络爬虫',"可疑数据","ARP攻击"],
			textStyle:{color:"#ccc"},
		},
		toolbox:
		{
			show:true,
			feature:
			{
				restore:
				{
					show:true
				},
				saveAsImage:
				{
					show:true
				}
			}
		},
		grid:
		{
			left:"3%",
			right:"4%",
			bottom:"3%",
			containLabel:true
		},
		calculable:true,
		xAxis:
		{
			axisLabel:
			{
				textStyle:
				{
					color:"#ccc"
				}
			},
			type:"category",
			boundaryGap:false,
			data:datenow
		},
		yAxis:
		{
			axisLabel:
			{
				textStyle:
				{
					color:"#ccc"
				}
			},
			type:"value"
		},
		series:[
		{
			name:"恶意软件",
			type:"line",
			stack:"总量",
			data:[0,0,0,0,0,0,0]
		},
		{
			name:"黑客攻击",
			type:"line",
			stack:"总量",
			data:[0,0,0,0,0,0,0]
		},
		{
			name:"垃圾邮件",
			type:"line",
			stack:"总量",
			data:[0,0,0,0,0,0,0]
		},
{name:"网络爬虫",type:"line",stack:"总量",data:[0,0,0,0,0,0,0]},
{name:"可疑数据",type:"line",stack:"总量",data:[0,0,0,0,0,0,0]},
{name:"ARP攻击",type:"line",stack:"总量",data:[0,0,0,0,0,0,0]}]};
		a.myLine.setOption(a.option)});
	a.interval=function(d)
	{
		for(var e=6;e>6-d["atktype1"].length;e--){
a.option.series[0].data[6-e]=d["atktype1"][d["atktype1"].length-e-1]["count"];
}
for(var f=6-d["atktype1"].length;f>-1;f--)
{
    a.option.series[0].data[6-f]=0;
}
		for(var e=6;e>6-d["atktype1"].length;e--){
a.option.series[1].data[6-e]=d["atktype2"][d["atktype1"].length-e-1]["count"];
}
for(var f=6-d["atktype1"].length;f>-1;f--)
{
    a.option.series[1].data[6-f]=0;
}
		for(var e=6;e>6-d["atktype1"].length;e--){
a.option.series[2].data[6-e]=d["atktype3"][d["atktype1"].length-e-1]["count"];
}
for(var f=6-d["atktype1"].length;f>-1;f--)
{
    a.option.series[2].data[6-f]=0;
}
		for(var e=6;e>6-d["atktype1"].length;e--){
a.option.series[3].data[6-e]=d["atktype4"][d["atktype1"].length-e-1]["count"];
}
for(var f=6-d["atktype1"].length;f>-1;f--)
{
    a.option.series[3].data[6-f]=0;
}
		for(var e=6;e>6-d["atktype1"].length;e--){
a.option.series[4].data[6-e]=d["atktype5"][d["atktype1"].length-e-1]["count"];
}
for(var f=6-d["atktype1"].length;f>-1;f--)
{
    a.option.series[4].data[6-f]=0;
}
		for(var e=6;e>6-d["atktype1"].length;e--){
a.option.series[5].data[6-e]=d["atktype6"][d["atktype1"].length-e-1]["count"];
}
for(var f=6-d["atktype1"].length;f>-1;f--)
{
    a.option.series[5].data[6-f]=0;
}
			a.myLine.setOption(a.option)};return a}};var MakeDash={createNew:function(b){var a={};
require(["echarts","echarts/chart/gauge"],function(c){a.myDash=c.init(b[0]);a.option={backgroundColor:"#2c343c",tooltip:{formatter:"{a} <br/>{c} {b}"},toolbox:{show:true,feature:{restore:{show:true},saveAsImage:{show:true}}},series:[{center:["36%","50%"],name:"CPU",type:"gauge",z:3,min:0,max:100,splitNumber:10,axisLine:{lineStyle:{width:5}},axisTick:{length:15,lineStyle:{color:"auto"}},splitLine:{length:20,lineStyle:{color:"auto"}},title:{textStyle:{fontWeight:"bolder",fontSize:20,fontStyle:"italic",color:"#ccc"}},detail:{textStyle:{fontWeight:"bolder",fontSize:20,}},data:[{value:40,name:"CPU"}]},{name:"内存",type:"gauge",center:["74%","50%"],radius:"50%",min:0,max:100,startAngle:135,endAngle:45,splitNumber:2,axisLine:{lineStyle:{color:[[0.2,"#228b22"],[0.8,"#48b"],[1,"#ff4500"]],width:5}},axisTick:{splitNumber:5,length:10,lineStyle:{color:"auto"}},axisLabel:{formatter:function(d){switch(d+""){case"0":return"L";case"50":return"内存";case"100":return"H"}}},splitLine:{length:15,lineStyle:{color:"auto"}},pointer:{width:2},title:{show:false},detail:{show:false},data:[{value:0.5,name:"%"}]},{name:"磁盘",type:"gauge",center:["74%","50%"],radius:"50%",min:0,max:100,startAngle:315,endAngle:225,splitNumber:2,axisLine:{lineStyle:{color:[[0.2,"#228b22"],[0.8,"#48b"],[1,"#ff4500"]],width:5}},axisTick:{show:false},axisLabel:{formatter:function(d){switch(d+""){case"0":return"L";case"50":return"磁盘";case"100":return"H"}}},splitLine:{length:15,lineStyle:{color:"auto"}},pointer:{width:2},title:{show:false},detail:{show:false},data:[{value:0.5,name:"%"}]}]};a.myDash.setOption(a.option,true)});a.interval=function(c){a.option.series[0].data[0].value=(c.cpu).toFixed(2).toString();a.option.series[1].data[0].value=c.memory;a.option.series[2].data[0].value=c.disk;a.myDash.setOption(a.option,true)};return a}};var DashLine={createNew:function(b){var a={};require(["echarts","echarts/chart/line"],function(c){a.myLine=c.init(b[0]);a.option={backgroundColor:"#2c343c",tooltip:{trigger:"axis"},legend:{textStyle:{color:"#ccc"},data:["CPU","Memory"]},toolbox:{show:true,feature:{restore:{show:true},saveAsImage:{show:true}}},calculable:true,xAxis:[{axisLabel:{textStyle:{color:"#ccc"}},type:"category",boundaryGap:false,data:["0","1","2","3","4","5","6","7","8","9","10","11","12","13"]}],yAxis:[{axisLabel:{textStyle:{color:"#ccc"},formatter:"{value} %"},type:"value",position:"left",min:0,max:100,},{type:"value",position:"right",axisLabel:{formatter:"{value} %"}}],series:[{name:"CPU",type:"line",data:[0,0,0,0,0,0,0,0,0,0,0,0,0,0],},{name:"Memory",type:"line",data:[0,0,0,0,0,0,0,0,0,0,0,0,0,0],}]};a.myLine.setOption(a.option)});a.interval=function(c){a.option.series[0].data.pop();a.option.series[0].data.unshift(c.cpu);a.option.series[1].data.pop();a.option.series[1].data.unshift(c.memory);a.myLine.setOption(a.option)};return a}};function getSvInfo(b,a){setInterval(function(){(Math.random()*100).toFixed(2);$.get("/tmp/server_info",function(h){var j=h["cpu"];var e=h["mem"]["used"];var g=h["mem"]["all"];var d=(e/g*100).toFixed(2);var f=h["disk"]["used"];var i=h["disk"]["all"];var c=(f/i*100).toFixed(2);b.interval({"cpu":j,"memory":d,"disk":c,});$("#cpu-percentage").text((j).toFixed(2)+"%");$("#mem-info").text(e+"M/"+g+"M");$("#disk-info").text(f+"G/"+i+"G");a.interval({"cpu":j,"memory":d,})})},500)}$(document).ready(function(d){require.config({paths:{echarts:"../../static/js/build/dist"}});var b=MakePie.createNew($("#pie1"),{"title":"被攻击主机IP","name":"IP"});var a=MakePie.createNew($("#pie2"),{"title":"访问网址比例","name":"访问网址"});var h=MakePie.createNew($("#pie3"),{"title":"访问网站比例","name":"访问网站"});var g=MakePie.createNew($("#pie4"),{"title":"攻击来源IP","name":"IP"});setTimeout(function(){coreFunc(b,a,h,g)},300);dealPieData(b,a,h,g,1800000);coreFuncTime();setInterval(function(){coreFuncTime()},10000);var c=MakeLine.createNew($("#stacked-graph"));setTimeout(function(){coreFuncLine(c)},300);dealLineData(c,1800000);var f=MakeDash.createNew($("#dash-board"));var e=DashLine.createNew($("#dash-line"));getSvInfo(f,e)});
