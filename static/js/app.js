/**
 * Created by ssessner on 9/23/2015.
 */
(function() {
    var app = angular.module('app', ['tc.chartjs', 'ngMaterial']);

    app.controller('CurrentController', ['$http', '$scope', function($http, $scope) {

        var order_param = {"q":{"order_by":[{"field": "local_epoch", "direction": "desc"}],"limit": 1}};

        $http.get('/api/meas', {params: order_param}).success(function (data) {
            $scope.current = data;
            //$scope.latest = $scope.readings[0];
        });
    }]);

    app.controller('MeasController', ['$http', '$scope', function ($http, $scope) {
        var mctl = this;
        $scope.readings = [];

        var current_param = {"q":{"order_by":[{"field": "local_epoch", "direction": "desc"}],"limit": 1}};

        var history_param = {"q":{"order_by":[ {"field": "local_epoch", "direction": "desc"}]}};

        $scope.load = function(params){

            $http.get('/api/meas', {params: params}).success(function (data) {
                $scope.readings = data.objects;
                $scope.current = $scope.readings[0];
            });
        };

        $scope.load(current_param);

        $scope.loadHistory = function(){
            $scope.load(history_param);
        };

    }]);

    app.directive('measTable', function(){
        return{
            restrict: 'E',
            templateUrl: 'elements/meas-table.html'

        };
    });

    app.config(function($mdThemingProvider){
       $mdThemingProvider.theme('default')
           .primaryPalette('blue');
    });

})();