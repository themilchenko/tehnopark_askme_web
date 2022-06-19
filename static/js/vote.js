function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

$(".button-like").on('click', function (ev) {
    const $this = $(this);

    var type = $this[0]['classList'][1];
    var body_str = 'type=' + type + '&question_id=' + $this.data('id') + '&vote=0'

    const request = new Request(
        'http://127.0.0.1:8000/vote/',
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: body_str
        }
    );

    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            $this.text(parsed.current_likes);
            $(".button-dislike").text(parsed.current_dislikes);
        });
    })
})

$(".button-dislike").on('click', function (ev) {
    const $this = $(this);

    var type = $this[0]['classList'][1];
    var body_str = 'type=' + type + '&question_id=' + $this.data('id') + '&vote=1'

    const request = new Request(
        'http://127.0.0.1:8000/vote/',
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: body_str
        }
    );

    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            $this.text(parsed.current_dislikes);
            $(".button-like").text(parsed.current_likes);
        }); 
    })
})