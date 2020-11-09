var url = "127.0.0.1:5000"

function verifyLogin(){

    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    httpGet();

}

function aCallback(response){
    alert(response);
}

function httpGet()
{
    alert("test");
    var key;
    var request = new XMLHttpRequest();
    var token_;
    request.open("POST", "/auth/login", true);
    request.setRequestHeader("Content-type", "application/json");
    request.send("grant_type=client_credentials&client_id="+"admin"+"&"+"client_secret="+"pass"); // specify the credentials to receive the token on request
    request.onreadystatechange = function () {
        if (request.readyState == request.DONE) {
            var response = request.responseText;
            alert(response)
            var obj = JSON.parse(response);
            key = obj.access_token; //store the value of the accesstoken
            token_ = key; // store token in your global variable "token_" or you could simply return the value of the access token from the function
        }
    }
}