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

app.run(['$rootScope', '$log', 'User', function ($rootScope, $log, User) {
    $rootScope.user_not_checked = true;

    $rootScope.$on('$routeChangeStart', function(event, next, current) {

        // Check to see if the user is logged in ...
        if (!User.getIsLoggedIn()) {
            $log.debug('User is not logged in... changing html.');
            next.templateUrl = '/html/login.html';
            next.controller = 'LoginCtrl';
        } else {
            $log.debug('User is logged in. Continuing on.');
        }
    });
}]);

app.run(['$rootScope', '$log', '$route', 'User', function ($rootScope, $log, $route, User) {
    $rootScope.$on('user', function(event) {
        if ($rootScope.user_not_checked === true) {
            $rootScope.user_not_checked = false;

            if (!User.getIsLoggedIn()) return;
        }

        $route.reload();
    });
}]);
