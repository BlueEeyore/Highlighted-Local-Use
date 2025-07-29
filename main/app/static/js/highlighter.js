document.addEventListener('DOMContentLoaded', () => {
    // --- ELEMENT SELECTORS ---
    const textContainer = document.getElementById('transcript-container');
    const commentSidebar = document.getElementById('comment-sidebar');
    const menu = document.getElementById('highlight-menu');
    const highlightButton = document.getElementById('highlight-btn');
    const commentButton = document.getElementById('comment-btn');
    const jumpButton = document.getElementById('jump-btn');
    const video = document.getElementById("lesson_video")

    if (!textContainer || !commentSidebar || !menu) {
        console.error("A critical element is missing from the page.");
        return;
    }

    let currentRange = null;

    // --- POP-UP MENU LOGIC (MODIFIED TO HANDLE OVERLAPS) ---
    textContainer.addEventListener('mouseup', (event) => {
        setTimeout(() => {
            const selection = window.getSelection();

            // Hide menu on simple clicks and do nothing.
            if (selection.isCollapsed) {
                menu.style.display = 'none';
                return;
            }

            if (selection.rangeCount > 0 && textContainer.contains(selection.anchorNode)) {
                currentRange = selection.getRangeAt(0);

                // --- NEW: OVERLAP DETECTION LOGIC ---
                let isOverlapping = false;
                const existingHighlights = textContainer.querySelectorAll('.highlight');
                for (const highlight of existingHighlights) {
                    // The intersectsNode() method checks if the user's selection
                    // crosses the boundary of an existing highlight.
                    if (currentRange.intersectsNode(highlight)) {
                        isOverlapping = true;
                        break; // Found an overlap, no need to check further
                    }
                }

                // Enable or disable buttons based on the overlap check.
                if (isOverlapping) {
                    highlightButton.disabled = true;
                    commentButton.disabled = true;
                } else {
                    highlightButton.disabled = false;
                    commentButton.disabled = false;
                }
                // --- END OF NEW LOGIC ---

                // Position and show the menu regardless of button state.
                const rect = currentRange.getBoundingClientRect();
                menu.style.display = 'block';
                menu.style.left = `${rect.left + window.scrollX + (rect.width / 2) - (menu.offsetWidth / 2)}px`;
                menu.style.top = `${rect.top + window.scrollY - menu.offsetHeight - 5}px`;
            }
        }, 10);
    });

    document.addEventListener('mousedown', (event) => {
        if (!menu.contains(event.target)) {
            menu.style.display = 'none';
        }
    });


    // --- FOCUSING, INITIALIZATION, AND HELPER FUNCTIONS ---
    // (The rest of the file remains the same as the previous version)

    function setFocus(commentId, scrollTarget) {
        const prevFocusedComment = document.querySelector('.focused-comment');
        if (prevFocusedComment) prevFocusedComment.classList.remove('focused-comment');
        const prevFocusedHighlight = document.querySelector('.focused-highlight');
        if (prevFocusedHighlight) prevFocusedHighlight.classList.remove('focused-highlight');

        if (!commentId) return;

        const commentToFocus = document.querySelector(`.comment[data-comment-id='${commentId}']`);
        const highlightToFocus = document.querySelector(`.highlight[data-comment-id='${commentId}']`);

        if (commentToFocus) {
            commentToFocus.classList.add('focused-comment');
            if (scrollTarget === 'comment') commentToFocus.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        if (highlightToFocus) {
            highlightToFocus.classList.add('focused-highlight');
            if (scrollTarget === 'highlight') highlightToFocus.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    textContainer.addEventListener('click', (e) => {
        const highlightSpan = e.target.closest('.highlight[data-comment-id]');
        if (highlightSpan) setFocus(highlightSpan.dataset.commentId, 'comment');
    });

    commentSidebar.addEventListener('click', (e) => {
        const clickedComment = e.target.closest('.comment');
        if (clickedComment && clickedComment.dataset.commentId) setFocus(clickedComment.dataset.commentId, 'highlight');
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.comment') && !e.target.closest('.highlight') && !e.target.closest('#highlight-menu')) {
            setFocus(null);
        }
    }, true);

    function initializeHighlights() {
        if (commentsData && commentsData.length > 0) {
            commentsData.sort((a, b) => a.ts_start_offset - b.ts_start_offset);
            for (const comment of commentsData) {
                if (comment.ts_start_offset == null || comment.ts_end_offset == null) continue;
                try {
                    applyHighlight(createRangeFromOffsets(textContainer, comment.ts_start_offset, comment.ts_end_offset), comment.id);
                } catch (error) { console.error('Could not apply comment highlight:', comment, error); }
            }
        }
        if (standaloneHighlights && standaloneHighlights.length > 0) {
            standaloneHighlights.sort((a, b) => a.ts_start_offset - b.ts_start_offset);
            for (const highlight of standaloneHighlights) {
                if (highlight.ts_start_offset == null || highlight.ts_end_offset == null) continue;
                try {
                    applyHighlight(createRangeFromOffsets(textContainer, highlight.ts_start_offset, highlight.ts_end_offset), null);
                } catch (error) { console.error('Could not apply standalone highlight:', highlight, error); }
            }
        }
    }

    highlightButton.addEventListener('click', async () => {
        if (!currentRange) return;
        try {
            const offsets = getRangeCharacterOffset(textContainer, currentRange);
            await fetch(currentURL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...offsets, selected_text: currentRange.toString(), comtype: 'highlight', posttype: 'highlight' })
            });
            window.location.reload();
        } catch (error) { console.error('Error saving highlight:', error); alert('Could not save your highlight.'); } finally { menu.style.display = 'none'; }
    });

    commentButton.addEventListener('click', () => {
        if (!currentRange) return;
        try {
            const offsets = getRangeCharacterOffset(textContainer, currentRange);
            const params = new URLSearchParams({ ...offsets, selected_text: currentRange.toString() });
            window.location.href = `${currentURL}?${params.toString()}`;
        } catch (error) { console.error("Error creating comment offsets:", error); alert("Could not prepare your comment."); }
    });

    jumpButton.addEventListener('click', () => {
        // Ensure a selection has been made
        if (!currentRange) {
            alert("Please select some text first.");
            return;
        }

        // Use our new helper function to get the timestamp
        const startTime = getTimestampFromRange(currentRange);

        // Check if we successfully got a timestamp
        if (startTime !== null) {
            console.log(`Jumping video to: ${startTime} seconds.`);
            
            // This is the line that seeks the video
            video.currentTime = startTime;

            // play the video if it's paused
            // video.play();

        } else {
            // This will happen if the selection started outside a valid segment
            alert("Could not find a timestamp for the selected text. Please select text within the transcript.");
        }

        // Hide the menu after the action
        menu.style.display = 'none';
    });

    function applyHighlight(range, commentId) {
        const span = document.createElement('span');
        span.className = 'highlight';
        if (commentId) span.dataset.commentId = commentId;
        try {
            range.surroundContents(span);
        } catch (e) {
            const content = range.extractContents();
            span.appendChild(content);
            range.insertNode(span);
        }
    }

    function createRangeFromOffsets(container, start, end) {
        const range = document.createRange();
        const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
        let count = 0, startNode, endNode;
        while (walker.nextNode()) {
            const node = walker.currentNode;
            const nodeLength = node.textContent.length;
            if (startNode === undefined && start < count + nodeLength) {
                startNode = node;
                range.setStart(node, start - count);
            }
            if (endNode === undefined && end <= count + nodeLength) {
                endNode = node;
                range.setEnd(node, end - count);
                break;
            }
            count += nodeLength;
        }
        if (!startNode || !endNode) throw new Error("Could not create range.");
        return range;
    }

    function getRangeCharacterOffset(container, range) {
        const preRange = document.createRange();
        preRange.selectNodeContents(container);
        preRange.setEnd(range.startContainer, range.startOffset);
        const start = preRange.toString().length;
        return { start_offset: start, end_offset: start + range.toString().length };
    }

    /**
     * Finds the first transcript segment that intersects with the start of a range
     * and returns its data-timestamp value as a number.
     * 
     * @param {Range} range - The selection range from window.getSelection().
     * @returns {number|null} The timestamp as a float, or null if not found.
     */
    function getTimestampFromRange(range) {
        // 1. Get the node where the selection starts.
        // This is often a text node, not the <p> element itself.
        const startNode = range.startContainer;

        // 2. Find the closest ancestor element that is a transcript segment.
        // We use .parentElement to handle cases where startNode is a text node.
        // .closest() is perfect because it checks the element itself and then its ancestors.
        const segment = startNode.parentElement.closest('.transcript-segment');

        // 3. Check if we found a segment and if it has the timestamp attribute.
        if (segment && segment.dataset.timestamp) {
            // 4. Return the timestamp. It's crucial to convert the string value
            // from the attribute into a number using parseFloat().
            return parseFloat(segment.dataset.timestamp);
        }

        // 5. If no segment or timestamp was found, return null.
        return null;
    }

    initializeHighlights();
});