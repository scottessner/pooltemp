/**
 * Created by ssessner on 9/23/2015.
 */
(function(){
var app = angular.module('app', ['tc.chartjs', 'ui.bootstrap']);

    app.controller('MeasController', function($http) {
        this.myvar = 'Hi World!';


        $http.get('/api/meas').success(function (data) {
            this.meas = data.objects;
        });
    });

})();