app.controller('DomainsCtrl', ['$scope', '$log', 'Domains',
    function($scope, $log, Domains) {
        $scope.domains = Domains.query();
    }
]);


