//Set global variables
//Using global objects as pseudo-namespaces
var table = {},
	anchors = {};

//Initializing function
$(function(){

	//Binding functions
	anchors.bind();

});

// Table Methods
table.even_odd = function(){
	$('table tr:odd').addClass('odd');
	$('table tr:even').addClass('even');
}

// Anchor Methods
anchors.bind = function(){
	$('a[href="#"]').bind('click', function(){ return false; });
	$('a.external, a[rel="external"]').each(function(e){
		var title = ($(this).attr('title')) ?  $(this).attr('title') : 'This link will take you to an external website in a new window';
		$(this).attr('target', '_blank').attr('title', title);
	});
}
