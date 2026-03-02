
document.addEventListener('DOMContentLoaded', function() {
    const fontSelect = document.getElementById('font-select');
    const transcriptContainer = document.getElementById('transcript-container');

    fontSelect.addEventListener('change', function() {
        transcriptContainer.style.fontFamily = this.value;
    });
});
