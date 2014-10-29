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
    $rootScope.user_not_checked = true;
    $rootScope.user = User.getUser();
    $rootScope.isLoggedIn = User.getIsLoggedIn();

    // Fetch user data/auth state
    User.checkLoggedIn().then(function(data) {
        $log.debug('checkLoggedIn succeeded.');
    }).catch(function(data) {
        $log.error('checkLoggedIn failed.');
    });

    $rootScope.$on('$routeChangeStart', function(event, next, current) {
        // We don't want to start routing until we have checked the user...
        if ($rootScope.user_not_checked) {
            event.preventDefault();
            return;
        }

        // Check to see if the user is logged in ...
        if (!User.getIsLoggedIn()) {
            $log.debug('User is not logged in: forceably changing template/controller.');
            next.templateUrl = '/html/login.html';
            next.controller = 'LoginCtrl';
        }
    });

    $rootScope.$on('user', function(event) {
        if ($rootScope.user_not_checked === true) {
            $rootScope.user_not_checked = false;
        }

        $rootScope.user = User.getUser();
        $rootScope.isLoggedIn = User.getIsLoggedIn();
        $route.reload();
    });
}]);
