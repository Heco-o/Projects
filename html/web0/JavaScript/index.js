document.getElementById("button").onclick = function(){
	document.getElementById("Lab").innerHTML = katex.renderToString(math.simplify(document.getElementById("in").value).toTex());
};