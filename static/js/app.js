/**
 * Created by ssessner on 9/23/2015.
 */
(function(){
var app = angular.module('app', ['tc.chartjs', 'ui.bootstrap']);

    app.controller('MeasController', function($http, $filter) {
        var app = this;
        app.myvar = 'Hi World!';


        $http.get('/api/meas').success(function (data, $filter) {
            app.meas = data.objects;
            //app.current = $filter('orderBy')(app.meas,'-local_epoch')[this.data.length-1].local_epoch ;
        });
    });

})();