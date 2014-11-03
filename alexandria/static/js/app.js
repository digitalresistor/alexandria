var app = angular.module('app', [
        'ngResource',
        'ngRoute'
        ]);


app.factory('csrfReset', ['$q', '$injector', '$browser', '$log', function($q, $injector, $browser, $log) {
    var csrfReset = {};

    csrfReset.responseError = function(response) {
        // When the CSRF token fails, we get back a new one in a cookie, retry
        // the request with the new token.
        if (response.status == 400 && typeof response.data.errors.csrf !== null) {
            $log.debug('CSRF token was invalid, going to re-run request');
            var $http = $injector.get('$http');
            var httpConfig = response.config;

            // Get the new xsrfValue from the cookies
            var xsrfValue = $browser.cookies()[$http.defaults.xsrfCookieName];

            if (xsrfValue) {
                httpConfig.headers[$http.defaults.xsrfHeaderName] = xsrfValue;
            }

            // Return the new request
            return $http(httpConfig);
        }

        return $q.reject(response);
    };

    return csrfReset;
}]);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRF-Token';
    $httpProvider.defaults.xsrfCookieName = 'CSRF-Token';
    $httpProvider.interceptors.push('csrfReset');
}]);

app.directive('serverError', function() {
    return {
        restrict: 'A',
        require: '?ngModel',
        link: function(scope, element, attrs, ctrl) {
            element.on('input', function() {
                scope.$apply(
                    function() {
                        ctrl.$setValidity('server', true);
                    })
                }
            );
        }
    };
});

