window.addEventListener("load",function createNav() {
    $.ajax({
      url: "static/staticLink/navbar.json",
      dataType: "json",
      success: function(data) {
        var nav = document.getElementById("navbar")
        var foot = document.getElementById("footer")
        var strToAppend;
        for (var i=0; i<data.length; i++) {
            if (data[i]["url"] == window.location.pathname && data[i]["navbar"]["present"] == true) {
                for (var j=0; j<data[i]["navbar"]["items"].length; j++) {
                    strToAppend = '<li class=\"nav-item\"><a class=\"nav-link\" href=\"' + data[i]["navbar"]["items"][j]["url"] + '\">' + data[i]["navbar"]["items"][j]["name"] + '</a></li>'
                    nav.innerHTML += strToAppend;
                    strToAppend = '<li><a class="footer-Link" href="' + data[i]["navbar"]["items"][j]["url"] + '">' + data[i]["navbar"]["items"][j]["name"] + '</a></li>'
                    footer.innerHTML += strToAppend;
                }
            }
        }
      }
    })
  }, false);