// Making sure the following code starts after the page has loaded
document.addEventListener('DOMContentLoaded', () => {
    // Selecting elements of the page that will be used later on
    const textContainer = document.getElementById('transcript-container');
    const commentSidebar = document.getElementById('comment-sidebar');
    const menu = document.getElementById('highlight-menu');
    const highlightButton = document.getElementById('highlight-btn');
    const commentButton = document.getElementById('comment-btn');
    const jumpButton = document.getElementById('jump-btn');
    const video = document.getElementById("lesson_video")
    const newCommentContainer = document.getElementById('setting-comment');

    // the text container containing the transcript, the comment sidebar,
    // and the highlight menu are crucial elements of this page. This checks
    // if they are there and raises a console error if not
    if (!textContainer || !commentSidebar || !menu) {
        console.error("A critical element is missing from the page.");
        return;
    }

    // setting currentRange to null initially. Will change if user highlights
    // a portion of the transcript
    let currentRange = null;

    // --- POP-UP MENU LOGIC ---
    // listening for when the user ends their selection (releases their mouse)
    textContainer.addEventListener('mouseup', (event) => {
        // delaying the code by imperceptible amount to give the code time to update information
        // (avoiding race conditions)
        setTimeout(() => {
            // getting the range of text that was selected
            const selection = window.getSelection();

            // Hide menu on simple clicks and do nothing.
            if (selection.isCollapsed) {
                menu.style.display = 'none';    // hide menu
                return;     // exit function
            }

            // checking that there is at least one selected range and that it starts within the
            // transcript container
            if (selection.rangeCount > 0 && textContainer.contains(selection.anchorNode)) {
                
                // setting our currentRange variable (defined earlier) to the Range object which
                // contains the detailed information on the start and end points of the selection
                currentRange = selection.getRangeAt(0);

                // --- OVERLAP DETECTION LOGIC ---
                let isOverlapping = false;
                // get all pre-existing elements with class .highlight
                const existingHighlights = textContainer.querySelectorAll('.highlight');
                // looping over these elements
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
                // --- END OF OVERLAP DETECTION LOGIC ---

                // Position and show the menu regardless of button state.
                const rect = currentRange.getBoundingClientRect();  // gives size and position of selection relative to viewport
                menu.style.display = 'block';
                menu.style.left = `${rect.left + window.scrollX + (rect.width / 2) - (menu.offsetWidth / 2)}px`;
                menu.style.top = `${rect.top + window.scrollY - menu.offsetHeight - 5}px`;
            }
        }, 10);
    });

    // This logic only runs if the new comment form is actually on the page.
    if (newCommentContainer) {
        // Define the function that will handle the click.
        const handleOutsideClick = (event) => {
            // Check if the click was *inside* the new comment container.
            // If it was, we do nothing and let the user interact with the form.
            if (newCommentContainer.contains(event.target)) {
                return;
            }

            // If the click was *outside* the container, we cancel the comment.
            // We do this by redirecting to the base URL without the comment query parameters.
            // The `currentURL` variable already holds the clean path.
            window.location.href = currentURL;

            // It's good practice to remove the listener after it has served its purpose,
            // though in this case, a page reload will happen anyway.
            document.removeEventListener('click', handleOutsideClick, true);
        };

        // Add a click listener to the entire document.
        // The `true` at the end makes it a "capturing" listener, meaning it
        // runs before other listeners on specific elements. This ensures it
        // always gets to check the click location first.
        document.addEventListener('click', handleOutsideClick, true);
    }

    // --- POP-UP MENU HIDING LOGIC ---
    // listening for when user performs first half of click
    document.addEventListener('mousedown', (event) => {
        // "if the user clicked outside of the pop-up menu"
        if (!menu.contains(event.target)) {
            // hide menu
            menu.style.display = 'none';
        }
    });

    // --- FOCUSING, INITIALIZATION, AND HELPER FUNCTIONS ---
    // - this is the logic for focusing and unfocusing highlights and comments when they or their
    // counterpart is clicked
    

    function setFocus(commentId, scrollTarget) {

        // find any elements that are already focused and remove their focus
        const prevFocusedComment = document.querySelector('.focused-comment');
        if (prevFocusedComment) prevFocusedComment.classList.remove('focused-comment');
        const prevFocusedHighlight = document.querySelector('.focused-highlight');
        if (prevFocusedHighlight) prevFocusedHighlight.classList.remove('focused-highlight');

        // if no new commentId is provided, then all we had to do was clean up
        if (!commentId) return;

        // find the new elements to focus
        const commentToFocus = document.querySelector(`.comment[data-comment-id='${commentId}']`);
        const highlightToFocus = document.querySelector(`.highlight[data-comment-id='${commentId}']`);

        // apply new focused classes to elements
        if (commentToFocus) {
            commentToFocus.classList.add('focused-comment');
            // scroll to new focused element
            if (scrollTarget === 'comment') {
                const containerHeight = commentSidebar.clientHeight;
                const commentTop = commentToFocus.offsetTop;
                const commentHeight = commentToFocus.offsetHeight;

                commentSidebar.scrollTo({
                    top: commentTop - (containerHeight / 2) + (commentHeight / 2),
                    behavior: 'smooth'
                });
            }
        }
        if (highlightToFocus) {
            highlightToFocus.classList.add('focused-highlight');
            // scroll to new focused element
            if (scrollTarget === 'highlight') {
                const containerHeight = textContainer.clientHeight;
                const highlightTop = highlightToFocus.offsetTop;
                const highlightHeight = highlightToFocus.offsetHeight;

                textContainer.scrollTo({
                    top: highlightTop - (containerHeight / 2) + (highlightHeight / 2),
                    behavior: 'smooth'
                });
            }
        }
    }

    // listens for a click inside the transcript container
    textContainer.addEventListener('click', (e) => {
        // finds next div up the ancestor tree and check if this is a highlight span
        const highlightSpan = e.target.closest('.highlight[data-comment-id]');
        if (highlightSpan) setFocus(highlightSpan.dataset.commentId, 'comment');    // if highlight span, focus the associated comment
    });

    // listens for a click inside the comment sidebar
    commentSidebar.addEventListener('click', (e) => {
        // same logic as before
        const clickedComment = e.target.closest('.comment');
        if (clickedComment && clickedComment.dataset.commentId) setFocus(clickedComment.dataset.commentId, 'highlight');
    });

    // listens for click in neither transcript container or comment sidebar and defocuses everything
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.comment') && !e.target.closest('.highlight') && !e.target.closest('#highlight-menu')) {
            setFocus(null);
        }
    }, true);

    
    // initialising (applying) all highlights
    function initializeHighlights() {
        // Render highlights that are tied to existing comments
        if (commentsData && commentsData.length > 0) {

            // sort the highlights based on starting position
            commentsData.sort((a, b) => a.ts_start_offset - b.ts_start_offset);

            // loop over comment highlights
            for (const comment of commentsData) {
                // skip the ones that don't have the necessary info
                if (comment.ts_start_offset == null || comment.ts_end_offset == null) continue;
                try {
                    // apply highlight. These are normal highlights, so no extra attributes are needed.
                    applyHighlight(createRangeFromOffsets(textContainer, comment.ts_start_offset, comment.ts_end_offset), comment.id, null);
                } catch (error) {
                    // fail gracefully if a problem with applying the highlight occurs
                    console.error('Could not apply comment highlight:', comment, error);
                }
            }
        }

        // Render standalone highlights (including temporary "setting" highlight)
        if (standaloneHighlights && standaloneHighlights.length > 0) {
            
            // sort the highlights based on starting position
            standaloneHighlights.sort((a, b) => a.ts_start_offset - b.ts_start_offset);
            
            // loop over standalone highlights
            for (const highlight of standaloneHighlights) {
                if (highlight.ts_start_offset == null || highlight.ts_end_offset == null) continue;
                try {
                    // Check if this is the special highlight for a new comment
                    const attributes = highlight.comtype === 'setting' ? { setting: 'true' } : null;
                    
                    // Pass the attributes object to the applyHighlight function
                    applyHighlight(createRangeFromOffsets(textContainer, highlight.ts_start_offset, highlight.ts_end_offset), null, attributes);
                } catch (error) {
                    // fail gracefully if a problem with applying the highlight occurs
                    console.error('Could not apply standalone highlight:', highlight, error);
                }
            }
        }
    }

    // if highlight button is pressed (in pop-up menu)
    highlightButton.addEventListener('click', async () => {
        // check that a range was actually selected before highlight button is pressed (should happen anyways)
        if (!currentRange) return;
        try {
            // get offset information for selected portion
            const offsets = getRangeCharacterOffset(textContainer, currentRange);
            
            // send post request to server with offset information
            await fetch(currentURL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...offsets, selected_text: currentRange.toString(), comtype: 'highlight', posttype: 'highlight' })
            });
            window.location.reload();

        } catch (error) {
            // fail gracefully if a problem occurs
            console.error('Error saving highlight:', error); alert('Could not save your highlight.'); } finally { menu.style.display = 'none'; }
    });

    // if comment button is pressed (in pop-up menu)
    commentButton.addEventListener('click', () => {
        // check that a range was actually selected before highlight button is pressed (should happen anyways)
        if (!currentRange) return;
        try {
            // get offset information for selected portion
            const offsets = getRangeCharacterOffset(textContainer, currentRange);
            
            // send GET request to server with offset information
            const params = new URLSearchParams({ ...offsets, selected_text: currentRange.toString() });
            window.location.href = `${currentURL}?${params.toString()}`;
        } catch (error) {
            // fail gracefully if a problem occurs
            console.error("Error creating comment offsets:", error); alert("Could not prepare your comment."); }
    });

    // if jump to text button is pressed (in pop-up menu)
    jumpButton.addEventListener('click', () => {
        // Ensure a selection has been made
        if (!currentRange) {
            alert("Please select some text first.");
            return;
        }

        // Get the timestamp (using helper function)
        const startTime = getTimestampFromRange(currentRange);

        // Check if we successfully got a timestamp
        if (startTime !== null) {
            // console.log(`Jumping video to: ${startTime} seconds.`);
            
            // seek the video
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

    // applies a highlight on the page with information given (range, etc)
    function applyHighlight(range, commentId, attributes) { 
        
        // create a new HTML <span> element in memory (which will later be applied)
        const span = document.createElement('span'); 

        // apply ".highlight" class to span
        span.className = 'highlight'; 
        
        // if associated with a comment
        if (commentId) { 
            // apply custom ".data-comment-id" class with comment id to associate highlight with comment
            span.dataset.commentId = commentId; 
        } 
        // if attributes applied to comment
        if (attributes) { 
            // loop through properties in provided attributes object
            for (const attr in attributes) { 
                // add a new "data-*" attribute on the <span>.
                // e.g. attributes like {setting: 'true'} will create "data-setting='true'"
                span.dataset[attr] = attributes[attr]; 
            } 
        } 
        try { 
            // finally, wrap the range with the <span> element
            range.surroundContents(span); 
        } catch (e) { 
            // if this doesn't work, we need a more robust method:

            // take out the contents and store in memory
            const content = range.extractContents(); 

            // put the content inside the span element
            span.appendChild(content); 

            // insert this back into the text
            range.insertNode(span); 
        } 
    }

    // function that converts offset information into Range object
    function createRangeFromOffsets(container, start, end) {
        // initialise new, empty Range object
        const range = document.createRange();

        // Create a 'TreeWalker', an efficient browser tool for navigating through the document structure
        // Tell it to only visit TEXT_NODES, meaning it will ignore HTML tags like <p>, <b>, etc.,
        // and only look at the actual text content, which is what our character counts are based on
        const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
        
        // this counts how many characters we will have passed
        // startNode and endNode will store the specific text nodes where the selection starts and ends.
        let count = 0, startNode, endNode;

        // continue looping while the walker can find another text node to move to
        while (walker.nextNode()) {

            // get the text node that the walker is currently on and its character length
            const node = walker.currentNode;
            const nodeLength = node.textContent.length;

            // Check if found the start of the highlight yet. Only run this if 'startNode' is still empty
            // The condition `start < count + nodeLength` checks if the target start position falls within the current text node
            if (startNode === undefined && start < count + nodeLength) {
                // set the startNode
                startNode = node;

                // tell the range where to start. Needs the starting node and the character position within that node
                // (global 'start' position minus the 'count' of all text that came before this node)
                range.setStart(node, start - count);
            }
            
            // apply same logic to endNode...
            if (endNode === undefined && end <= count + nodeLength) {
                endNode = node;
                range.setEnd(node, end - count);
                break;
            }
            
            // keep count by incrementing the length of this node before moving to next node
            count += nodeLength;
        }
        
        // fail gracefully if we either failed to set a startNode or an endNode
        if (!startNode || !endNode) throw new Error("Could not create range.");

        // if successful, return our new range object!
        return range;
    }

    // opposite function of the one defined above: turns Range object into offset info
    function getRangeCharacterOffset(container, range) {
        // create new temporary Range object
        const preRange = document.createRange();
        
        // set this new Range object to contain *all* info in the container
        preRange.selectNodeContents(container);

        // set the object's range to end where the user's actual selection starts
        // this way, we now have a range of everything before the user's selection
        preRange.setEnd(range.startContainer, range.startOffset);
        
        // this allows us to now convert the range to a string, and get our start offset
        // by finding its length
        const start = preRange.toString().length;

        // the end offset is now just that start offset plus the length of the original range
        return { start_offset: start, end_offset: start + range.toString().length };
    }

    // finds the first transcript segment that intersects with the start of a range
    // and returns its data-timestamp value as a number
    // (used for jumping to place in video)
    function getTimestampFromRange(range) {
        // get the node where the selection starts
        const startNode = range.startContainer;

        // find the closest ancestor element that is a transcript segment
        // .parentElement is used to handle cases where startNode is a text node
        // .closest() is perfect because it checks the element itself and then its ancestors.
        const segment = startNode.parentElement.closest('.transcript-segment');

        // check if found a segment and if it has the timestamp attribute.
        if (segment && segment.dataset.timestamp) {
            // return the timestamp. It's crucial to convert the string value
            // from the attribute into a number using parseFloat()
            return parseFloat(segment.dataset.timestamp);
        }

        // if no segment or timestamp was found, return null
        return null;
    }

    // Always initialize highlights on page load
    initializeHighlights();
});