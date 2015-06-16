$(document).ready(function () {
    var choices = $('#choices-group');
    var forecastType = $('#id_forecast_type');

    function triggerChoices() {
        if($(forecastType).val() == '1') {
            choices.show()
        } else {
            choices.hide()
        }
    }

    triggerChoices();

    $(forecastType).change(triggerChoices)
        .on('keyup keydown', function () { $(this).trigger('change') });
});