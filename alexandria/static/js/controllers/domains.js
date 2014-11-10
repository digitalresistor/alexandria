app.controller('DomainsCtrl', ['$scope', '$log', 'Domains',
    function($scope, $log, Domains) {
        $scope.domains = Domains.query();
        $scope.newDomainForm = {}

        $scope.newDomainSubmit = function() {
            $log.debug('Setting all the newDomain fields to $dirty...');
            // Reset the errors list
            if ($scope.newDomain.submitted == false) {
                $scope.errors = {};
            }

            angular.forEach($scope.newDomain, function(ctrl, field) {
                // Dirty hack because $scope.newDomain contains so much more than just the fields
                if (typeof ctrl === 'object' && ctrl.hasOwnProperty('$modelValue')) {
                    ctrl.$dirty = true;
                    ctrl.$pristine = false;

                    // Add a viewChangeListener, so that if the newDomain is
                    // modified at all, we remove .submitted
                    ctrl.$viewChangeListeners.push($scope.modified);
                }
            });

            if ($scope.newDomain.$invalid) {
                $log.debug('Form is invalid. Not sending request to server.');
                return;
            }

            $scope.newDomain.submitted = true;

            $log.debug('Attempting to save domain');

            Domains.save($scope.newDomainForm, function(value, responseHeader) {
                $scope.domains.push($scope.newDomainForm);
                $scope.newDomainForm = {};
                $scope.newDomain.$setPristine();
            }, function(httpResponse) {
                data = httpResponse.data;
                $scope.errors = {};

                // Set the full form error
                $scope.errors['form_error'] = data.form_error;

                if (data.form_error === null) {
                    angular.forEach(data.errors, function(error, field) {
                        $scope.newDomain[field].$setValidity('server', false);
                        $scope.errors[field] = error;
                    });
                }
            });
        };

        $scope.modified = function() {
            $scope.newDomain.submitted = false;
        };
    }
]);


