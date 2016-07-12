angular.module('myApp.services').factory('Post', function($resource) {
  return $resource('api/v1/posts/:id.json', { id:'@posts.id' }, {
    update: {
      method: 'PATCH',



    }
    }, {
    stripTrailingSlashes: false
    });
});


angular.module('myApp.controllers').controller('PostListController', function($scope, $state,  Post, $auth, toaster) {
 //Table header definitions
        var columnDefs = [ {headerName: "Sr No", cellRenderer: function(params) {return params.node.id + 1;} },
                             {headerName: "author", field: "author", width: 300 },{headerName: "title", field: "title", width: 300 },{headerName: "slug", field: "slug", width: 300 },
                             {headerName: "date", field: "date", width: 300 },{headerName: "date_gmt", field: "date_gmt", width: 300 },
                             {headerName: "content", field: "content", width: 300 },{headerName: "excerpt", field: "excerpt", width: 300 },
                             {headerName: "status", field: "status", width: 300 },{headerName: "modified", field: "modified", width: 300 },
                             {headerName: "modified_gmt", field: "modified_gmt", width: 300 },{headerName: "type", field: "type", width: 300 },
                             {headerName: "parent", field: "parent", width: 300 },{headerName: "terms", field: "tags", width: 300 },
                             {headerName: "comments", field: "comments", width: 300 },{headerName: "image", field: "path", width: 300 }


                            ];
        $scope.gridOptions = { columnDefs: columnDefs,
                               rowData: null,
                               enableSorting: true,
                               enableColResize: true,
                               rowSelection: 'single',};
        Post.get(function(data) {
                     $scope.posts = [];
                     angular.forEach(data.data, function(value, key)
                                                        {
                                                       this.post = value.attributes;
                                                       this.post['id'] = value.id;
                                                       this.post['tags'] = value.tags;
                                                       this.push(this.post);
                                                        },   $scope.posts);
                    $scope.gridOptions.rowData = $scope.posts;
                    $scope.gridOptions.api.onNewRows();
                    $scope.gridOptions.api.sizeColumnsToFit();
                               },
                function(error){
                      $scope.error = error.data;
                                              });


   $scope.deletePost = function(selected_id) { // Delete a Post. Issues a DELETE to /api/posts/:id
      post = Post.get({ id: selected_id});
      post.$delete({ id: selected_id},function() {
        toaster.pop({
                type: 'success',
                title: 'Sucess',
                body: "Post deleted successfully",
                showCloseButton: true,
                timeout: 0
                });

        $state.reload();
      }, function(error) {
         toaster.pop({
                type: 'error',
                title: 'Error',
                body: error,
                showCloseButton: true,
                timeout: 0
                });;
    });
    };

}).controller('PostEditController', function($scope, $state, $stateParams, toaster, $window, Post, Gallery, Term) {
     $scope.loading = false;

     $scope.updatePost = function() { //Update the post. Issues a PATCH to /v1/api/posts/:id

     $scope.loading = true;
    $scope.post.$update({ id: $stateParams.id },function() {
     toaster.pop({
                type: 'success',
                title: 'Sucess',
                body: "Update was a success",
                showCloseButton: true,
                timeout: 0
                });

       $state.go('posts.list');
       $scope.loading = false;
      //$state.go('sites'); // on success go back to home i.e. sites state.
    }, function(error) {
    toaster.pop({
                type: 'error',
                title: 'Error',
                body: error,
                showCloseButton: true,
                timeout: 0
                });
      $scope.loading = false;
    });
  };


  $scope.loadPost = function() { //Issues a GET request to /api/posts/:id to get a post to update
                       $scope.post = Post.get({ id: $stateParams.id },
                                       function() {}, function(error) {
                                          toaster.pop({
                                                type: 'error',
                                                title: 'Error',
                                                body: error,
                                                showCloseButton: true,
                                                timeout: 0
                                                });
                                                });

                                };

  $scope.loadPost(); // Load a post



  // Gallery

        var columnDefs = [ {headerName: "Sr No", cellRenderer: function(params) {return params.node.id + 1;} },
                             {headerName: "name", field: "name" },

                             {headerName: "Pic", width: 400,
                                cellRenderer: function(params) {
                                                return '<img src="'+params.data.path+'"  height="100" width="500">'
                                                       ;
                                                    } }



                            ];
        $scope.gridOptions = { columnDefs: columnDefs,
                               rowData: null,
                               enableSorting: true,
                               enableColResize: true,
                               rowSelection: 'single',};
        Gallery.get(function(data) {
                     $scope.files = [];
                     angular.forEach(data.data, function(value, key)
                                                        {
                                                       this.file = value.attributes;
                                                       this.file['id'] = value.id;
                                                       this.push(this.file);
                                                        },   $scope.files);
                    $scope.gridOptions.rowData = $scope.files;
                    $scope.gridOptions.api.onNewRows();
                    $scope.gridOptions.api.sizeColumnsToFit();

                               },
                function(error){
                      $scope.error = error.data;
                                              });

        // Terms

        Term.get(function(data) {

                  $scope.terms = [];
                  angular.forEach(data.data, function(value, key) {


                                                       this.term = value.attributes;

                                                           this.term['id'] = value.id;
                                                           this.push(this.term);
                                                        },   $scope.terms);







                })



}).controller('PostCreateController', function($scope, $state, Post, Gallery, Term, toaster) {
          $scope.post = new Post();
          $scope.loading = false;

         $scope.addPost = function() { //Issues a POST to v1/api/post.json
                                $scope.loading = true;
                                $scope.post.data.type = "posts";
                                $scope.post.data.attributes.type ="post";
                                $scope.post.data.attributes.parent = 0;
                                $scope.post.$save(function() {
                                toaster.pop({
                                            type: 'success',
                                            title: 'Sucess',
                                            body: "Post saved successfully",
                                            showCloseButton: true,
                                            timeout: 0
                                            });
                                   $state.go('posts.list');
                                   $scope.loading = false;
                                }, function(error) {
                                toaster.pop({
                                            type: 'error',
                                            title: 'Error',
                                            body: error,
                                            showCloseButton: true,
                                            timeout: 0
                                            });
                                 $scope.loading = false;
                                           });
                                 };


        // Gallery

        var columnDefs = [ {headerName: "Sr No", cellRenderer: function(params) {return params.node.id + 1;} },
                             {headerName: "name", field: "name" },

                             {headerName: "Pic", width: 400,
                                cellRenderer: function(params) {
                                                return '<img src="'+params.data.path+'"  height="100" width="500">'
                                                       ;
                                                    } }



                            ];
        $scope.gridOptions = { columnDefs: columnDefs,
                               rowData: null,
                               enableSorting: true,
                               enableColResize: true,
                               rowSelection: 'single',
                               };
        Gallery.get(function(data) {
                     $scope.files = [];
                     angular.forEach(data.data, function(value, key)
                                                        {
                                                       this.file = value.attributes;
                                                       this.file['id'] = value.id;
                                                       this.push(this.file);
                                                        },   $scope.files);
                    $scope.gridOptions.rowData = $scope.files;
                    $scope.gridOptions.api.onNewRows();
                    $scope.gridOptions.api.sizeColumnsToFit();

                               },
                function(error){
                      $scope.error = error.data;
                                              });

        // Terms

        Term.get(function(data) {

                  $scope.terms = [];
                  angular.forEach(data.data, function(value, key) {


                                                       this.term = value.attributes;

                                                           this.term['id'] = value.id;
                                                           this.push(this.term);
                                                        },   $scope.terms);







                })


});
