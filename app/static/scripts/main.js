var diaper_form = document.getElementById('diaper_form');
var diaper_type = document.getElementsByName('diaper_type');
var diaper_size = document.getElementsByName('diaper_size');
var bottle_slider = document.getElementById('bottle-slider');
var bottle_form = document.getElementById('bottle_form');
var diaper_list = document.getElementById('diaperList');
var bottle_list = document.getElementById('bottleList');
var childID = 1;


function bottleDeleteClicked(e){
	var key = e.id;
    $.post("/delete_bottle", {id: key});
    location.reload();
}	


function diaperDeleteClicked(e){
	var key = e.id;
    $.post("/delete_diaper", {id: key});
    location.reload();
}	


function logDiaper(child, type, size){
	var diaperData = {
		child: child,
		type: type,
		size: size,
		date: Math.round(new Date().getTime()/1000.0)
	}
	var newDiaperKey = firebase.database().ref().child('diapers').push().key;
	var updates = {};
	updates['/diapers/' + child + '/' + newDiaperKey] = diaperData;
	return firebase.database().ref().update(updates);
}

function logBottle(child, amount){
	var bottleData = {
		child: child,
		amount: amount,
		date: Math.round(new Date().getTime()/1000.0)
	};
	var newBottleKey = firebase.database().ref().child('bottles').push().key;
	var updates = {};
	updates['/bottles/' + child + '/' + newBottleKey] = bottleData;
	return firebase.database().ref().update(updates);
}

function getRadioValue(options){
	var radioVal = undefined;
	for (var i = 0; i < options.length; i++) {
		if(options[i].checked){
			radioVal = options[i].value;
		}
	}
	return radioVal;
}
  
window.addEventListener('load', function() {
}, false);
