function newPost(){

    document.getElementById("postForm").classList.remove("d-none");
    document.getElementById("centerContent").innerHTML = "";

}

function viewPosts() {


    var numPosts = 10;
    var http = '<div class="list-group">';

    for (i = 0; i < numPosts; i++) {
        http +=
            '       <div class="list-group-item flex-column align-items-start">\n' +
            '       <div class="d-flex w-100 justify-content-between">\n' +
            '           <h5 class="mb-1">@username: Post title</h5>\n' +
            '           <small>45 points</small>\n' +
            '       </div>\n' +
            '       <div class="d-flex w-100 justify-content-between">\n' +
            '           <p class="mb-1">This is where the text post does</p>\n' +
            '           <div>' +
            '               <div class="btn btn-success"> /\\ </div>' +
            '               <div class="btn btn-danger"> \\/ </div>' +
            '           </div>' +
            '        </div>' +
            '       <small> 3 days ago. Associated files</small>\n' +
            '       </div>';

    }

    http += '</div>';
    document.getElementById('centerContent').innerHTML = http;
    document.getElementById("postForm").classList.add("d-none");
}

function viewUsers() {

    var http = '<ul class="list-group">';

    for(i = 0 ; i < 20 ; i++){

        if(i < 10) {
            http +=
                '   <li class="list-group-item d-flex justify-content-between align-items-center">\n' +
                '       @Username\n' +
                '       <button onclick="changeSubButton(this)" class ="btn btn-success">Subscribe</button>\n' +
                '   </li>';
        } else {

            http +=
                '   <li class="list-group-item d-flex justify-content-between align-items-center">\n' +
                '       @Username\n' +
                '       <button onclick="changeSubButton(this)" class ="btn btn-danger">Unsubscribe</button>\n' +
                '   </li>';
        }
    }

    http += '</ul>'
    document.getElementById('centerContent').innerHTML = http;
    document.getElementById("postForm").classList.add("d-none");
}

function changeSubButton(source){

    if(source.classList.contains("btn-danger")) {
        source.classList.remove("btn-danger");
        source.classList.add("btn-success");
        source.innerHTML = "Subscribe";
    } else {
        source.classList.remove("btn-success");
        source.classList.add("btn-danger");
        source.innerHTML = "Unsubscribe";
    }
}

