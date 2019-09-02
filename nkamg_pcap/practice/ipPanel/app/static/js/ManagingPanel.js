queue()
	.defer(d3.json, 'data')
	.await(upgradeblocks)

var regex = /^(\d|\d\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|\d\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|\d\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|\d\d|1\d\d|2[0-4]\d|25[0-5])$/;
function IP2int(ip) {                                            
	var result = regex.exec(ip);
	if (result == null) return -1;
	return (parseInt(result[1]) << 24 | parseInt(result[2]) << 16 | parseInt(result[3]) << 8 | parseInt(result[4]));
}

var ip_dict = new Array();
var mask;
var groups;

function hideall() {
	$('.block').css({'display':'none'});
	//$('.navitem').removeClass('active');
}
function showall() {
	$('.block').css({'display':'block'});
	//$('.navitem').removeClass('active');
	//$('#navshowall').addClass('active');
}
function showtab(group) {
	$('.tab'+group).css({'display':'block'});
	//$('#nav'+group).addClass('active');
}
function changetab(group) {
	hideall();showtab(group);
}
function changetabrecursive(treenode) {
	if(treenode.nodes===undefined) {
		for(var i in groups) {
			if(groups[i] === treenode.text) {
				showtab(i);
			}
		}
	} else {
		for(var i in treenode.nodes) {
			changetabrecursive(treenode.nodes[i]);
		}
	}
}

function addblock(ipint) {
	var block = $('<div></div>');
	block.addClass('block').addClass('col-xs-6 col-sm-4 col-md-3 col-lg-2');
	block.append($('<div></div>').addClass("innerblock innerblock-grey"));
	var innerblock = block.children('.innerblock').eq(0);

	innerblock.attr('id', 'inner'+ipint);
	innerblock.append($('<div></div>').addClass("innerblockhead").text(ipint&255));
	innerblock.append($('<div></div>').addClass("innerblockbody"));
	var ipgroup = ipint & mask;
	if(!(ipgroup in ip_dict)) {
		var groupname = groups[ipgroup];
		if(groupname===undefined){
			if(ip_dict[-1] === undefined){
				ip_dict[-1]=[ipint];
				$('#navcol').append($('<li></li>').addClass('navitem').attr('id', 'nav-1').append('<a onclick="changetab(' + -1 + ')">' + groups[-1] + '</a>'));
			}
			ip_dict[-1].push(ipint);
			ipgroup = -1;
		} else {
			ip_dict[ipgroup] = [ipint];
			//$('#navcol').append($('<li></li>').addClass('navitem').attr('id', 'nav'+ipgroup).append('<a onclick="changetab(' + ipgroup + ')">' + groupname + '</a>'));
		}
	} else {
		ip_dict[ipgroup].push(ipint); 
	}
	block.addClass("tab" + ipgroup);
	block.attr('id',ipint);
	var blockbody = innerblock.children('.innerblockbody').eq(0).append('<div class="row"></div>');
	blockbody.append ('<div class="row"><div class="col-xs-2 col-sm-2 text-left"><b>MAC</b></div><div class="col-xs-9 col-sm-9 text-right">'+'</div></div>');
	blockbody.append ('<div class="row"><div class="col-xs-2 col-sm-2 text-left"><b>IP</b></div><div class="col-xs-9 col-sm-9 text-right">'+(ipint>>>24)+'.'+(ipint>>>16&255)+'.'+(ipint>>>8&255)+'.'+(ipint&255)+'</div></div>');
	blockbody.append ('<div class="row"><div class="col-xs-4 col-sm-4 text-left"><b>Software</b></div><div class="col-xs-7 col-sm-7 text-right">'+'</div></div>');
	$('#blocks').append(block);
}

function upgradeblocks(error, responseJson) {
	var iplist = responseJson;                      

	// 解析掩码
	mask = ((-1) << iplist.maskbits);

	// 解析组名
	groups = new Array();
	for (var groupname in iplist.groupnames) {
		groups[IP2int(groupname)] = iplist.groupnames[groupname];
	}
	
	// 解析组层次
	$('#tree').treeview({data: [iplist.grouptree], color: '#337ab7'});
	$('#tree').on('nodeSelected', function(event, node){
		hideall();
		changetabrecursive(node);
	});

	// 解析传来数据中的固定范围
	for (var i in iplist.ipranges) {
		var begin = IP2int(iplist.ipranges[i].beginip);
		var end = IP2int(iplist.ipranges[i].endip);
		for (var i = begin; i <= end; ++i) {
			addblock(i);
		}
	}

	// 解析传来数据中的活跃数据
	for (var i in iplist.list) {
		var ipint = IP2int(iplist.list[i].src_ip);
		if (ipint == -1) continue;
		var innerblock = $('#inner' + ipint);
		if (innerblock.length == 0) {
			addblock(ipint);
		}
		$('#inner' + ipint).removeClass('innerblock-grey').addClass('innerblock-green');
	}
}

