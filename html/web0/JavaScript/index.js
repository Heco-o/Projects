document.getElementById("button").onclick = function(){
	let expr = new algebra.parse(document.getElementById("in").value);
	document.getElementById("Lab").innerHTML = katex.renderToString(algebra.toTex(expr).toString());
};