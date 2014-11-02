app.controller('LoginCtrl', ['$scope', '$log', '$route', 'User',
    function($scope, $log, $route, User) {
        $scope.loginForm = {};
        $scope.errors = {};

        $scope.login = function() {
            $log.debug('Setting all the form fields to $dirty...')

            angular.forEach($scope.form, function(ctrl, field) {
                // Dirty hack because $scope.form contains so much more than just the fields
                if (typeof ctrl === 'object' && ctrl.hasOwnProperty('$modelValue')) {
                    ctrl.$dirty = true;
                }
            });

            if ($scope.form.$valid == false) {
                $log.debug('Form is invalid. Not sending request to server.')
                return;
            }

            $log.debug('Attempting to log user in...');
            User.login($scope.loginForm.email, $scope.loginForm.password).then(function(data) {
                $route.reload();
            }).catch(function(data) {
                $log.debug('Unable to log user in... %o', data);

                $scope.errors = {}

                angular.forEach(data.errors, function(error, field) {
                    $scope.form[field].$setValidity('server', false);
                    $scope.errors[field] = error;
                });
            });
        };
    }
]);

