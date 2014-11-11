app.controller('DomainsCtrl', ['$scope', '$log', 'Domains',
    function($scope, $log, Domains) {
        $scope.domains_loaded = false;
        $scope.domains = Domains.query(function(value, responseHeader) {
            $scope.domains_loaded = true;
        });
        $scope.deleted_domains = []

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
                $scope.domains.push(value);
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

        $scope.deleteDomain = function(domain) {
            (function() {
                var domain_id = domain.id;

                angular.forEach($scope.domains, function(value, $index) {
                    if (domain_id == value.id) {
                        $scope.domains.splice($index, 1);
                    }
                });

                $scope.deleted_domains.push(angular.copy(domain));

                domain.$delete(function(value, reponseHeader) {
                    angular.forEach($scope.deleted_domains, function(value, $index) {
                        if (domain_id == value.id) {
                            $scope.deleted_domains.splice($index, 1);
                        }
                    });
                }, function(httpResponse) {
                    $log.error('Unable to delete domain entry. %o', httpResonse);
                });
            })();
        };

        $scope.modified = function() {
            $scope.newDomain.submitted = false;
        };
    }
]);


