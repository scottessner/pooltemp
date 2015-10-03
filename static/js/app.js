/**
 * Created by ssessner on 9/23/2015.
 */
(function(){
var app = angular.module('app', ['tc.chartjs', 'ui.bootstrap']);

    app.controller('MeasController', ['$scope', '$filter', '$http', function($scope, $filter, $http) {

        var orderBy = $filter('orderBy');

        $http.get('/api/meas').success(function (data) {
            $scope.meas = data.objects;
            $scope.meas = orderBy($scope.meas, '-local_epoch');
            $scope.latest = $scope.meas[0];
            //app.current = $filter('orderBy')(app.meas,'-local_epoch')[this.data.length-1].local_epoch ;
        });

        //$scope.latest = $scope.meas[0];


    }]);

})();