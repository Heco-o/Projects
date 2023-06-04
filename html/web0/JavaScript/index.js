let SRender = katex.renderToString;

document.getElementById("button").onclick = function(){
  let exprStr = document.getElementById("in").value;
  let exprFn = numeric.parse(exprStr); // compile expression string into a function
  let expr = exprFn({}); // evaluate the function with an empty object for variables
  document.getElementById("Lab0").innerHTML = expr.toString();
  document.getElementById("Lab").innerHTML = SRender(numeric.prettyPrint(expr));
};