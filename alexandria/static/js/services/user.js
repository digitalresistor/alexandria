app.service('User', ['$rootScope', '$q', '$http', '$log',
    function($rootScope, $q, $http, $log) {
        var service = {
            user: {},
            isLoggedIn: false,

            resetService: function() {
                service.user = {};
                service.isLoggedIn = false;
            },

            getUser: function() {
                return service.user;
            },

            setUser: function(user) {
                if (user && user.authenticated == true) {
                    service.user = user;
                    service.isLoggedIn = true;
                    $rootScope.$broadcast('user', user);
                    return true;
                } else {
                    service.resetService();
                    $rootScope.$broadcast('user', user);
                    return false;
                }
            },

            getIsLoggedIn: function() {
                return service.isLoggedIn;
            },

            checkLoggedIn: function() {
                var deferred = $q.defer();

                $http.get('/user').success(function(data, status, headers, config) {
                    ret = service.setUser(data);
                    deferred.resolve(ret);
                }).error(function(data, status, headers, config) {
                    service.resetService();
                    deferred.reject(data);
                });

                return deferred.promise;
            },

            login: function(username, password) {
                var deferred = $q.defer();

                $http.post('/user/login', {
                    username: username,
                    password: password,
                }).success(function(data, status, headers, config) {
                    $log.debug('User has been logged in...');
                    service.setUser(data);
                    deferred.resolve(data);
                }).error(function(data, status, headers, config) {
                    deferred.reject(data);
                });

                return deferred.promise;
            },

            logout: function() {
                var deferred = $q.defer();

                $http.post('/user/logout').success(function(data, status, headers, config) {
                    $log.debug('User has been logged out...');
                    service.setUser({});
                    deferred.resolve(true);
                }).error(function(data, status, headers, config) {
                    deferred.reject(false);
                }.bind(this));

                return deferred.promise;
            },
        };

        return service;
    }
]);
