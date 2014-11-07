app.controller('DomainsCtrl', ['$scope', 'Domains',
    function($scope, Domains) {
        $scope.domains = Domains.query();
    }
]);


