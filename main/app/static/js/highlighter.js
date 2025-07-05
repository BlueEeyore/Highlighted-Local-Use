document.addEventListener('DOMContentLoaded', () => {
    const textContainer = document.getElementById('text-container');
    if (!textContainer) return;

    const menu = document.getElementById('highlight-menu');
    const highlightButton = document.getElementById('highlight-btn');
    let currentRange = null;

    // --- Event Listeners for Pop-up Menu ---

    textContainer.addEventListener('mouseup', (event) => {
        setTimeout(() => {
            console.log("Mouseup detected");
            const selection = window.getSelection();
            const anchorNode = selection.anchorNode;
            const focusNode = selection.focusNode;

            if (selection.isCollapsed || !anchorNode || !textContainer.contains(anchorNode) || !focusNode || !textContainer.contains(focusNode)) {
                menu.style.display = 'none';
                return;
            }
    
            currentRange = selection.getRangeAt(0);
            const rect = currentRange.getBoundingClientRect();
    
            // Step 1: Make menu visible but hidden to measure size
            menu.style.visibility = 'hidden';
            menu.style.display = 'block';
    
            const menuWidth = menu.offsetWidth;
            const menuHeight = menu.offsetHeight;
    
            // Step 2: Calculate initial centered position
            let left = rect.left + window.scrollX + (rect.width / 2) - (menuWidth / 2);
            let top = rect.top + window.scrollY - menuHeight - 5;
    
            // Step 3: Clamp position to prevent off-screen
            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
    
            // Clamp horizontally
            left = Math.max(5, Math.min(left, viewportWidth - menuWidth - 5));
    
            // Clamp vertically (optional, but avoids negative top)
            top = Math.max(5, top);
    
            // Step 4: Apply final position and show menu
            menu.style.left = `${left}px`;
            menu.style.top = `${top}px`;
            menu.style.visibility = 'visible';
        }, 10);
    });
    

    document.addEventListener('mousedown', (event) => {
        if (!menu.contains(event.target) && menu.style.display === 'block') {
            menu.style.display = 'none';
            // Optional: clear selection if you click away from the menu
            // window.getSelection().removeAllRanges(); 
        }
    });

    // --- Handle Highlight Button Click ---
    highlightButton.addEventListener('click', async () => {
        if (!currentRange) return;

        try {
            // 1. Calculate character offsets using our robust function
            const offsets = getRangeCharacterOffset(textContainer, currentRange);

            // 2. Send the offsets to the backend
            const response = await fetch(currentURL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify({
                    start_offset: offsets.start,
                    end_offset: offsets.end,
                    selected_text: currentRange.toString(), // Also useful to save the text itself
                    comtype: 'highlight'
                })
            });

            // Navigate to the same page with parameters for the backend
            // window.location.href = `${currentURL}?${params.toString()}`;
            window.location.href = `${currentURL}`;

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to save highlight');
            }

            // 3. On success, apply the highlight visually right away
            applyHighlight(currentRange);

        } catch (error) {
            console.error('Error saving highlight:', error);
            alert('Could not save your highlight. Please try again.');
        } finally {
            // 4. Clean up
            menu.style.display = 'none';
            window.getSelection().removeAllRanges();
            currentRange = null;
        }
    });

    // Handle when existing highlight is clicked
    textContainer.addEventListener('click', (e) => {
        const target = e.target;
    
        if (target.classList.contains('highlight') && target.dataset.commentId) {
            const commentId = target.dataset.commentId;
            focusComment(commentId);
        }
    });

    // Function to "focus" comment associated with clicked highlight
    function focusComment(commentId) {
        const comment = document.querySelector(`.comment[data-comment-id='${commentId}']`);

        if (comment) {
            // Scroll comment sidebar to bring it into view
            comment.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // Add emphasis effect
            comment.classList.add('focused-comment');

            // Remove emphasis when clicking outside
            function handleClickOutside(e) {
                if (!comment.contains(e.target)) {
                    comment.classList.remove('focused-comment');
                    document.removeEventListener('mousedown', handleClickOutside);
                }
            }

            document.addEventListener('mousedown', handleClickOutside);
        }
    }

    // --- Function to apply saved highlights on page load ---
    function applySavedHighlights() {
        if (!savedHighlights || savedHighlights.length === 0) {
            return;
        }

        // Sort highlights to apply them in order of appearance
        savedHighlights.sort((a, b) => a.ts_start_offset - b.ts_start_offset);

        for (const highlight of savedHighlights) {
            // Ensure the properties exist before using them
            if (highlight.ts_start_offset == null || highlight.ts_end_offset == null) continue;
            
            try {
                const range = createRangeFromOffsets(textContainer, highlight.ts_start_offset, highlight.ts_end_offset);
                applyHighlight(range, highlight.id);
            } catch (error) {
                console.error('Could not apply saved highlight:', highlight, error);
            }
        }
    }

    // --- Helper Functions ---

    function applyHighlight(range, commentId = null) {
        const highlightSpan = document.createElement('span');
        highlightSpan.className = 'highlight';
        
        if (commentId) {
            highlightSpan.dataset.commentId = commentId;
        }

        try {
            // This is the ideal way to wrap a selection
            range.surroundContents(highlightSpan);
        } catch (e) {
            // This can happen if the range spans across incompatible element boundaries.
            // A fallback is to extract, wrap, and re-insert.
            console.warn("Could not use surroundContents, using fallback. Error:", e);
            const content = range.extractContents();
            highlightSpan.appendChild(content);
            range.insertNode(highlightSpan);
        }
    }

    /**
     * Creates a DOM Range object from character offsets within a container.
     * This function is the "loader".
     * @param {Node} container - The element containing the text.
     * @param {number} startOffset - The starting character offset.
     * @param {number} endOffset - The ending character offset.
     * @returns {Range}
     */
    function createRangeFromOffsets(container, startOffset, endOffset) {
        const range = document.createRange();
        const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
        let charCount = 0;
        let startNode, endNode, startNodeOffset, endNodeOffset;

        while (walker.nextNode()) {
            const node = walker.currentNode;
            const nodeLength = node.textContent.length;

            if (startNode === undefined && startOffset < charCount + nodeLength) {
                startNode = node;
                startNodeOffset = startOffset - charCount;
            }

            if (endNode === undefined && endOffset <= charCount + nodeLength) {
                endNode = node;
                endNodeOffset = endOffset - charCount;
                break; // Found both points, we can stop
            }

            charCount += nodeLength;
        }

        if (startNode && endNode) {
            range.setStart(startNode, startNodeOffset);
            range.setEnd(endNode, endNodeOffset);
            return range;
        }
        throw new Error("Could not create range from offsets. The text may have changed.");
    }

    /**
     * REWRITTEN: Gets the start and end character offsets of a Range within a container.
     * This function is the "saver" and is the symmetrical inverse of the loader.
     * @param {Node} container - The element containing the text.
     * @param {Range} range - The range to measure.
     * @returns {{start: number, end: number}}
     */
    function getRangeCharacterOffset(container, range) {
        const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
        let charCount = 0;
        let start = -1;
        let end = -1;

        while (walker.nextNode()) {
            const node = walker.currentNode;
            if (node === range.startContainer) {
                start = charCount + range.startOffset;
            }
            if (node === range.endContainer) {
                end = charCount + range.endOffset;
                break; // Found both, we're done
            }
            charCount += node.textContent.length;
        }

        // If the selection spans multiple nodes, end won't be found in the first loop.
        // We need to calculate it based on the start and the length of the selected text.
        if (start !== -1 && end === -1) {
             end = start + range.toString().length;
        }
       
        // Fallback for single-node selections where the loop exits early
        if (start !== -1 && end === -1) {
            end = start + (range.endOffset - range.startOffset);
        }

        if (start === -1 || end === -1) {
            throw new Error("Could not calculate offsets for the given range.");
        }

        return { start, end };
    }

    // --- Initial Execution ---
    applySavedHighlights();


    const commentButton = document.getElementById('comment-btn');

    commentButton.addEventListener('click', () => {
        if (!currentRange) {
            alert("Please highlight text before adding a comment.");
            return;
        }

        try {
            const offsets = getRangeCharacterOffset(textContainer, currentRange);

            const params = new URLSearchParams({
                start_offset: offsets.start,
                end_offset: offsets.end,
                selected_text: currentRange.toString(),
            });

            // Navigate to the same page with parameters for the backend
            window.location.href = `${currentURL}?${params.toString()}`;

        } catch (error) {
            console.error("Error calculating offsets for comment:", error);
            alert("Could not prepare comment. Please try again.");
        }
    });
});