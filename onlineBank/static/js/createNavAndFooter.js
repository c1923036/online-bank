window.addEventListener("load",function createNav() {
  var navData = navbarContents
  var footData = footerContents
  var nav = document.getElementById("navbar")
  var foot = document.getElementById("footer")
  var strToAppend;
  for (var i=0; i<navData.length; i++) {
    strToAppend = '<li class=\"nav-item\"><a class=\"nav-link\" href=\"' + navData[i]['url'] + '\">' + navData[i]['name'] + '</a></li>'
    nav.innerHTML += strToAppend;
  }
  for (var i=0; i<footData.length; i++) {
    strToAppend = '<li><a class="footer-Link" href="' + footData[i]['url'] + '">' + footData[i]['name'] + '</a></li>'
    footer.innerHTML += strToAppend;
  }
}, false);