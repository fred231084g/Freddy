angular.module('myApp.services').factory('Term', function($resource) {
  return $resource('api/v1/terms/:id.json', { id:'@terms.id' }, {
    update: {
      method: 'PATCH',
      
     
     
    }
    }, {
    stripTrailingSlashes: false
    });
});


angular.module('myApp.controllers').controller('TermListController', function($scope, $state,  Term, $auth, toaster) {
 //Table header definitions  
        var columnDefs = [ {headerName: "Sr No", cellRenderer: function(params) {return params.node.id + 1;} },
                             {headerName: "name", field: "name", width: 300 },{headerName: "slug", field: "slug", width: 300 },{headerName: "description", field: "description", width: 300 },{headerName: "taxonomy", field: "taxonomy", width: 300 },{headerName: "parent", field: "parent", width: 300 },
                            
                            
                            ];
        $scope.gridOptions = { columnDefs: columnDefs,
                               rowData: null,
                               enableSorting: true,
                               enableColResize: true,
                               rowSelection: 'single',};  
        Term.get(function(data) {
                     $scope.terms = [];
                     angular.forEach(data.data, function(value, key)
                                                        {
                                                       this.term = value.attributes;
                                                       this.term['id'] = value.id;
                                                       this.push(this.term);                    
                                                        },   $scope.terms); 
                    $scope.gridOptions.rowData = $scope.terms;
                    $scope.gridOptions.api.onNewRows();
                    $scope.gridOptions.api.sizeColumnsToFit();
                               }, 
                function(error){
                      $scope.error = error.data;
                                              });
  
  
   $scope.deleteTerm = function(selected_id) { // Delete a Term. Issues a DELETE to /api/terms/:id
      term = Term.get({ id: selected_id});
      term.$delete({ id: selected_id},function() {
        toaster.pop({
                type: 'success',
                title: 'Sucess',
                body: "Term deleted successfully",
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
  
}).controller('TermEditController', function($scope, $state, $stateParams, toaster, $window, Term) {
     $scope.loading = false;
     $scope.updateTerm = function() { //Update the term. Issues a PATCH to /v1/api/terms/:id
     
     $scope.loading = true;
    $scope.term.$update({ id: $stateParams.id },function() {
     toaster.pop({
                type: 'success',
                title: 'Sucess',
                body: "Update was a success",
                showCloseButton: true,
                timeout: 0
                });
        
       $state.go('terms.list');
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

  
  $scope.loadTerm = function() { //Issues a GET request to /api/terms/:id to get a term to update
                       $scope.term = Term.get({ id: $stateParams.id },
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

  $scope.loadTerm(); // Load a term 
  }).controller('TermCreateController', function($scope, $state, Term, toaster) {
          $scope.term = new Term(); 
          $scope.loading = false;

         $scope.addTerm = function() { //Issues a POST to v1/api/term.json
                                $scope.loading = true;
                                $scope.term.data.type = "terms";
                                $scope.term.data.attributes.parent = 0;
                                $scope.term.$save(function() {
                                toaster.pop({
                                            type: 'success',
                                            title: 'Sucess',
                                            body: "Term saved successfully",
                                            showCloseButton: true,
                                            timeout: 0
                                            });
                                   $state.go('terms.list');
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




  