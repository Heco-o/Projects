function add(num){
	document.getElementById("iscreen").innerHTML = document.getElementById("iscreen").innerHTML + num;
}
function remove(){
	document.getElementById("iscreen").innerHTML = document.getElementById("iscreen").innerHTML.slice(0, -1);
}
function reset(){
	document.getElementById("iscreen").innerHTML = "";
}
function solve(){
	document.getElementById("iscreen").innerHTML = math.evaluate(document.getElementById("iscreen").innerHTML);
}