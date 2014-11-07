<!DOCTYPE html>
<html lang="en" ng-app="app" ng-controller="MainCtrl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Alexandria</title>
<link rel="shortcut icon" href="${request.static_url('alexandria:static/favicon.ico')}">
<link rel="stylesheet" href="${request.static_url('alexandria:static/css/style.css')}" type="text/css" />
</head>

<body>
<header class="navigation">
    <div class="navigation-wrapper">
        <a href="javascript:void(0)" class="logo">
            <img src="https://raw.githubusercontent.com/thoughtbot/refills/master/source/images/placeholder_logo_1.png" alt="Logo Image">
        </a>
        <a href="" class="navigation-menu-button" id="js-mobile-menu" ng-show="isLoggedIn">MENU</a>
        <div class="nav" ng-show="isLoggedIn">
            <ul id="navigation-menu">
                <li class="nav-link"><a href="/">Home</a></li>
                <li class="nav-link"><a href="/domain">Domains</a></li>
            </ul>
        </div>
        <div class="navigation-tools" ng-show="isLoggedIn">
            <div class="search-bar">
                <div class="search-and-submit">
                    <input type="search" placeholder="Enter Search" />
                    <button type="submit">
                        <img src="https://raw.githubusercontent.com/thoughtbot/refills/master/source/images/search-icon.png" alt="Search Icon">
                    </button>
                </div>
            </div>
            <a href="" ng-click="logout()" class="button" ng-show="isLoggedIn">Logout</a>
        </div>
    </div>
</header>
<div class="container" ng-view>
</div>
<footer class="footer-2">
    <div class="footer-secondary-links">
        <ul>
            <li><a href="javascript:void(0)">Terms and Conditions</a></li>
            <li><a href="javascript:void(0)">Privacy Policy</a></li>
        </ul>
    </div>
</footer>

<!-- 3rd party libraries -->
<script type="text/javascript" src="${request.static_url('alexandria:static/js/3rdparty/angular/angular.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('alexandria:static/js/3rdparty/angular-resource/angular-resource.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('alexandria:static/js/3rdparty/angular-route/angular-route.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('alexandria:static/js/3rdparty/underscore/underscore-min.js')}"></script>
<!-- /3rd party libraries -->

<!-- application -->
<script type="text/javascript" src="${request.static_url('alexandria:static/js/app.js')}"></script>
<script type="text/javascript" src="${request.static_url('alexandria:static/js/router.js')}"></script>
<!-- /application -->

<!-- controllers -->
<script type="text/javascript" src="${request.static_url('alexandria:static/js/controllers/main.js')}"></script>
<script type="text/javascript" src="${request.static_url('alexandria:static/js/controllers/login.js')}"></script>
<script type="text/javascript" src="${request.static_url('alexandria:static/js/controllers/home.js')}"></script>
<script type="text/javascript" src="${request.static_url('alexandria:static/js/controllers/domains.js')}"></script>
<!-- /controllers -->

<!-- services -->
<script type="text/javascript" src="${request.static_url('alexandria:static/js/services/user.js')}"></script>
<script type="text/javascript" src="${request.static_url('alexandria:static/js/services/domains.js')}"></script>
<!-- /services -->

<!-- <script type="text/javascript" src="${request.static_url('alexandria:static/jquery-2.0.3.min.js')}"></script> -->
</body>
</html>

