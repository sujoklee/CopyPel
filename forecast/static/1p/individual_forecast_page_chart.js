$(document).ready(function (e) {
    var forecast_id = $('#peleus-individual-forecast').attr('forecast-id');
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
