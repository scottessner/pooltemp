/**
 * Created by ssessner on 9/23/2015.
 */
var app = angular.module('app', ['tc.chartjs', 'ui.bootstrap']);

app.controller('MeasController', function($http){
   var app = this;

    $http.get('/api/meas').success(function(data){
        this.meas = data.objects;
    })



});