window.addEventListener("load",function createNav() {
  var data = navbarContents
  var nav = document.getElementById("navbar")
  //var foot = document.getElementById("footer")
  var strToAppend;
  for (var i=0; i<data.length; i++) {
    strToAppend = '<li class=\"nav-item\"><a class=\"nav-link\" href=\"' + data[i]['url'] + '\">' + data[i]['name'] + '</a></li>'
    nav.innerHTML += strToAppend;
    //strToAppend = '<li><a class="footer-Link" href="' + data[i]["navbar"]["items"][j]["url"] + '">' + data[i]["navbar"]["items"][j]["name"] + '</a></li>'
    //footer.innerHTML += strToAppend;
  }
}, false);