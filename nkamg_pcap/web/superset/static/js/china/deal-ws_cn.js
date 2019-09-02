var DealWS={
  createNew: function(inArg){

    var ret={};
    ret.planet=inArg.planet;
    ret.localws=AttackWS.createNew({
      //host: '192.168.0.85',
      host: wsCfg.host,
      port: wsCfg.port
    });

    ret.localws.run();
    return ret;
  }
};











