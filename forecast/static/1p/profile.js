$().ready(function() {
    $('#messclick').on('click', function() {

            $.ajax({
                url: "/messages/inbox/",
                method: 'GET'

            }).done(function(data) {
                $('#message').toggle('300').html(data);
                console.log(data);
            });


    });
    });

