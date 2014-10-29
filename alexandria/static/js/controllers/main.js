app.controller('MainCtrl', ['$scope', '$route', '$log', 'User',
    function($scope, $route, $log, User) {
        $scope.logout = function(event) {
            User.logout().then(function(data) {
                $log.debug('User has been logged out...');
            }).catch(function(data) {
                $log.debug('Unable to log user out...');
            });

        }
    }
]);
