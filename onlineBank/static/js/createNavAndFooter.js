function createNav() {
    var navData = navbarContents
    var footData = footerContents
    var colour = getSyncScriptParams();
    var nav = document.getElementById("navbar")
    var foot = document.getElementById("footer")
    var strToAppend;
    for (var i = 0; i < navData.length; i++) {
        strToAppend = '<li class=\"nav-item\"><a class=\"nav-link\" style=\"color:' + colour + '\" href=\"' + navData[i]['url'] + '\">' + navData[i]['name'] + '</a></li>'
        nav.innerHTML += strToAppend;
    }
    for (var i = 0; i < footData.length; i++) {
        strToAppend = '<li><a class="footer-Link" href="' + footData[i]['url'] + '">' + footData[i]['name'] + '</a></li>'
        footer.innerHTML += strToAppend;
    }
};

function getSyncScriptParams() { //https://stackoverflow.com/questions/5292372/how-to-pass-parameters-to-a-script-tag - 24/01/2022
    var scripts = document.getElementsByTagName('script');
    var lastScript = scripts[scripts.length - 1];
    var scriptName = lastScript;
    var font_colour = scriptName.getAttribute('font_colour')
    return font_colour
}