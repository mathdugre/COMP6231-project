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
}
