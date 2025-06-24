document.addEventListener('DOMContentLoaded', () => {
    const textContainer = document.getElementById('text-container');
    const menu = document.getElementById('highlight-menu');
    const highlightButton = document.getElementById('highlight-btn');

    let currentRange = null;

    // Show the menu when text is selected
    textContainer.addEventListener('mouseup', (event) => {
        // Use setTimeout to allow the selection to finalize
        setTimeout(() => {
            const selection = window.getSelection();

            // If the selection is empty or just a click, hide the menu
            if (selection.isCollapsed) {
                menu.style.display = 'none';
                return;
            }

            // Make sure the selection is within our target container
            if (textContainer.contains(selection.anchorNode) && textContainer.contains(selection.focusNode)) {
                // Store the selected range
                currentRange = selection.getRangeAt(0);
                const rect = currentRange.getBoundingClientRect();

                // Position the menu above the selection
                menu.style.display = 'block';
                menu.style.left = `${rect.left + window.scrollX + (rect.width / 2) - (menu.offsetWidth / 2)}px`;
                menu.style.top = `${rect.top + window.scrollY - menu.offsetHeight - 5}px`;
            }
        }, 10);
    });

    // Hide the menu if the user clicks elsewhere on the page
    document.addEventListener('mousedown', (event) => {
        // Hide the menu if the click is outside of the menu itself
        if (!menu.contains(event.target)) {
            menu.style.display = 'none';
            currentRange = null;
        }
    });

    // Handle the highlight button click
    highlightButton.addEventListener('click', () => {
        if (currentRange) {
            applyHighlight(currentRange);
            menu.style.display = 'none';
            // Clear the selection after highlighting
            window.getSelection().removeAllRanges();
            currentRange = null;
        }
    });

    /**
     * Wraps the given DOM Range with a <span class="highlight"> tag.
     * This is the first step. The real magic for overlaps happens in normalizeHighlights.
     * @param {Range} range The DOM Range object to highlight.
     */
    function applyHighlight(range) {
        // Create a new span element for the highlight
        const highlightSpan = document.createElement('span');
        highlightSpan.className = 'highlight';

        try {
            // This is the simplest way to wrap a selection.
            // It can create adjacent spans, which we'll fix.
            // Using extractContents and insertNode is more robust
            // for complex selections across different nodes.
            const content = range.extractContents();
            highlightSpan.appendChild(content);
            range.insertNode(highlightSpan);

            // The KEY step: normalize the DOM to merge adjacent highlights
            normalizeHighlights(highlightSpan.parentNode);
        } catch (e) {
            console.error("Error applying highlight:", e);
        }
    }

    /**
     * Merges adjacent <span class="highlight"> elements within a parent container.
     * This function solves the overlapping highlight problem.
     * @param {Node} container The parent node to scan for highlights to merge.
     */
    function normalizeHighlights(container) {
        const highlights = container.querySelectorAll('.highlight');
        if (highlights.length < 2) return; // No need to merge if less than 2 highlights

        let changed = true;
        while(changed) {
            changed = false;
            const allNodes = Array.from(container.childNodes);

            for(let i = 0; i < allNodes.length - 1; i++) {
                const currentNode = allNodes[i];
                let nextNode = allNodes[i + 1];

                // Skip over empty text nodes that can separate spans
                while (nextNode && nextNode.nodeType === Node.TEXT_NODE && nextNode.textContent.trim() === '') {
                    const toRemove = nextNode;
                    nextNode = nextNode.nextSibling;
                    toRemove.remove(); // Clean up empty text nodes
                }

                if (currentNode.nodeType === Node.ELEMENT_NODE && currentNode.classList.contains('highlight') &&
                    nextNode && nextNode.nodeType === Node.ELEMENT_NODE && nextNode.classList.contains('highlight')) {
                    
                    // Merge the next node into the current one
                    currentNode.innerHTML += nextNode.innerHTML;
                    nextNode.remove();
                    
                    // Restart the process since we modified the DOM
                    changed = true;
                    break; 
                }
            }
        }
    }
});



    // // Store for annotations
    // let currentAnnotations = [];
    // let annotationId = 1000;

    // // Get the statement element
    // const statementBody = () => {
    //     return document.querySelector(".statement");
    // };

    // // Listen for text selection
    // const setupSelectionListener = () => {
    //     statementBody().addEventListener('mouseup', getSelectionInfo);
    // };

    // // Get selection info and send to server
    // const getSelectionInfo = async () => {
    //     const selection = window.getSelection();
    //     const selectedText = selection.toString().trim();
        
    //     if (selectedText.length > 0) {
    //         const newAnnotation = {
    //             id: ++annotationId,
    //             text: selectedText,
    //             start: selection.anchorOffset,
    //             end: selection.focusOffset
    //         };
            
    //         currentAnnotations.push(newAnnotation);
            
    //         // Send to Flask backend
    //         try {
    //             const response = await fetch("{{url_for('classes.individual_lesson', cid=results['cid'], lid=results['lid'])}}", {
    //                 method: 'POST',
    //                 headers: {
    //                     'Content-Type': 'application/json',
    //                 },
    //                 body: JSON.stringify(newAnnotation)
    //             });
                
    //             const result = await response.json();
    //             displayAnnotation(result);
    //         } catch (error) {
    //             console.error('Error:', error);
    //         }
    //     }
    // };

    // // Display the annotation
    // const displayAnnotation = (annotation) => {
    //     const list = document.getElementById('annotation-list');
    //     const item = document.createElement('li');
    //     item.textContent = `Annotation #${annotation.id}: "${annotation.text}"`;
    //     list.appendChild(item);
    // };
    
    // // highlight selected text
    // const highlightBody = () => {
    //     currentAnnotations.forEach(annotation => {
    //         let newStatementBody = spanSplicer(annotation);
    //         statementBody().innerHTML = newStatementBody;
    //     });
    // };

    // const spanSplicer = annotation => {
    //     const body = statementBody().innerHTML;
    //     const preSlice = body.slice(0, annotation.start)
    //     const span = `<span class="highlight">${body.slice(annotation.start, annotation.end)}</span>`
    //     const postSlice = body.slice(annotation.end)
    //     return preSlice.concat(span, postSlice)
    // }

    // // Initialize when page loads
    // document.addEventListener('DOMContentLoaded', setupSelectionListener);
