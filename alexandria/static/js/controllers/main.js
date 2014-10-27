app.controller('MainCtrl', ['$scope', 'User',
        function($scope, User) {
            $scope.initMain = function() {
                $scope.checkLoggedIn();
            };

            $scope.checkLoggedIn = function() {
                User.checkLoggedIn().then(function(data) {
                    console.log("User logged in? %o", data);
                }).catch(function(data) {
                    console.error("ERROR! %o", data);
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
