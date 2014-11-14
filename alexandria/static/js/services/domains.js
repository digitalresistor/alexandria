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

        service.all = [];
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

        return service;
    }
]);
