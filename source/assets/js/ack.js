document.addEventListener("DOMContentLoaded", function() {
    var location = window.location;
    var page = (location.pathname + encodeURIComponent(location.search)).replace(/^\/|\/$/g, "");
    var request = new XMLHttpRequest();
    request.open('POST', 'https://api.magentix.fr/ack/');
    request.send(JSON.stringify({"uuid":"mgx","sandbox":false,"page":page}));
});