app.factory('Domains', ['$resource', function($resource) {
    return $resource('/domain/:id', { id: '@id' }, {
        update: {
            method: 'PUT'
        }
    });
}]);
