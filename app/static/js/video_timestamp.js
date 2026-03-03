window.addEventListener('DOMContentLoaded', () => {

    // Selecting elements of the page that will be used later on
    const video = document.getElementById('lesson_video');
    const segments = document.querySelectorAll('.transcript-segment');

    // setting currentActiveSegment to null initially. Will change if user highlights
    // a portion of the transcript
    let currentActiveSegment = null;
        
    // speed options
    document.getElementById('speed').onchange = e =>
        video.playbackRate = +e.target.value;

    const transcriptContainer = document.getElementById('transcript-container');

    // listen for when the video's timestamp changes
    video.addEventListener('timeupdate', () => {
        // get the video's current time in seconds
        const currentTime = video.currentTime;
        let activeSegment = null;

        // Find the segment that should be active at the current time
        // This loop finds the *last* segment whose timestamp is before the current video time
        for (let i = 0; i < segments.length; i++) {
            const segmentTimestamp = parseFloat(segments[i].getAttribute('data-timestamp'));
            if (segmentTimestamp <= currentTime) {
                activeSegment = segments[i];
            } else {
                // Since segments are ordered by time, we can stop once we pass the current time
                break;
            }
        }
        
        // If we found an active segment and it's different from the currently active one
        if (activeSegment && activeSegment !== currentActiveSegment) {
            
            // Remove 'active' class from the previous segment (if there was one)
            if (currentActiveSegment) {
                currentActiveSegment.classList.remove('active');
                currentActiveSegment.classList.remove('video-active');
            }

            // Add 'active' class to the new segment
            activeSegment.classList.add('active');
            activeSegment.classList.add('video-active');
            currentActiveSegment = activeSegment;
            
            // Scroll the container to the active segment
            if (transcriptContainer) {
                const containerHeight = transcriptContainer.clientHeight;
                // Since we set transcript-container to position: relative, 
                // offsetTop is relative to the container.
                const segmentTop = activeSegment.offsetTop;
                const segmentHeight = activeSegment.offsetHeight;
                
                transcriptContainer.scrollTo({
                    top: segmentTop - (containerHeight / 4) + (segmentHeight / 2),
                    behavior: 'smooth'
                });
            }
        }
    });
});