app.controller('LoginCtrl', ['$scope', '$log', '$route', 'User',
    function($scope, $log, $route, User) {
        $scope.loginForm = {};

        $scope.login = function() {
            User.login($scope.loginForm.email, $scope.loginForm.password).then(function(data) {
                $route.reload();
            }).catch(function(data) {
                $log.debug('Unable to log user in...');
            });
        };
    }
]);

