(function(){
    var app = angular.module('forecast', ['ngCookies', 'checklist-model']).
    config(function($interpolateProvider){
        $interpolateProvider.startSymbol('__').endSymbol('__');
    });

    app.service('formService', ['$http', '$cookies', function($http, $cookies){
        this.send = function(url, data){
            var result = $http({
                method: 'POST',
                url: url,
                data: $.param(data),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': $cookies.csrftoken
                }
            })
            return result;
        }
    }]);

    app.controller('signupFormController', ['formService', function(formService){
        var form = this;
        form.data ={'display_only_username': '0', 'agree_with_terms': '0'};
        form.errors = null;
        form.submit = function(url){
            formService.send(url, form.data).then(function(res){
                var data = res.data;
                password = form.data.password;
                password_conf = form.data.password_conf;
                agree = form.data.agree_with_terms;
                display_only_username = form.data.display_only_username;
                if (data.form == 'invalid'){
                    data.form_data.forecast_areas = list_str2int(data.form_data.forecast_areas);
                    data.form_data.forecast_regions = list_str2int(data.form_data.forecast_regions);
                    form.data = data.form_data;
                    form.data.password = password;
                    form.data.password_conf = password_conf;
                    form.data.agree_with_terms = agree;
                    form.data.display_only_username = display_only_username;
                    form.errors = data.errors;
                }
                else
                    if (data.form == 'valid')
                        window.location = data.location;
            });
        };
    }]);
})();