$(document).ready(function (e) {
     console.log('hello');
    $.ajax({
        url: "/forecasts/",
        method: 'GET'

    }).done(function (data) {
        for (var i=0; i<data.length; i++){
            draw_timeseries_chart('#peleus-forecast-'+data[i].id, data[i].votes);
        }
    });
});
