window.addEventListener("load",function createContent() {
    var data = pageItems;
    var container = document.getElementById("blockContent")
    var strToAppend = "";
    for (var i=0; i<data.length; i++) {
        switch(data[i]["class"]) {
          case "image":
            strToAppend += "<div class=\"text-white container-fluid h-auto text-center col-centered\" style=\"background-image: url(\'static/" + data[i]["path"] + "\'); background-size: cover; height: 400px !important; position: relative;\">";
            if (data[i]["overlay"] != null){
              strToAppend += data[i]["overlay"]["content"];
            }
            strToAppend += "</div>";
            container.innerHTML += strToAppend;
            break;
          case "50:50-split":
            strToAppend = "<div class=\"container\"><div class=\"row\"><div class=\"col-6\">" + data[i]["leftSplit"] + "</div><div class=\"col-6\">" + data[i]["rightSplit"] + "</div></div></div>";
            container.innerHTML += strToAppend;
            break;
        }
    }
  }, false);