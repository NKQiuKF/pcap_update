var WebSocketServer = require('websocket').server;
var http = require('http');


var points = [{
  latitude: 32.06,
  longitude: -88.78,
  countrycode: "US",
  country: "US",
  city: "Arkansas",
  org: "PoizonBOx",
  md5: "222.186.221.60"
},
  {
    latitude: 39.43,
    longitude: -104.00,
    countrycode: "US",
    country: "US",
    city: "Denver",
    org: "PoizonBOx",
    md5: "111.111.111.111"
  },
  {
    latitude: 40.43,
    longitude: -74.00,
    countrycode: "US",
    country: "US",
    city: "New York",
    org: "PoizonBOx",
    md5: "222.222.222.222"
  },
  {
    latitude: 32.13,
    longitude: -110.58,
    countrycode: "US",
    country: "US",
    city: "Tucson",
    org: "PoizonBOx",
    md5: "333.333.333.333"
  },
  {
    latitude: 39.55,
    longitude: 116.24,
    countrycode: "CN",
    country: "CN",
    city: "北京",
    org: "中国黑客联盟",
    md5: "444.444.444.444"
  },
  {
    latitude: 31.14,
    longitude: 121.29,
    countrycode: "CN",
    country: "CN",
    city: "上海",
    org: "中国鹰派联盟",
    md5: "555.555.555.555"
  },
  {
    latitude: 39.02,
    longitude: 117.12,
    countrycode: "CN",
    country: "CN",
    city: "天津",
    org: "H.U.C",
    md5: "666.666.666.666"
  }];

var attackTypes = [{
  name: "ftp",
  port: 21
}, {
  name: "ssh",
  port: 22
}, {
  name: "telnet",
  port: 23
}, {
  name: "smtp",
  port: 25
}, {
  name: "netbios-ns",
  port: 137
}, {
  name: "netbios-dgm",
  port: 138
}, {
  name: "netbios-ssn",
  port: 139
}, {
  name: "remote-as",
  port: 1053
}, {
  name: "brvread",
  port: 1054
}, {
  name: "ansyslmd",
  port: 1055
}, {
  name: "vfo",
  port: 1056
}, {
  name: "vpvc",
  port: 1519
}, {
  name: "atm-zip-office",
  port: 1520
}, {
  name: "ncube-lm",
  port: 1521
}];


// 对Date的扩展，将 Date 转化为指定格式的String
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
// 例子：
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
Date.prototype.Format = function (fmt) { //author: meizz
  var o = {
    "M+": this.getMonth() + 1,                 //月份
    "d+": this.getDate(),                    //日
    "h+": this.getHours(),                   //小时
    "m+": this.getMinutes(),                 //分
    "s+": this.getSeconds(),                 //秒
    "q+": Math.floor((this.getMonth() + 3) / 3), //季度
    "S": this.getMilliseconds()             //毫秒
  };
  if (/(y+)/.test(fmt))
    fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
  for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt))
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
  return fmt;
}

var server = http.createServer(function (request, response) {
  console.log(new Date().Format("yyyy-MM-dd hh:mm:ss") + ' Received request for ' + request.url);
  request.setEncoding('utf-8');
  var postData = ""; //POST & GET ： name=zzl&email=zzl@sina.com
  // 数据块接收中
  request.addListener("data", function (postDataChunk) {
    postData += postDataChunk;
  });
  // 数据接收完毕，执行回调函数
  request.addListener("end", function () {
    //console.log('receive:' + postData);
    response.writeHead(200, {
      "Content-Type": "text/plain;charset=utf-8"
    });
    wsServer.broadcastUTF(postData);
    response.end("0");
  });
});
server.listen(8000, function () {
  console.log(new Date().Format("yyyy-MM-dd hh:mm:ss") + ' Server is listening on port 8000');
});

wsServer = new WebSocketServer({
  httpServer: server,
  // You should not use autoAcceptConnections for production
  // applications, as it defeats all standard cross-origin protection
  // facilities built into the protocol and the browser.  You should
  // *always* verify the connection's origin and decide whether or not
  // to accept it.
  autoAcceptConnections: false
});

function originIsAllowed(origin) {
  // put logic here to detect whether the specified origin is allowed.
  return true;
}

wsServer.on('request', function (request) {
  if (!originIsAllowed(request.origin)) {
    // Make sure we only accept requests from an allowed origin
    request.reject();
    console.log(new Date().Format("yyyy-MM-dd hh:mm:ss") + ' Connection from origin ' + request.origin + ' rejected.');
    return;
  }

  var connection = request.accept('echo-protocol', request.origin);
  console.log((new Date()) + ' Connection accepted.');
  connection.on('message', function (message) {
    // if (message.type === 'utf8') {
    //     console.log('Received Message: ' + message.utf8Data);
    //     wsServer.broadcastUTF('{"latitude":"32.06","longitude":"88.78","countrycode":"CN","country":"CN","city":"Nanjing","org":"Chinanet Jiangsu Province Network","latitude2":"25.04","longitude2":"121.53","countrycode2":"TW","country2":"TW","city2":"Taipei","type":"ipviking.honey","md5":"222.186.2221.60","dport":"3128","svc":"3128","zerg":""}');
    //     //connection.sendUTF('{"latitude":"32.06","longitude":"118.78","countrycode":"CN","country":"CN","city":"Nanjing","org":"Chinanet Jiangsu Province Network","latitude2":"25.04","longitude2":"121.53","countrycode2":"TW","country2":"TW","city2":"Taipei","type":"ipviking.honey","md5":"222.186.21.60","dport":"3128","svc":"3128","zerg":""}');
    // }
    // else if (message.type === 'binary') {
    //     console.log('Received Binary Message of ' + message.binaryData.length + ' bytes');
    //     connection.sendBytes(message.binaryData);
    // }
  });
  connection.on('close', function (reasonCode, description) {
    console.log(new Date().Format("yyyy-MM-dd hh:mm:ss") + ' Peer ' + connection.remoteAddress + ' disconnected.');
  });
});

wsServer.on('atkSend', function(inData){
  console.log('wsServer.on atkSend');
  //console.log(inData);
  console.log(inData['json']);
  wsServer.broadcastUTF(inData['json']);
});



function getRandom(arr, exclude) {
  var num;
  do {
    num = Math.floor(Math.random() * arr.length);
  } while (num == exclude);
  return num;
}
//
// function newAttack() {
//     var srcIndex = getRandom(points);
//     var dstIndex = getRandom(points, srcIndex);
//     var srcObj = points[srcIndex];
//     var dstObj = points[dstIndex];
//     var attIndex = getRandom(attackTypes);
//     var attObj = attackTypes[attIndex];
//     var srcJson = '"latitude":"' + srcObj.latitude + '","longitude":"' + srcObj.longitude + '","countrycode":"' + srcObj.countrycode + '","country":"' + srcObj.country + '","city":"' + srcObj.city + '","org":"' + srcObj.org + '"';
//     var dstJson = '"latitude2":"' + dstObj.latitude + '","longitude2":"' + dstObj.longitude + '","countrycode2":"' + dstObj.countrycode + '","country2":"' + dstObj.country + '","city2":"' + dstObj.city + '"';
//     var json = '{' + srcJson + ',' + dstJson + ',"type":"' + attObj.name + '","md5":"' + srcObj.md5 + '","dport":"' + attObj.port + '","svc":"' + attObj.port + '","zerg":""}';
//     //console.log(json);
//     console.log(json);
//     wsServer.broadcastUTF(json);
// }

function sleep(numberMillis) {
  var now = new Date();
  var exitTime = now.getTime() + numberMillis;
  while (true) {
    now = new Date();
    if (now.getTime() > exitTime)
      return;
  }
}

// setInterval(function () {
//     var rnd = Math.random() * 5;
//     for (var i = 0; i < rnd; i++) {
//         newAttack();
//         sleep(100);
//     }
// }, 1000);

var lineReader = require('line-reader');
var configObj={
  timeWindow: 10*60,
  maxLineNum: 0,
  curLineNum: 0,

};




var mysql= require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : 'gbs1210605',
  database : 'mnt2'
});

var timeSpan=10000; 
connection.connect();


function readDb() {
  var nowDate = new Date();
  var nowSeconds = parseInt(nowDate.getTime() / 1000);
  var limitSeconds = nowSeconds - timeSpan;
  console.log(limitSeconds);
  connection.query('select * from `atkinfo2` where `atkTime` > ? ;', [limitSeconds], function (err, rows, fields) {
    console.log('hhhhiiiiiiihhhhhh');
    if (err) throw err;


    var len = rows.length;
    if (len == 0) {
      return;
    }
    var maxId = rows[len - 1].id + 1;
    connection.query('delete from `atkinfo2` where `id`< ? ;', [maxId], function () {
    });

    for (var i = 0; i < len; ++i) {
      console.log('aaaaaaaaaaaaaaaaaaaa');
      console.log(rows[i].id);
      rows[i].timeStamp = new Date(rows[i].atkTime * 1000).Format("yyyy-MM-dd hh:mm:ss");
      //rows[i].latitude=parseFloat(rows[i].srcLat).toString(); //need delete
      //rows[i].longitude=parseFloat(rows[i].srcLng).toString(); //need delete
      rows[i].latitude = rows[i].srcLat.toString();
      rows[i].longitude = rows[i].srcLng.toString();
      rows[i].countrycode = 'CN';
      rows[i].country = 'CN';
      rows[i].city = 10;
      rows[i].org = 10;
      //rows[i].latitude2=parseFloat(rows[i].dstLat).toString(); //need delete
      //rows[i].longitude2=parseFloat(rows[i].dstLng).toString(); //need delete
      rows[i].latitude2 = rows[i].dstLat.toString();
      rows[i].longitude2 = rows[i].dstLng.toString();
      rows[i].countrycode2 = 'CN';
      rows[i].country2 = 'CN';
      rows[i].city2 = 10;
      rows[i].org2 = 10;
      rows[i].type = rows[i].infos;
      rows[i].dport = rows[i].dstPort;
      rows[i].svc = rows[i].dstPort;
      rows[i].zerg = '';
      //there is trails
      rows[i].refs = rows[i].refer;
      rows[i].md5 = rows[i].srcIp;
      //there is srcIp
      //there is srcPort
      //there is dstIp
      //there is dstPort
      //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      rows[i].sensorId = rows[i].sensorNumber;
      rows[i].protocalA = rows[i].cmProtocal;
      rows[i].atkType = rows[i].infos;
      
      console.log('ggggggggggggggggggggggggggggggggg')
      console.log(rows[i]);
      delete(rows[i].srcLat);
      delete(rows[i].srcLng);
      delete(rows[i].dstLat);
      delete(rows[i].dstLng);
      delete(rows[i].atkId);
      delete(rows[i].atkTime);
      delete(rows[i].infos);
      //delete(rows[i].infos);
      
      console.log('fffffffffffffffffffffffffffffffff');
      console.log(rows[i]);
      //websocket data is a python dictionary transformed from json
      wsServer.emit('atkSend', {'json': JSON.stringify(rows[i])});
    }
  });
}





//connection.query('select * from `atkinfo2` where `atkTime` > ? ;', [limitSeconds], function(err, rows, fields) {



setInterval(function(){
  readDb();
}, 1000)



 
//connection.end();
