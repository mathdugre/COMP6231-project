function newPostView() {
    document.getElementById("postForm").classList.remove("d-none");
    document.getElementById("centerContent").innerHTML = "";
}

function newPost() {

    let formData = new FormData();
    formData.append('title', document.getElementById("title").value);
    formData.append('message', document.getElementById("message").value);

    fetch(window.location.href.substr(0, window.location.href.indexOf('#')) + 'newpost', {
        method: "POST",
        body: formData,
    }).then(function (response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem. Status code: ${response.status}');
        }
        return response.json();
    }).then(function (json) {
        alert("post created: " + JSON.stringify(json));
    }).catch(function (error) {
        console.log("Fetch error: " + error);
    });
}

function viewPosts() {

    posts = getUserPosts();
    posts.then(function (userposts) {
        let numPosts = userposts.length
        let html = '<div class="list-group">';
        for (let i = 0; i < numPosts; i = i + 6) {

            let username = "@" + userposts[i + 3] + ": ";
            let message = userposts[i + 1];
            let title = userposts[i + 2];
            let timeInSec = userposts[i];
            let time = new Date(0); // The 0 there is the key, which sets the date to the epoch
            let postScore = userposts[i + 4]
            let postID = userposts[i + 5];
            time.setUTCSeconds(timeInSec);

            html += `
                       <div class="list-group-item flex-column align-items-start">
                       <div class="d-flex w-100 justify-content-between">
                           <h5 class="mb-1"> ` + username + title + `</h5>
                           <b class="w-25 text-right" id="postscorewithID` + postID + `">` + postScore + ` points</b>
                       </div> 
                       <div class="d-flex w-100 justify-content-between"> 
                           <p class="mb-1 w-75">` + message + `</p> 
                           <div> 
                               <div class="btn btn-success" onclick="vote('upvote','` + postID + `'); return false;"> /\\ </div> 
                               <div class="btn btn-danger" onclick="vote('downvote','` + postID + `'); return false" > \\/ </div> 
                           </div> 
                        </div> 
                       <small> ` + time + `</small> 
                       </div>`

        }
        html += '</div>';
        document.getElementById('centerContent').innerHTML = html;
        document.getElementById("postForm").classList.add("d-none");

        setPostScoreColors();
    });
}

function vote(upOrDown, postID) {

    let formData = new FormData();

    formData.append("postID", postID);
    formData.append("vote", upOrDown);

    fetch(window.location.href.substr(0, window.location.href.indexOf('#')) + 'vote', {
        method: "POST",
        body: formData,
    }).then(function (response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem. Status code: ${response.status}');
            return;
        }
        viewPosts();
    }).catch(function (error) {
        console.log("Fetch error: " + error);
    });

}

function setPostScoreColors() {

    getUserPostScores().then(function (scores) {

        for (let postID in scores) {

            if (scores.hasOwnProperty(postID)) {

                let domID = "postscorewithID" + postID;

                if (scores[postID] === '1') {

                    document.getElementById(domID).style.color = "green";

                } else if (scores[postID] === '0') {

                    document.getElementById(domID).style.color = "black";

                } else if (scores[postID] === '-1') {

                    document.getElementById(domID).style.color = "red";

                }
            }
        }
    })
}

function getUserPostScores() {

    return fetch(window.location.href.substr(0, window.location.href.indexOf('#')) + 'getuservotes', {
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

function getUserPosts() {

    return fetch(window.location.href.substr(0, window.location.href.indexOf('#')) + 'getposts', {
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

    for (let user of whoUserFollows) {

        html +=
            '   <li class="list-group-item d-flex justify-content-between align-items-center">\n' +
            '       @' + user + '\n' +
            '       <button onclick="changeSubButton(this,\'' + theUser + "\',\'" + user + '\')" class ="btn btn-danger">Unsubscribe</button>\n' +
            '   </li>';
    }

    for (let user of users) {

        if (user === theUser) continue;

        if (!whoUserFollows.has(user)) {
            html +=
                '   <li class="list-group-item d-flex justify-content-between align-items-center">\n' +
                '       @' + user + '\n' +
                '       <button onclick="changeSubButton(this,\'' + theUser + "\',\'" + user + '\')" class ="btn btn-success">Subscribe</button>\n' +
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

    let filenames = getFileNames();

    var html =
        '<div class = "col-12 text-center mb-5"> ' +
        '      <form action="" method="" enctype="">' +
        '        <div class="form-group">' +
        '          <div class="custom-file">' +
        '            <input type="file" class="custom-file-input" name="fileUpload" id="fileUpload">' +
        '            <label class="custom-file-label" for="fileUpload">Select file to upload...</label>' +
        '          </div>' +
        '        </div>' +
        '        <button type="" onclick="uploadFile(); return false;" class="btn btn-primary">Upload</button>' +
        '      </form>' +
        '</div>' +
        '<ul class="list-group">';

    filenames.then(function (files) {
        let allFiles = files['allFiles'];
        let userFiles = new Set(files['userFiles']);
        let baseURL = window.location.href.substr(0, window.location.href.indexOf('#'));
        for (let fileName of userFiles) {
            html +=
                '<li class="list-group-item d-flex justify-content-between align-items-center">' +
                '   <div class = "w-75 text-truncate">' +
                fileName + '' +
                '   </div>' +
                '   <div>' +
                '       <form action="' + baseURL + 'download" method="get">' +
                '           <input type ="hidden" name="filename" value="' + fileName + '">' +
                '           <button type="submit" class="btn btn-success">download</button>' +
                '<button type="button" onclick="deleteFile(\'' + fileName + '\')" class="btn btn-danger ml-1">delete</button>' +
                '       </form>' +
                '   </div>' +
                '</li>';
        }

        for (let i = 0; i < allFiles.length; i++) {
            if (!userFiles.has(allFiles[i])) {
                html +=
                    '<li class="list-group-item d-flex justify-content-between align-items-center">' +
                    '   <div class = "w-75 text-truncate">' +
                            allFiles[i] + '' +
                    '   </div>' +
                    '<div>' +
                    '       <form action="' + baseURL + 'download" method="get">' +
                    '       <input type ="hidden" name="filename" value="' + allFiles[i] + '">' +
                    '       <button type="submit" class="btn btn-success">download</button>' +
                    '   </form>' +
                    '</div>' +
                    '</li>';
            }
        }
        html += '</ul>';

        document.getElementById('centerContent').innerHTML = html;
        document.getElementById("postForm").classList.add("d-none");
    });


}

function getFileNames() {

    return fetch(window.location.href.substr(0, window.location.href.indexOf('#')) + 'getfilenames', {
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

function uploadFile() {

    const file = document.getElementById('fileUpload').files[0];
    let formData = new FormData();

    formData.append('fileUpload', file)

    fetch(window.location.href.substr(0, window.location.href.indexOf('#')) + 'upload', {
        method: "POST",
        body: formData,
    }).then(function (response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem. Status code: ${response.status}');
        }
        return response.json();
    }).then(function (json) {
        alert(JSON.stringify(json));
        viewFiles();
    }).catch(function (error) {
        console.log("Fetch error: " + error);
    });

}

function deleteFile(fileName) {

    return fetch(window.location.href.substr(0, window.location.href.indexOf('#')) + 'deletefile?filename=' + fileName, {
        method: "GET",
        cache: "no-cache",
    }).then(function (response) {
        if (response.status !== 200) {
            console.log('Looks like there was a problem. Status code: ${response.status}');
        }
        return response.json();
    }).then(function (json) {
        alert(JSON.stringify(json));
        viewFiles();
    }).catch(function (error) {
        console.log("Fetch error: " + error);
    });
}

function downloadFile(fileName) {
    return fetch(window.location.href.substr(0, window.location.href.indexOf('#')) + 'download?filename=' + fileName, {
        method: "GET",
        cache: "no-cache",
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