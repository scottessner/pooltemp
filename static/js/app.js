/**
 * Created by ssessner on 9/23/2015.
 */
(function() {
    var app = angular.module('app', ['tc.chartjs', 'ui.bootstrap']);

    app.controller('MeasController', ['$http', function ($http) {
        var mctl = this;
        mctl.readings = [];

        var order_param = '"q":{"order_by":[ {"field": "local_epoch", "direction": "desc"}]}'

        $http.get('/api/meas', {params: order_param}).success(function (data) {
            mctl.readings = data.objects;
        });

        mctl.latest = mctl.readings[0];

    }]);

    app.directive('measTable', function(){
        return{
            restrict: 'E',
            templateUrl: 'elements/meas-table.html'

        }
     });

})();