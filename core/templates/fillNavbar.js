
var text = "[{\"name\": \"home\",\"showOnNavbar\": false,\"navbarDetails\": []},{\"name\": \"Login\",\"showOnNavbar\": true,\"navbarDetails\": [{\"displayName\": \"Log In\", \"link\": \"/login\"}]}]"

window.onload = function createNav() {
    var data = JSON.parse(text);
    nav = $('<ul class="nav justify-content-end" id="navbar">');
    var strToAppend
    for (var i=0; i<data.length; i++) {
        if (data[i]["showOnNavbar"] == true) {
            for (var j=0; j<data[i]["navbarDetails"].length; j++) {
                strToAppend = "<li class=\"nav-item\"><a class=\"nav-link\" href=\"" + data[i]["navbarDetails"][j]["link"] + "\">" + data[i]["navbarDetails"][j]["displayName"] + "</a></li>"
                nav.append(strToAppend);
            }
        }
    }
};