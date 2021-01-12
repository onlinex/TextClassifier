window.onload = () => {
    genres = ['Adventure', 'Crime', 'Fantasy', 'Fiction', 'Novel', 'Satire', 'Science']
    periods = ['Unknown', 'Renaissance', 'Enlightenment', 'Victorian', 'Modernism', 'Post-modernism']


    renderGenreChart(Object.assign({}, ...genres.map(x => ({[x]: 0.0}))));
    renderPeriodChart(Object.assign({}, ...periods.map(x => ({[x]: 0.0}))));

    animation_handler.bookAnim(true);
}

let AnimHandler = class {
    constructor() {
        this.book = $('#loading_animation');
        this.info = $('#author_info');

        this.info.fadeTo(0, 0);
        this.book.fadeTo(0, 1);

        this.bookAnim(false);
    }

    fadeIn() {
        // remove info
        this.info.stop().fadeTo(100, 0).delay(100);
        // set book
        this.book.stop().fadeTo(100, 1);
    }

    fadeOut() {
        // remove book
        this.book.stop().fadeTo(120, 0).delay(120).queue(() => {
            // set info   
            this.info.stop().fadeTo(100, 1);
        });
    }

    bookAnim(flag=true) {
        let state = (flag ? 'running' : 'paused');

        this.book.children().children().css('-webkit-animation-play-state', state);
        this.book.children().children().css('-animation-play-state', state);
    }
}

animation_handler = new AnimHandler();


$("#text").on("input", function() {
    // get request value
    let text = $("#text").val()
    // if empty, stop
    if(text.length == 0) {
        network.clear();
        return
    };
    // convert to json
    let json = JSON.stringify({ 
        text: text
    });
    // add to stack
    network.add(json);
});


let Network = class {
    // damper function, 500 ms
    add(json) {
        clearTimeout(this.timeBlock);

        this.timeBlock = setTimeout(() => {
            request(json)
        }, 700)
    }

    clear() {
        clearTimeout(this.timeBlock);
    }
}

let network = new Network();


function request(data) {
    animation_handler.fadeIn();
    // fetch request
    fetch("/query", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: data
    }).then(response => {
        // check for errors
        if(response.ok) {
            // decode json
            return response.json()
        } else {
            throw new Error(response.status, response.statusText);
        }
    }).then(json => {
        //console.log(json) // debug information
        
        // set author's name
        $("#response").text(json['name']);
        // set confidence level
        setTimeout(() => {
            setNumbers(parseFloat(json['confidence']) * 100);
            renderGenreChart(json['genres']);
            renderPeriodChart(json['periods']);
        }, 85)
        // set image
        $("#thumbnail").attr("src", json['img_src']);

    }).catch(error => {
        console.log(error)
    }).finally(() => {
        //
    });
}

document.getElementById('thumbnail').addEventListener('load', () => {
    // end animation when the picture is loaded
    animation_handler.fadeOut();
})