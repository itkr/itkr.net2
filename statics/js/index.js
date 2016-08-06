(function(global, document) {
	var $ = function(id) {
		return document.getElementById(id);
	};
	var changeImage = function() {
		var files = [
			'top1.jpg',
			'top2.jpg'
		];
		var file = files[Math.floor(Math.random() * files.length)];
		$('layout-main').style.backgroundImage = 'url(/static/img/photo/top/' + file
				+ ')';
	};
	global.onload = changeImage;
})(this, this.document);