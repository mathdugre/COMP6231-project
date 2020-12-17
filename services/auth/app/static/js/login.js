function register() {

    let formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('password', document.getElementById('password').value);

    fetch(window.location.href + '/userFrontEnd', {
        method: "POST",
        body: formData,
    }).then(function (response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem. Status code: ${response.status}');
        }
        return response.json();
    }).then(function(json){
       alert(json['msg']);
    }).catch(function (error) {
        console.log("Fetch error: " + error);
    });

}