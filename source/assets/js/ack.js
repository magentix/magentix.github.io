var api = {
    "protocol": "https",
    "name": "api",
    "domain": "magentix.fr"
};
var apiUrl = api.protocol + '://' + api.name + "." + api.domain + "/";
document.addEventListener("DOMContentLoaded", function() {
    var location = window.location;
    var page = (location.pathname + encodeURIComponent(location.search)).replace(/^\/|\/$/g, "");
    var request = new XMLHttpRequest();
    request.open('POST', apiUrl + 'ack/');
    request.send(JSON.stringify({"uuid":"mgx","page":page}));
});