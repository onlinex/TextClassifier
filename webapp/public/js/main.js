$("#send_text").on("click", function() {

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
        console.log(response.status);
    }).catch(error => {
        console.log(error)
    });
});