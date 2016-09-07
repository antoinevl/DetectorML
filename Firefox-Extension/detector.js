function httpGet(theUrl){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function textDisplay(theUrl){
    var res = httpGet(theUrl);
    var type;
    var proba;
    if (res.search("benign") != -1){
        type = "benign";
    } else if (res.search("malicious") != -1){
        type = "malicious";
    } else {
		type = "error";
    }
    if (res.search("benign") != -1){
        type = "benign";
    } else if (res.search("malicious") != -1){
        type = "malicious";
    } else {
		type = "error";
    }
        
    return res;
}

var url = document.URL
var detector_url = "http://146.169.47.251:8080/prediction?url="+url
alert('Result: '+textDisplay(detector_url));
