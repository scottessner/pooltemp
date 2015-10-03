/**
 * Created by ssessner on 9/23/2015.
 */
(function(){
var app = angular.module('app', ['tc.chartjs', 'ui.bootstrap']);

    app.controller('MeasController', function($http) {
        var app = this;
        app.myvar = 'Hi World!';


        $http.get('/api/meas').success(function (data) {
            app.meas = data.objects;
        });
    });

})();