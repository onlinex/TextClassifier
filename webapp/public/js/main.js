let AnimHandler = class {
    constructor() {
        this.book = $('#loading_animation')
        this.book.fadeOut(0); // fadout by default
        this.timeBlock = NaN
    }

    fadeIn() {
        // clear fadeout
        clearTimeout(this.timeBlock);
        //
        this.book.fadeIn();
    }

    fadeOut() {
        // timeout can be reverted by fadeIN
        this.timeBlock = setTimeout(() => {
            this.book.fadeOut();
        }, 800)
    }
}

animation_handler = new AnimHandler();

let Network = class {
    constructor() {
        this.stack = [];
        // interval requests
        setInterval(() => {
            // if requests
            if(this.stack.length > 0) {
                // get most recent
                let json = this.stack.pop();
                // clear everything else
                this.stack = [];
                // make request
                request(json)
            }
        }, 500);
    }

    add(json) {
        this.stack.push(json);
    }
}

let network = new Network();

$("#text").on("input", function() {
    // get request value
    let text = $("#text").val()
    // convert to json
    let json = JSON.stringify({ 
        text: text
    });
    // add to stack
    network.add(json);
});

function request(json) {
    animation_handler.fadeIn();
    // fetch request
    fetch("/query", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: json
    }).then(response => {
        // check for errors
        if(response.ok) {
            // decode json
            return response.json()
        } else {
            throw new Error(response.status, response.statusText);
        }
    }).then(json => {
        console.log(json) // debug information
        // set author's name
        $("#response").text(json['name']);

    }).catch(error => {
        console.log(error)
    }).finally(() => {
        animation_handler.fadeOut();
    });
}