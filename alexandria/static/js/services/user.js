app.service('User', ['$rootScope', '$q', '$http',
    function($rootScope, $q, $http) {
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
                    return user.authenticated;
                } else {
                    service.resetService();
                    return false;
                }
            },

            getIsLoggedIn: function() {
                return service.isLoggedIn;
            },

            checkLoggedIn: function() {
                var deferred = $q.defer();

                $http.get('/user').success(function(data, status, headers, config) {
                    if (status == 200) {
                        deferred.resolve(service.setUser(data));
                    } else {
                        service.resetService();
                        deffered.reject(false);
                    }
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
                    // Reset locally cached user information
                    service.resetService();
                    deferred.resolve(data);
                }).error(function(data, status, headers, config) {
                    deferred.reject(data);
                }.bind(this));

                return deferred.promise;
            },
        };

        return service;
    }
]);
