$(document).ready(function(){
  queue()
    .defer(d3.json, "/tmp/refresh_eqp")
    .await(show_eqp);
  set_update_timer();
 });

function set_update_timer(){
  setInterval(function(){
    queue()
      .defer(d3.json, "/tmp/refresh_eqp")
      .await(show_eqp);
  }, 60000);
}

function show_eqp(error,msg){
  var dataset = msg['data'];
  var eqp = d3.select("body").select(".all-eqp").selectAll(".one-eqp");
  var eqp_update = eqp.data(dataset);
  var eqp_enter = eqp_update.enter();
  
  var one_eqp = eqp_enter.append("div")
           .attr("class","one-eqp")
           .attr("id",function(d,i){return "div_"+d['id'];})
  	   .style("display","inline-block");
  	 
  var eqp_top = one_eqp.append("div")
    .attr("class",function(d,i){return "top"+d['authority'];})
    .attr("id",function(d,i){return "top_"+d['id'];})
    .append("i")
    .attr("class","icon-laptop vl-text");
 
  //d3.selectAll(".one-eqp")
  var eqp_text = one_eqp.append("div")
                .attr("class","text");

    // show eqp name
  var eqp_name = eqp_text.append("div")
                .attr("class","text-line name");

  eqp_name.append("div")
          .attr("class","text-line-left")
          .append("span")
          .attr("class","title-text")
          .text("用户:");

  eqp_name.append("div")
          .attr("class","text-line-right")
          .append("span")
          .text(function(d,i){return d['name'];});
  
  var eqp_department = eqp_text.append("div")
                .attr("class","text-line department");
  eqp_department.append("div")
          .attr("class","text-line-left")
          .append("span")
          .attr("class","title-text")
          .text("部门:");

  eqp_department.append("div")
          .attr("class","text-line-right")
          .append("span")
          .text(function(d,i){return d['department'];});


  var eqp_ip = eqp_text.append("div")
              .attr("class","text-line ip");
  
  eqp_ip.append("div")
        .attr("class","text-line-left")
        .append("span")
        .attr("class","title-text")
        .text("IP地址:");

  eqp_ip.append("div")
        .attr("class","text-line-right")
        .append("span")
        .text(function(d,i){return d["ip"];});

  var eqp_mac = eqp_text.append("div")
           .attr("class","text-line mac");
  
  eqp_mac.append("div")
         .attr("class","text-line-left")
         .append("span")
         .attr("class","title-text")
         .text("MAC地址:");

  eqp_mac.append("div")
         .attr("class","text-line-right")
         .text(function(d,i){return d["mac"];});
/*
  var eqp_os = eqp_text.append("div")
                .attr("class","text-line os");

  eqp_os.append("div")
          .attr("class","text-line-left")
          .append("span")
          .attr("class","title-text")
          .text("操作系统:");

  eqp_os.append("div")
          .attr("class","text-line-right")
          .append("span")
          .text(function(d,i){return d['os'];});

  var eqp_computer = eqp_text.append("div")
                .attr("class","text-line computer");

  eqp_computer.append("div")
          .attr("class","text-line-left")
          .append("span")
          .attr("class","title-text")
          .text("设备:");

  eqp_computer.append("div")
          .attr("class","text-line-right")
          .append("span")
          .text(function(d,i){return d['computer'];});

*/
  
  
  var eqp_first_time = eqp_text.append("div")
                     .attr("class","text-line first_time");
 
  eqp_first_time.append("div")
                .attr("class","time-line-left")
                .append("span")
                .attr("class","title-text")
                .style("width","100%")
                .style("text-align","center")
                .style("display","block")
                .text("首次发现时间");
  
  eqp_first_time.append("div")
                .attr("class","time-line-right")
                .style("width","100%")
                .style("text-align","center")
                .style("display","block")
                .text(function(d,i){return d["first_time"];});
  
   var eqp_last_time = eqp_text.append("div")
                .attr("class","text-line last_time");
   
   eqp_last_time.append("div")
                .attr("class","time-line-left")
                .append("span")
                .attr("class","title-text")
                .style("width","100%")
                .style("text-align","center")
                .style("display","block")
                .text("最近发现时间");
  	         
   eqp_last_time.append("div")
                .attr("class","time-line-right")
                .style("width","100%")
                .style("text-align","center")
                .style("display","block")
                .text(function(d,i){return d["last_time"];});
  
   var auth=["授权","取消授权"];
   console.log(auth[0]);
   var eqp_button = one_eqp.append("button")
                          .attr("type","button")
                          .attr("class","btn")
                          .attr("id",function(d,i){return "btn_"+d['id']})
                          .style("text-align","center")
                          .text(function(d,i){return auth[d['authority']];});

  $(".btn").click(function(){
    var btn_id = this.id;
    //alert(btn_id);
    //get the number in btn_id
    var id = btn_id.slice(4);
    //alert(id);
    //get the top_id of the button
    var top_id = 'top_'+id;
    var socket = io.connect('http://' + wsCfg.host + ':' + wsCfg.port);

    if(document.getElementById(btn_id).innerHTML=="授权"){
      document.getElementById(btn_id).innerHTML="取消授权";
      //document.getElementById(top_id).css("background","#65c147");
      $("#"+top_id).css("background","#65c147");
      socket.emit("eqp_auth_click",{'eqp_id':id,'auth':1});
      //alert("success!")
     }
     else{
       document.getElementById(btn_id).innerHTML="授权";
      // document.getElementById(div_id).find('.top').css('background','#c33');
       $("#"+top_id).css("background","#c33");
       socket.emit("eqp_auth_click",{'eqp_id':id,'auth':0});
     }
  });

}