window.onload = () => {
    renderChart(
        {'Drama': 0.0, 'Novel': 0.0, 'Phylosophy': 0.0}
    );
}

let AnimHandler = class {
    constructor() {
        this.book = $('#loading_animation');
        this.info = $('#author_info');

        this.info.fadeTo('fast', 0);
        this.book.fadeTo('fast', 1);
    }

    fadeIn() {
        // remove info
        this.info.stop().fadeTo(85, 0).delay(85);
        // set book
        this.book.stop().fadeTo(85, 1);
    }

    fadeOut() {
        // remove book
        this.book.stop().fadeTo(120, 0).delay(120).queue(() => {
            // set info   
            this.info.stop().fadeTo(85, 1);
        });
    }
}

animation_handler = new AnimHandler();


$("#text").on("input", function() {
    // get request value
    let text = $("#text").val()
    // if empty, stop
    if(text.length == 0) return;
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
            renderChart(json['style'])
        }, 85)
        // set image
        $("#thumbnail").attr("src", json['img_src']);

    }).catch(error => {
        console.log(error)
    }).finally(() => {
        // fade if there is nothing to print
        animation_handler.fadeOut();
    });
}