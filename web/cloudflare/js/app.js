document.addEventListener("DOMContentLoaded",function(){
    var l=window.location,e=(l.pathname+encodeURIComponent(l.search)).replace(/^\/|\/$/g,"");
    var n=document.createElement("img");
    n.src="https://cdn.magentix.fr/mgx-ack-"+encodeURI(e||"root")+".png";
    n.style.display = "none";
    n.alt="";
    document.body.appendChild(n);
},!1);