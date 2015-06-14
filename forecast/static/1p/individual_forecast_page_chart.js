$(document).ready(function (e) {
    var forecast_id = $('#peleus-individual-forecast').attr('forecast-id');
    $.ajax({
        url: "/forecasts/",
        method: 'GET',
        data:{
            id: forecast_id
        }

    }).done(function (data) {
        for (var i=0; i<data.length; i++){
            drawChart('#peleus-individual-forecast', data[i])
        }
    });
});
