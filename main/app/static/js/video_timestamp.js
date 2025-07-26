document.getElementById("timestampBtn").addEventListener("click", function() {
    var video = document.getElementById("lesson_video");
    var currentTime = video.currentTime;

    // Using the Fetch API to send the data to the Flask server
    fetch(currentURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'timestamp': currentTime, posttype: 'timestamp' })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("status").innerText = data.message;
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});