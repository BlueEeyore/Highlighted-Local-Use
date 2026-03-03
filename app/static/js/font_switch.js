document.addEventListener('DOMContentLoaded', () => {
    const fontSelector = document.getElementById('font-family');
    const sizeInput = document.getElementById('font-size');
    const sizeList = document.getElementById('font-size-list');
    const sizeDropdown = document.getElementById('font-size-dropdown');
    const transcriptContainer = document.getElementById('transcript-container');

    function updateFontSize(size) {
        if (size && size > 0) {
            transcriptContainer.style.fontSize = `${size}px`;
            
            // Sync the input value
            if (sizeInput.value !== size.toString()) {
                sizeInput.value = size;
            }

            // Also update individual segments for consistency
            const segments = transcriptContainer.querySelectorAll('.transcript-segment');
            segments.forEach(segment => {
                segment.style.fontSize = `${size}px`;
            });
        }
    }

    if (fontSelector && transcriptContainer) {
        fontSelector.addEventListener('change', (e) => {
            const selectedFont = e.target.value;
            transcriptContainer.style.fontFamily = selectedFont;
        });
    }

    if (sizeInput && transcriptContainer) {
        // Handle direct typing
        sizeInput.addEventListener('input', (e) => {
            updateFontSize(e.target.value);
        });

        // Bootstrap dropdown instance
        const bsDropdown = new bootstrap.Dropdown(sizeInput);

        // Show dropdown on click or focus
        sizeInput.addEventListener('click', () => {
            bsDropdown.show();
        });

        sizeInput.addEventListener('focus', () => {
            bsDropdown.show();
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!sizeDropdown.contains(e.target)) {
                bsDropdown.hide();
            }
        });

        // Handle dropdown selection
        if (sizeList) {
            sizeList.querySelectorAll('.dropdown-item').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    const size = e.target.getAttribute('data-size');
                    updateFontSize(size);
                    bsDropdown.hide();
                });
            });
        }

        // Initialize with default value
        updateFontSize(sizeInput.value);
    }
});
