/**
 * Created by ssessner on 9/23/2015.
 */
(function() {
    var app = angular.module('app', ['tc.chartjs', 'ngMaterial'])

    app.controller('MeasController', ['$http', '$scope', function ($http, $scope) {
        var mctl = this;
        $scope.readings = [];

        var order_param = {"q":{"order_by":[ {"field": "local_epoch", "direction": "desc"}]}};

        $http.get('/api/meas', {params: order_param}).success(function (data) {
            $scope.readings = data.objects;
            $scope.latest = $scope.readings[0];
        });

        $scope.shown = 0;

        this.showTable = function(){
            if($scope.shown)
                $scope.shown = 0;
            else
                $scope.shown = 1;
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