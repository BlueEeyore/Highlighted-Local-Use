// initialising listing table on listing page to have a scrollbar instead of just being as long as possible
new DataTable('#classes', {
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