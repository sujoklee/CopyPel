$(document).ready(function (e) {
    $.ajax({
        url: "/forecasts/",
        method: 'GET'
        //async: false

    }).done(function (data) {
        for (var i=0; i<data.length; i++){
            draw_timeseries_chart('#peleus-individual-forecast', data[i].votes)
        }
    });
});
