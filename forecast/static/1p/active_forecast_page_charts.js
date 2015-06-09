$(document).ready(function (e) {
     console.log('hello');
    $.ajax({
        url: "/forecasts/",
        method: 'GET'

    }).done(function (data) {
        for (var i=0; i<data.length; i++) {
            (function (i) {
                $('#collapseOne-' + data[i].id).on('shown.bs.collapse', function () {
                    draw_timeseries_chart('#peleus-forecast-' + data[i].id, data[i].votes);
                }).on('hidden.bs.collapse', function () {
                    $('#peleus-forecast-' + data[i].id).empty();
                });
            })(i);
        }
    });
});
