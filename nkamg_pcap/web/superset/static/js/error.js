function dealErrorCode(){
  var errorJq=$("#error-main");
  var errorCode=parseInt(errorJq.text());
  var errorInfo=[];
  errorInfo['2']='您不应该来到这里';
  errorInfo['3']='对不起您没有访问权限';
  errorJq.text(errorInfo[errorCode]);
}
$(document).ready(function(){
  dealErrorCode();
});
