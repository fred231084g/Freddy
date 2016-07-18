angular.module('App', ['ui.router', 'ngResource', 'App.services', 'App.controllers','toaster', 'ngAnimate', 
                        'angular-google-analytics', 'ngSanitize', 'ezfb', 'ngRoute']);

angular.module('App.services', []);

// https://github.com/pc035860/angular-easyfb

angular.module('App').constant('SOCIAL_PLUGINS', ['comments']);

angular.module('App')
  .run( function($rootScope, $state){
                //$rootScope.$on('$stateChangeStart'
                $rootScope.$state = $state;
                $rootScope.$state.current.title = "Freddy by Leonard";
                }
    );

angular.module('App').config(function( $stateProvider , $urlRouterProvider, AnalyticsProvider, ezfbProvider, SOCIAL_PLUGINS, $routeProvider) {


    $urlRouterProvider.otherwise('/');

   // Google Analytics
    AnalyticsProvider.setAccount('UA-37519052-11');
    AnalyticsProvider.setDomainName('seven.leog.in');
	
   // https://github.com/pc035860/angular-easyfb
   
   ezfbProvider.setInitParams({
    appId: '115533011960122',
    version: 'v2.7'
  });
    
   angular.forEach(SOCIAL_PLUGINS, function (dirTag) {
    var routeName = dirTag;
    
   $routeProvider.when('/' + routeName, {
      templateUrl: routeName + '.html'
    });
  });
  
 // https://github.com/pc035860/angular-easyfb 
   
 
$stateProvider.state('index', {
        // Note: abstract state cannot be loaded, but it still needs a ui-view for its children to populate.
        // https://github.com/angular-ui/ui-router/wiki/Nested-States-and-Nested-Views
        // abstract: true,
        url: '/',
        templateUrl: 'posts.html',
        title: 'Freddy',
        controller: 'AllPostsController'
    })

  .state('post', {
    url: '/:slug',
    params: {
         id : null
        },

    templateUrl: 'post.html',
    controller: 'SinglePostController'


    });

    });

angular.module('App.services').factory('ReadPost', function($resource, $stateParams) {
  return $resource('api/v1/r/posts/:id.json', { id:'@posts.id' }, {
    update: {
      method: 'PATCH',


    }
    }, {
    stripTrailingSlashes: false
    });
});

angular.module('App.services').factory('ReadTerms', function($resource, $stateParams) {
  return $resource('api/v1/r/posts/terms.json', { }, {
    update: {
      method: 'PATCH',


    }
    }, {
    stripTrailingSlashes: false
    });
});

angular.module('App.controllers', []);
angular.module('App.controllers').controller('AllPostsController', function($scope, $state,  ReadPost, ReadTerms, toaster) {

        ReadPost.get(function(data) {
                     $scope.posts = [];
                     angular.forEach(data.data, function(value, key)
                                                        {
                                                       this.post = value.attributes;
                                                       this.post['id'] = value.id;
                                                       this.push(this.post);
                                                        },   $scope.posts);

                              }, 
                function(error){
                      toaster.pop({
                                                type: 'error',
                                                title: 'Error',
                                                body: error,
                                                showCloseButton: true,
                                                timeout: 0
                                                });
                                              });
	     ReadTerms.get(function(data) {
                     $scope.terms = [];
                     angular.forEach(data.data, function(value, key)
                                                        {
                                                       this.term = value.attributes;
                                                       this.term['id'] = value.id;
                                                       this.push(this.term);
                                                        },   $scope.terms);

                              }, 
                function(error){
                      toaster.pop({
                                                type: 'error',
                                                title: 'Error',
                                                body: error,
                                                showCloseButton: true,
                                                timeout: 0
                                                });
                                              });

}).controller('SinglePostController', function($scope, $state, $stateParams, ReadPost, toaster, SOCIAL_PLUGINS) {



                       $scope.post = ReadPost.get({ id: $stateParams.id },
                                       function() {}, function(error) {
                                          toaster.pop({
                                                type: 'error',
                                                title: 'Error',
                                                body: error,
                                                showCloseButton: true,
                                                timeout: 0
                                                });
                                                });
												
												
                    // Fb comments
					
					
					 $scope.SOCIAL_PLUGINS = SOCIAL_PLUGINS;
  
					  $scope.pluginOn = true;
					  $scope.rendering = false;
					  
					  $scope.goto = function (dirTag) {
						$location.path('/' + dirTag);
					  };
					  
					  $scope.isActive = function (dirTag) {
						return ($location.path() === '/' + dirTag);
					  };
					  
					  $scope.rendered = function () {
						$scope.rendering = false;
					  };
					  
					  $scope.$watch('pluginOn', function (newVal, oldVal) { 
						if (newVal !== oldVal) {
						  $scope.rendering = true;
						}
					  });
					  
					  $scope.$on('$routeChangeSuccess', function () {
						$scope.rendering = true;
					  });




 });
