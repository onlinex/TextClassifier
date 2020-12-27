$("#send_text").on("click", function() {

    // get request value
    let text = $("#text").val()

    fetch("/query", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ 
            text: text
        })
    }).then(response => {
        // check for errors
        if(response.ok) {
            // decode json
            return response.json()
        } else {
            throw new Error(response.status, response.statusText);
        }
    }).then(json => {
        console.log(json);

        // json['name'], json['confidence]

        $("#response").text(json['name']);

    }).catch(error => {
        console.log(error)
    });
});