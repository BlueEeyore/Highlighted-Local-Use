// //initialising join_classes table to have a scrollbar instead of just being as long as possible
// new DataTable('#join_classes', {
//     searching: false,
//     info: false,
//     paging: false,
//     scrollCollapse: true,
//     scrollY: '300px'
// });

let table = new DataTable('#join_classes', {
    columns: [
        {
            className: 'dt-control',
            orderable: false,
            data: null,
            defaultContent: ''
        },
        { orderable: true },    //name column
        { orderable: true }     //school column
    ],
    order: [[1, 'asc']]
});

// Add event listener for opening and closing details
table.on('click', 'tbody td.dt-control', function (e) {
    let tr = e.target.closest('tr');
    let row = table.row(tr);

    if (row.child.isShown()) {
        // This row is already open - close it
        row.child.hide();
    }
    else {
        // Get the content from the data- attribute
        let childContent = $(tr).data('child-content');
        // Open this row using the content from the attribute
        row.child(childContent).show();
    }
});


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