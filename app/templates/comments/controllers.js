angular.module('myApp.services').factory('Comment', function($resource) {
  return $resource('api/v1/comments/:id.json', { id:'@comments.id' }, {
    update: {
      method: 'PATCH',
      
     
     
    }
    }, {
    stripTrailingSlashes: false
    });
});


angular.module('myApp.controllers').controller('CommentListController', function($scope, $state,  Comment, $auth, toaster) {
 //Table header definitions  
        var columnDefs = [ {headerName: "Sr No", cellRenderer: function(params) {return params.node.id + 1;} },
                             {headerName: "post_id", field: "post_id", width: 300 },{headerName: "author_name", field: "author_name", width: 300 },{headerName: "author_email", field: "author_email", width: 300 },{headerName: "author_url", field: "author_url", width: 300 },{headerName: "created_on", field: "created_on", width: 300 },{headerName: "content", field: "content", width: 300 },{headerName: "karma", field: "karma", width: 300 },{headerName: "approved", field: "approved", width: 300 },{headerName: "agent", field: "agent", width: 300 },{headerName: "type", field: "type", width: 300 },{headerName: "parent", field: "parent", width: 300 },
                            
                            
                            ];
        $scope.gridOptions = { columnDefs: columnDefs,
                               rowData: null,
                               enableSorting: true,
                               enableColResize: true,
                               rowSelection: 'single',};  
        Comment.get(function(data) {
                     $scope.comments = [];
                     angular.forEach(data.data, function(value, key)
                                                        {
                                                       this.comment = value.attributes;
                                                       this.comment['id'] = value.id;
                                                       this.push(this.comment);                    
                                                        },   $scope.comments); 
                    $scope.gridOptions.rowData = $scope.comments;
                    $scope.gridOptions.api.onNewRows();
                    $scope.gridOptions.api.sizeColumnsToFit();
                               }, 
                function(error){
                      $scope.error = error.data;
                                              });
  
  
   $scope.deleteComment = function(selected_id) { // Delete a Comment. Issues a DELETE to /api/comments/:id
      comment = Comment.get({ id: selected_id});
      comment.$delete({ id: selected_id},function() {
        toaster.pop({
                type: 'success',
                title: 'Sucess',
                body: "Comment deleted successfully",
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
  
}).controller('CommentEditController', function($scope, $state, $stateParams, toaster, $window, Comment) {
     $scope.loading = false;
     $scope.updateComment = function() { //Update the comment. Issues a PATCH to /v1/api/comments/:id
     
     $scope.loading = true;
    $scope.comment.$update({ id: $stateParams.id },function() {
     toaster.pop({
                type: 'success',
                title: 'Sucess',
                body: "Update was a success",
                showCloseButton: true,
                timeout: 0
                });
        
       $state.go('comments.list');
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

  
  $scope.loadComment = function() { //Issues a GET request to /api/comments/:id to get a comment to update
                       $scope.comment = Comment.get({ id: $stateParams.id },
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

  $scope.loadComment(); // Load a comment 
  }).controller('CommentCreateController', function($scope, $state, Comment, toaster) {
          $scope.comment = new Comment(); 
          $scope.loading = false;

         $scope.addComment = function() { //Issues a POST to v1/api/comment.json
                                $scope.loading = true;
                                $scope.comment.data.type = "comments";
                                $scope.comment.$save(function() {
                                toaster.pop({
                                            type: 'success',
                                            title: 'Sucess',
                                            body: "Comment saved successfully",
                                            showCloseButton: true,
                                            timeout: 0
                                            });
                                   $state.go('comments.list');
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
});




  