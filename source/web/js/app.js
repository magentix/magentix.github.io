document.addEventListener("DOMContentLoaded",function(){
    var e=window.location.pathname.replace(/^\/|\/$/g,""),n=document.createElement("img");
    n.src="https://cdn.magentix.fr/mgx-ack-"+encodeURI(e||"root")+".png";
    n.alt="";
    document.body.appendChild(n)
},!1);