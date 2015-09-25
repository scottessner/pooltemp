/**
 * Created by ssessner on 9/23/2015.
 */
var app = angular.module('app', ['tc.chartjs', 'ui.bootstrap']);

app.controller('MeasCtrl', function($http){
   var app = this;

    $http.get('/api/meas').success(function(data){
        this.meas = data.objects;
    })



});