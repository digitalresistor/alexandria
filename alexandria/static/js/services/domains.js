app.factory('DomainsFactory', ['$resource', function($resource) {
    return $resource('/domain/:id', { id: '@id' }, {
        update: {
            method: 'PUT'
        }
    });
}]);

app.service('Domains', ['$rootScope', '$log', '$q', 'DomainsFactory',
    function($rootScope, $log, $q, DomainsFactory) {
        var service = {};

        service.state = {};
        service.state.loaded = false;
        service.all = [];
        service.deleted_domains = [];

        service.query = function(ret_func) {
            if (service.all.length == 0) {
                $log.debug("Fetching list of domains.");
                service.all = DomainsFactory.query(ret_func);

                return service.all;
            }
            else {
                ret_func();
                return service.all;
            }
        };

        service.save = function(data, success, error) {
            DomainsFactory.save(data, function(value, responseHeader) {
                service.all.push(value);

                success(value, responseHeader);
            }, function(httpResponse) {
                error(httpResonse);
            });
        }

        service.delete = function(domain) {
            (function() {
                var domain_id = domain.id;

                angular.forEach(service.all, function(value, $index) {
                    if (domain_id == value.id) {
                        service.all.splice($index, 1);
                    }
                });

                service.deleted_domains.push(angular.copy(domain));

                domain.$delete(function(value, reponseHeader) {
                    angular.forEach(service.deleted_domains, function(value, $index) {
                        if (domain_id == value.id) {
                            service.deleted_domains.splice($index, 1);
                        }
                    });
                }, function(httpResponse) {
                    $log.error('Unable to delete domain entry. %o', httpResonse);
                });
            })();
        }

        $log.debug("Initialised Domains");

        service.query(function() {
            service.state.loaded = true;
        });

        return service;
    }
]);
