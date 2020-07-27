document.addEventListener('DOMContentLoaded', function () {


    //add event listener to the follow button
    if (document.getElementById('follow') !== null){
        document.getElementById('follow').addEventListener('click', follow)
    }

    //add event listener to the unfollow button
    if (document.getElementById('unfollow') !== null){
        document.getElementById('unfollow').addEventListener('click', unfollow)
    }
    
    //add click event to post new posts if user is logged in:
    if (document.getElementById('newPost') !== null){
        //if user is not logged in then load all posts only without displaying the compose form
        document.getElementById('newPost').addEventListener('click', createPost)
        // load_posts("getposts")
    }

});

function edit_post(id) {
    //onclick, reveal the hidden textarea content
    document.getElementById(`post_content_${id}`).style.display = 'block'
}

function save_post(id) {
    var body = document.getElementById(`update_content_${id}`).value
    console.log(body)

    fetch(`http://127.0.0.1:8000/update/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          content: body
        })
      })
    .then(response => response.text())
    .then(result => {
        console.log(result)
        $(`#post-${id}`).html(`
            ${body}
        `)
        document.getElementById(`post_content_${id}`).style.display = 'none'
    })    
}

function like(id){
    var like_counts = document.getElementById(`post_like_${id}`).getAttribute('data-count')
    // console.log(like_counts)
    //update like counts when button is clicked
    fetch(`http://127.0.0.1:8000/like/${id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result.count)
        $(`#post_like_${id}`).html(`
            ${result.count}
        `)

    })
}

function createPost(event) {
    event.preventDefault()
    var body = document.querySelector('#compose-body').value;
    //make sure the body field is not empty.
    if (body == 0) {
        $(`#warning-view`).html(`
        <div class="alert alert-danger" role="alert">
            Cannot create empty post
        </div>
        `)
        return false
    }
    else{

        //send the post request to '/emails'
        fetch('http://127.0.0.1:8000/compose', {
            method: 'POST',
            body: JSON.stringify({
                //   userID: userID,
                body: body
            })
        })
        .then(response => response.json())
        .then(result => {
            //Print result
            console.log(result);
            $(`#warning-view`).html(`
            <div class="alert alert-success" role="alert">
                Successfully created post
            </div>
            `)
            location.reload()  
        })
    }
    
}

function follow(event){
    event.preventDefault()
    //when the button is clicked, add the current profile's page into the current logged in user's following list
    //get the current page user id
    id = document.getElementById('follow').value

    fetch(`http://127.0.0.1:8000/following/${id}`)
    .then(response => response.json())
    .then(result => {
        code = parseInt(result.code)
        if (code == 1) {
            $('#message-view').html(
                `<div class="alert alert-warning" role="alert">
                    You are already following this user
                </div>`
            )
        }else if (code == 2) {
            $('#message-view').html(
                `<div class="alert alert-success" role="alert">
                    You are now following this user
                </div>`
            )
        }

    })

}

function unfollow(event){
    event.preventDefault()
    id = document.getElementById('unfollow').value

    fetch(`http://127.0.0.1:8000/unfollow/${id}`)
    .then(response => response.json())
    .then(result => {
        code = parseInt(result.code)
        if (code == 4) {
            $('#message-view').html(
                `<div class="alert alert-dark" role="alert">
                    You are not following this user
                </div>`
            )
        }else if (code == 3) {
            $('#message-view').html(
                `<div class="alert alert-info" role="alert">
                    You have successfully unfollowed this user
                </div>`
            )
        }
    })
}
