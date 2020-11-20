function newPost() {

    document.getElementById("postForm").classList.remove("d-none");
    document.getElementById("centerContent").innerHTML = "";
}

function viewPosts() {

    var numPosts = 10;
    var html = '<div class="list-group">';

    for (i = 0; i < numPosts; i++) {
        html +=
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

    html += '</div>';
    document.getElementById('centerContent').innerHTML = html;
    document.getElementById("postForm").classList.add("d-none");
}

function viewUsers() {

    let allUsers = getListOfUsers();

    allUsers.then(function (data) {
        //console.log(data);
        getWhoUserFollows(data['username']).then(function (data2) {
            generateViewUsersHTML(new Set(data['users']), data['username'], new Set(data2['users']));
        })
    })
}

function generateViewUsersHTML(users, theUser, whoUserFollows) {

    var html = '<ul class="list-group">';

    for (let user of users) {

        if(user === theUser) continue;

        if (!whoUserFollows.has(user)) {
            html +=
                '   <li class="list-group-item d-flex justify-content-between align-items-center">\n' +
                '       @' + user + '\n' +
                '       <button onclick="changeSubButton(this,\'' + theUser + "\',\'" + user + '\')" class ="btn btn-success">Subscribe</button>\n' +
                '   </li>';
        } else {

            html +=
                '   <li class="list-group-item d-flex justify-content-between align-items-center">\n' +
                '       @' + user + '\n' +
                '       <button onclick="changeSubButton(this,\'' + theUser + "\',\'" + user + '\')" class ="btn btn-danger">Unsubscribe</button>\n' +
                '   </li>';
        }
    }

    html += '</ul>'
    document.getElementById('centerContent').innerHTML = html;
    document.getElementById("postForm").classList.add("d-none");
}

function getListOfUsers() {

    return fetch(window.location.href.substr(0, window.location.href.indexOf('#')) + 'getallusers', {
        method: "GET",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function (response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem. Status code: ${response.status}');
            return;
        }
        return response.json();
    }).catch(function (error) {
        console.log("Fetch error: " + error);
    });
}

function getWhoUserFollows(username) {

    let urlStr = window.location.href.substr(0, window.location.href.indexOf('#')) + 'getwhouserfollows?username=' + username;
    return fetch(urlStr, {
        method: "GET",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function (response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem. Status code: ${response.status}');
            return;
        }
        return response.json();
    }).catch(function (error) {
        console.log("Fetch error: " + error);
    });
}

function followOrUnfollow(requester, target, willFollow) {

    let urlStr;
    let jsonBody;

    if (willFollow) {
        urlStr = window.location.href.substr(0, window.location.href.indexOf('#')) + 'follow';
        jsonBody = JSON.stringify({
            requester: requester,
            tofollow: target
        })
    } else {
        urlStr = window.location.href.substr(0, window.location.href.indexOf('#')) + 'unfollow';
        jsonBody = JSON.stringify({
            requester: requester,
            tounfollow: target
        })
    }

    return fetch(urlStr, {
        method: "POST",
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        }),
        body: jsonBody
    }).then(function (response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem. Status code: ${response.status}');
        }
        return response.status;
    }).catch(function (error) {
        console.log("Fetch error: " + error);
    });
}

function changeSubButton(source, requester, target) {

    if (source.classList.contains("btn-danger")) {

        followOrUnfollow(requester, target, false).then(function (httpResp) {
            if (httpResp === 200) {
                source.classList.remove("btn-danger");
                source.classList.add("btn-success");
                source.innerHTML = "Subscribe";
            }
        });

    } else {
        followOrUnfollow(requester, target, true).then(function (httpResp) {
            if (httpResp === 200) {
                source.classList.remove("btn-success");
                source.classList.add("btn-danger");
                source.innerHTML = "Unsubscribe";
            }
        });
    }
}

function viewFiles() {

    var html =
        '<div class="row">\n' +
        '   <div class="col-12 text-center">\n' +
        '       <button class="btn btn-primary mb-5"> Upload file</button>\n' +
        '   </div>\n' +
        '</div>' +
        '<ul class="list-group">';


    for (i = 0; i < 20; i++) {

        if (i < 5) {
            html +=
                '<li class="list-group-item d-flex justify-content-between align-items-center"> File title\n' +
                '<div>\n' +
                '   <button class="btn btn-success">download</button>\n' +
                '   <button class="btn btn-danger">delete</button>\n' +
                '</div>\n' +
                '</li>';
        } else {
            html +=
                '<li class="list-group-item d-flex justify-content-between align-items-center"> File title\n' +
                '<div>\n' +
                '   <button class="btn btn-success">download</button>\n' +
                '</div>\n' +
                '</li>';
        }
    }

    html += '</ul>';

    document.getElementById('centerContent').innerHTML = html;
    document.getElementById("postForm").classList.add("d-none");
}

