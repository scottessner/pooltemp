/**
 * Created by ssessner on 9/23/2015.
 */
(function() {
    var app = angular.module('app', ['tc.chartjs', 'ui.bootstrap']);

    app.controller('MeasController', ['$http', function ($http) {
        var mctl = this;
        mctl.readings = [];

        $http.get('/api/meas').success(function (data) {
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