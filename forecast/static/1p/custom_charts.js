function draw_timeseries_chart(selector, data) {
    var chart = c3.generate({
        bindto: selector,
        data: {
            json: data,
            keys: {
                x: 'date',
                value: ['avgVotes']
            },
            type: 'spline'
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%Y-%m-%d',
                    rotate: 80,
                    multiline: false
                }
            },
            y: {
                min: 0,
                max: 100,
                padding: {
                    top: 0,
                    bottom: 0
                }
            }
        }
    });
}

