var AttackWS={
  createNew: function(inArg){
    var ret={};
    ret.host=inArg.host;
    ret.port=inArg.port||80;
    //ret.socket=io.connect('http://'+ret.host+":"+ret.port); 
    ret.socket=io.connect('http://'+ret.host+':'+ret.port); 
    ret.run=function(){
      ret.socket.on('connect', function(data){
        ret.socket.emit('client connect', {'client': 'connect'});
        console.log("connected!");
      });
    };
    ret.add=function(inArg){
      ret.socket.on(inArg.evt, inArg.hdler);
    };
    return ret;
  }
};
