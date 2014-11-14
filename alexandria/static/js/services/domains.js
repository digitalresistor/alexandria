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

        service.query = function(ret_func) {
                service.domains = DomainsFactory.query(ret_func);
                return service.domains;
            }
        };

        return service;
    }
]);
