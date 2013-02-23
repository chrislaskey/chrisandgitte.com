//Set global variables
//Using global objects as pseudo-namespaces
var mobile = {};
var table = {};

//Initializing function
$(function(){

	//Binding functions
	mobile.bind_responsive_toggle();

});

// Mobile Methods
mobile.bind_responsive_toggle = function(){
	$('a.is_responsive').on('click', function(){
		var cookie = $.cookie('is_responsive');
		if( cookie == null || cookie == 'true' ){
			$.cookie('is_responsive', 'false', { expires: 7, path: '/' });
		}else{
			$.cookie('is_responsive', 'true', { expires: 7, path: '/' });
		}
		document.location.reload(true);
		return false;
	});
}

// Table Methods
table.even_odd = function(){
	$('table tr:odd').addClass('odd');
	$('table tr:even').addClass('even');
}
