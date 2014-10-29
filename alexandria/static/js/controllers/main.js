app.controller('MainCtrl', ['$scope', '$log', 'User',
        function($scope, $log, User) {
            $scope.initMain = function() {
                $scope.checkLoggedIn();
            };

            $scope.checkLoggedIn = function() {
                User.checkLoggedIn().then(function(data) {
                    $log.debug("User logged in: %o", data);
                }).catch(function(data) {
                    $log.error("ERROR! %o", data);
                });
            };

            // ============= Watch =============
            $scope.user = User.getUser();
            $scope.$on('user.update', function(event) {
                $scope.user = User.getUser();
            });

            $scope.isLoggedIn = User.getIsLoggedIn();
            $scope.$on('user.loggedin.status', function(event) {
                $scope.isLoggedIn = User.getIsLoggedIn();
            });
        }
]);
