// script.js
window.addEventListener('DOMContentLoaded', () => {

    const video = document.getElementById('lesson_video');
    const textContainer = document.getElementById('transcript-container');
    const segments = document.querySelectorAll('.transcript-segment');

    let currentActiveSegment = null;

    video.addEventListener('timeupdate', () => {
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
            }

            // Add 'active' class to the new segment
            activeSegment.classList.add('active');
            currentActiveSegment = activeSegment;
            
            // Scroll the container to the active segment
            // 'center' tries to put the element in the middle of the container
            activeSegment.scrollIntoView({
                behavior: 'smooth',
                block: 'center',
                inline: 'nearest'
            });
        }
    });
});