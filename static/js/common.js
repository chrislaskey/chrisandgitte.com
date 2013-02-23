//Set global variables
//Using global objects as pseudo-namespaces
var table = {};

//Initializing function
$(function(){

	//Binding functions
	mobile.bind_responsive_toggle();

});

// Table Methods
table.even_odd = function(){
	$('table tr:odd').addClass('odd');
	$('table tr:even').addClass('even');
}
