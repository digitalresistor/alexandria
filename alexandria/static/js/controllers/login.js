app.controller('LoginCtrl', ['$scope', '$log', '$route', 'User',
    function($scope, $log, $route, User) {
        $scope.loginForm = {};
        $scope.errors = {};

        $scope.login = function() {
            $log.debug('Attempting to log user in...');
            User.login($scope.loginForm.email, $scope.loginForm.password).then(function(data) {
                $route.reload();
            }).catch(function(data) {
                $log.debug('Unable to log user in... %o', data);

                angular.forEach(data.errors, function(error, field) {
                    $scope.form[field].$setValidity('server', false);
                    $scope.errors[field] = error;
                });
            });
        };
    }
]);
