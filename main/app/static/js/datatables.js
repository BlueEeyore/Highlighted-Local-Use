/*
  This function formats the content for a child row.
  It takes the string from the 'data-child-content' attribute.
*/
function format(d) {
    return d;
}

$(document).ready(function() {
    
    // --- Standard Initialization for other tables ---
    if ($('#classes').length) {
        var classesTable = $('#classes').DataTable();
    }
    if ($('#lessons').length) {
        var lessonsTable = $('#lessons').DataTable();
    }

    // --- PROMINENT SEARCH Initialization for the 'join_classes' table ---
    if ($('#join_classes').length) {
        
        // 1. Get references to our custom elements
        const customSearchInput = $('#custom-search-input');

        // 2. Initialize the DataTable.
        //    'dom': 'lrtip' is important: it removes the default search box ('f').
        //    'l'=length, 'r'=processing, 't'=table, 'i'=info, 'p'=pagination
        var joinTable = $('#join_classes').DataTable({
            "dom": 'rtp' ,
            "columnDefs": [
                {
                    "orderable": false, // This disables sorting
                    "targets": 0,      // We are targeting the first column (index 0)
                }
            ],
            "pagingType": "simple" //removes pagination numbers
        });

        // 3. Attach a keyup event listener to OUR search box.
        customSearchInput.on('keyup', function() {
            // 4. On every keypress, apply the search to the DataTable.
            joinTable.search(this.value).draw();
        });

        // --- Event listener for the expand/collapse functionality ---
        $('#join_classes tbody').on('click', 'td.dt-control', function() {
            var tr = $(this).closest('tr');
            var row = joinTable.row(tr);

            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                var childContent = tr.data('child-content');
                row.child(format(childContent)).show();
                tr.addClass('shown');
            }
        });
    }

    //initialising classes table to have a scrollbar instead of just being as long as possible
    new DataTable('#classes', {
        searching: false,
        info: false,
        paging: false,
        scrollCollapse: true,
        scrollY: '300px'
    });


    // initialising lessons table to have a scrollbar instead of just being as long as possible
    new DataTable('#lessons', {
        searching: false,
        info: false,
        paging: false,
        scrollCollapse: true,
        scrollY: '300px'
    });
});


// // initialising the datatable on search page (with the expandable rows)
// var table = $("#search").DataTable(
//     {
//         responsive: true,
//         columnDefs: [ {
//             targets: 7,
//             render: $.fn.dataTable.render.ellipsis( 12 )
//         } ]
//     }
// );