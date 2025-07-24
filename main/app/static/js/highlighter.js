document.addEventListener('DOMContentLoaded', () => {
    const textContainer = document.getElementById('text-container');
    const commentSidebar = document.getElementById('comment-sidebar');
    if (!textContainer || !commentSidebar) return;

    const menu = document.getElementById('highlight-menu');
    const highlightButton = document.getElementById('highlight-btn');
    let currentRange = null;

    // --- Pop-up Menu Logic (No Changes) ---
    textContainer.addEventListener('mouseup', (event) => {
        setTimeout(() => {
            const selection = window.getSelection();
            if (selection.isCollapsed || !textContainer.contains(selection.anchorNode)) {
                menu.style.display = 'none';
                return;
            }
            currentRange = selection.getRangeAt(0);
            const rect = currentRange.getBoundingClientRect();
            menu.style.display = 'block';
            menu.style.left = `${rect.left + window.scrollX + (rect.width / 2) - (menu.offsetWidth / 2)}px`;
            menu.style.top = `${rect.top + window.scrollY - menu.offsetHeight - 5}px`;
        }, 10);
    });
    
    // --- Highlight Button Logic (No Changes) ---
    highlightButton.addEventListener('click', async () => {
        if (!currentRange) return;
        try {
            const offsets = getRangeCharacterOffset(textContainer, currentRange);
            const response = await fetch(currentURL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify({
                    start_offset: offsets.start,
                    end_offset: offsets.end,
                    selected_text: currentRange.toString(),
                    comtype: 'highlight'
                })
            });
            if (!response.ok) throw new Error('Failed to save highlight');
            window.location.reload();
        } catch (error) {
            console.error('Error saving highlight:', error);
            alert('Could not save your highlight.');
        } finally {
            menu.style.display = 'none';
            window.getSelection().removeAllRanges();
            currentRange = null;
        }
    });

    // --- THE NEW, UNIFIED FOCUS SYSTEM ---

    /**
     * Sets focus on a comment and its corresponding highlight.
     * @param {string} commentId The ID of the item to focus.
     * @param {string} scrollTarget Which element to scroll into view ('comment' or 'highlight').
     */
    function setFocus(commentId, scrollTarget) {
        // 1. Clear any previous focus from both the sidebar and the main text.
        const prevFocusedComment = document.querySelector('.focused-comment');
        if (prevFocusedComment) {
            prevFocusedComment.classList.remove('focused-comment');
        }
        const prevFocusedHighlight = document.querySelector('.focused-highlight');
        if (prevFocusedHighlight) {
            prevFocusedHighlight.classList.remove('focused-highlight');
        }

        // If no commentId is provided, we're done (this is for clearing focus).
        if (!commentId) return;

        // 2. Find the new elements to focus.
        const commentToFocus = document.querySelector(`.comment[data-comment-id='${commentId}']`);
        const highlightToFocus = document.querySelector(`.highlight[data-comment-id='${commentId}']`);

        // 3. Apply the 'focused' classes and scroll the target into view.
        if (commentToFocus) {
            commentToFocus.classList.add('focused-comment');
            if (scrollTarget === 'comment') {
                commentToFocus.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
        if (highlightToFocus) {
            highlightToFocus.classList.add('focused-highlight');
            if (scrollTarget === 'highlight') {
                highlightToFocus.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    }

    // --- UPDATED EVENT LISTENERS (Now using the setFocus function) ---

    // When a HIGHLIGHT in the text is clicked...
    textContainer.addEventListener('click', (e) => {
        const highlightSpan = e.target.closest('.highlight');
        if (highlightSpan && highlightSpan.dataset.commentId) {
            const commentId = highlightSpan.dataset.commentId;
            setFocus(commentId, 'comment'); // Focus everything, scroll the comment into view.
        }
    });

    // When a COMMENT in the sidebar is clicked...
    commentSidebar.addEventListener('click', (e) => {
        const clickedComment = e.target.closest('.comment');
        if (clickedComment && clickedComment.dataset.commentId) {
            const commentId = clickedComment.dataset.commentId;
            setFocus(commentId, 'highlight'); // Focus everything, scroll the highlight into view.
        }
    });

    // When clicking anywhere else on the page...
    document.addEventListener('click', (e) => {
        // If the click was NOT inside a comment and NOT on a highlight, clear all focus.
        if (!e.target.closest('.comment') && !e.target.closest('.highlight')) {
            setFocus(null);
        }
    }, true); // Use capture phase to handle the event cleanly.


    // --- Functions to apply highlights and offsets (No Changes) ---
    
    function applyHighlightsFromComments() {
        if (!commentsData || commentsData.length === 0) return;
        commentsData.sort((a, b) => a.ts_start_offset - b.ts_start_offset);
        for (const comment of commentsData) {
            if (comment.ts_start_offset == null || comment.ts_end_offset == null) continue;
            try {
                const range = createRangeFromOffsets(textContainer, comment.ts_start_offset, comment.ts_end_offset);
                applyHighlight(range, comment.id);
            } catch (error) {
                console.error('Could not apply saved highlight:', comment, error);
            }
        }
    }
    
    function applyHighlight(range, commentId) {
        const highlightSpan = document.createElement('span');
        highlightSpan.className = 'highlight';
        if (commentId) {
            highlightSpan.dataset.commentId = commentId;
        }
        try {
            range.surroundContents(highlightSpan);
        } catch (e) {
            const content = range.extractContents();
            highlightSpan.appendChild(content);
            range.insertNode(highlightSpan);
        }
    }

    function createRangeFromOffsets(container, startOffset, endOffset) {
        const range = document.createRange();
        const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
        let charCount = 0, startNode, endNode;
        while (walker.nextNode()) {
            const node = walker.currentNode;
            const nodeLength = node.textContent.length;
            if (startNode === undefined && startOffset < charCount + nodeLength) {
                startNode = node;
                range.setStart(node, startOffset - charCount);
            }
            if (endNode === undefined && endOffset <= charCount + nodeLength) {
                endNode = node;
                range.setEnd(node, endOffset - charCount);
                break;
            }
            charCount += nodeLength;
        }
        if (!startNode || !endNode) throw new Error("Could not create range from offsets.");
        return range;
    }

    function getRangeCharacterOffset(container, range) {
        const preRange = document.createRange();
        preRange.selectNodeContents(container);
        preRange.setEnd(range.startContainer, range.startOffset);
        const start = preRange.toString().length;
        return { start, end: start + range.toString().length };
    }

    // --- Initial Execution ---
    applyHighlightsFromComments();
});