$().ready(function() {
    $('#messclick').on('click', function() {

            $.ajax({
                url: "/messages/inbox/",
                method: 'GET'

            }).done(function(data) {
                $('#message').toggle('300').html(data);
                console.log(data);
            });

        //$('#SendMessage').on('shown.bs.modal', function() {
        //    $.ajax({
        //        url: "/profile_forecasts/{{ profile.id }}/",
        //        method: 'GET'
        //
        //    }).done(function(data) {
        //        $('#message-set-modal').html(data);
        //        $.ajax({
        //            url: "/messages/write/",
        //            method: 'GET'
        //        }).on('hidden.bs.modal', function() {
        //          $('#message-set-modal').empty()
        //        });
        });




    });




