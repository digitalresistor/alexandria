app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    var rp = $routeProvider;

    rp.when('/', {
        templateUrl: '/html/home.html',
        controller: 'HomeCtrl',
    });

    rp.otherwise({
        redirectTo: '/'
    });

    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
    });
}]);

app.run(['$rootScope', '$log', '$route', 'User', function ($rootScope, $log, $route, User) {
    $rootScope.$on('user', function(event) {
        $route.reload();
    });
}]);
