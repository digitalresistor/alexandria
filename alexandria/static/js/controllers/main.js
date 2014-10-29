app.controller('MainCtrl', ['$scope', '$route', '$log', 'User',
    function($scope, $route, $log, User) {
        $scope.initMain = function() {
            $scope.checkLoggedIn();
        };

        $scope.checkLoggedIn = function() {
            User.checkLoggedIn().then(function(data) {
                $log.debug("User logged in: %o", data);
            }).catch(function(data) {
                $log.error("Checking to see if we are logged in failed, hard!");
            });
        };

        $scope.logout = function(event) {
            User.logout().then(function(data) {
                $log.debug('User has been logged out...');
            }).catch(function(data) {
                $log.debug('Unable to log user out...');
            });

        }
    }
]);
