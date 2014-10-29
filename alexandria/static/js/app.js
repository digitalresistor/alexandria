var app = angular.module('app', [
        'ngResource',
        'ngRoute'
        ]);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRF-Token';
    $httpProvider.defaults.xsrfCookieName = 'CSRF-Token';
}]);
