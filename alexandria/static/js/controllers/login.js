app.controller('LoginCtrl', ['$scope', '$log', '$route', 'User',
    function($scope, $log, $route, User) {
        $scope.loginForm = {};
        $scope.errors = {};

        $scope.login = function() {
            $log.debug('Setting all the form fields to $dirty...');
            // Reset the errors list
            if ($scope.form.submitted == false) {
                $scope.errors = {};
            }

            angular.forEach($scope.form, function(ctrl, field) {
                // Dirty hack because $scope.form contains so much more than just the fields
                if (typeof ctrl === 'object' && ctrl.hasOwnProperty('$modelValue')) {
                    ctrl.$dirty = true;
                    ctrl.$pristine = false;

                    // Add a viewChangeListener, so that if the form is
                    // modified at all, we remove .submitted
                    ctrl.$viewChangeListeners.push($scope.modified);
                }
            });

            if ($scope.form.$invalid) {
                $log.debug('Form is invalid. Not sending request to server.')
                return;
            }

            $scope.form.submitted = true;

            $log.debug('Attempting to log user in...');
            User.login($scope.loginForm.email, $scope.loginForm.password).then(function(data) {
                $route.reload();
            }).catch(function(data) {
                $scope.errors = {};

                // Set the full form error
                $scope.errors['form_error'] = data.form_error;

                if (data.form_error === null) {
                    angular.forEach(data.errors, function(error, field) {
                        $scope.form[field].$setValidity('server', false);
                        $scope.errors[field] = error;
                    });
                }
            });
        };

        $scope.modified = function() {
            $scope.form.submitted = false;
        };
    }
]);

