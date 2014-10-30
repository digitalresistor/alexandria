var app = angular.module('app', [
        'ngResource',
        'ngRoute'
        ]);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRF-Token';
    $httpProvider.defaults.xsrfCookieName = 'CSRF-Token';
}]);

app.directive('serverError', function() {
    return {
        restrict: 'A',
        require: '?ngModel',
        link: function(scope, element, attrs, ctrl) {
            element.on('change', function() {
                scope.$apply(
                    function() {
                        ctrl.$setValidity('server', true);
                    })
                }
            );
        }
    };
});

