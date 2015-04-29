$( document ).ready(function() {
    var heights = $(".row .form-panel").map(function() {
        return $(this).height();
    }).get(),

    maxHeight = Math.max.apply(null, heights);

    $(".row .form-panel").height(maxHeight);

    var row = $(".row-panel").parent();
    row.find(".panel").height(row.height() - 40);
});

$('.dropdown-menu').find('form').click(function (e) {
    e.stopPropagation();
  });

function list_str2int(arr){
    var int_list = [];
    if((arr !== []) && (arr instanceof Array))
        for(var k in arr)
            int_list.push(parseInt(arr[k]));
    return int_list;
}