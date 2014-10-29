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

        // ============= Watch =============
        $scope.user = User.getUser();
        $scope.isLoggedIn = User.getIsLoggedIn();
        $scope.$on('user', function(event) {
            $log.debug("User changed: {%o, %o}", User.getUser(), User.getIsLoggedIn());
            $scope.user = User.getUser();
            $scope.isLoggedIn = User.getIsLoggedIn();
        });
    }
]);
