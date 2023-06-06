document.addEventListener("DOMContentLoaded", function () {
		document.querySelectorAll("th, td").forEach(function (element) {
			katex.render(element.innerHTML, element);
		});
	});