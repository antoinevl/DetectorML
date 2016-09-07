function httpGet(theUrl){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function textDisplay(theUrl){
    var res = httpGet(theUrl);
    return res;
}

var url = document.URL
var detector_url = "http://146.169.47.251:8080/prediction?url="+url
alert(textDisplay(detector_url));
