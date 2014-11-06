app.service('Domains', ['$rootScope', '$q', '$resource', '$log',
    function($rootScope, $q, $resource, $log) {
        var service = {};

        return service;
    }
]);

app.factory('Domain', ['$resource', function($resource) {
    return $resource('/domain/:id'{ id: '@_id' }, {
        update: {
            method: 'PUT'
        }
    });
}]);
