angular.module('myApp.services').factory('Gallery', function($resource) {
  function formDataObject (data) {
            var fd = new FormData();
            angular.forEach(data.data.attributes, function(value, key) {
                fd.append(key, value);
            });
            return fd;
        }
  return $resource('api/v1/gallery/:id.json', { id:'@gallery.id' }, {
    
    create: {
            method: "POST",
            transformRequest: formDataObject,
            headers: { 'Content-Type': undefined,  enctype:'multipart/form-data' }
        },
    update: {
      method: 'PATCH', 
      transformRequest: formDataObject,
      headers: { 'Content-Type': undefined,  enctype:'multipart/form-data' }      
     
    }
    }, {
    stripTrailingSlashes: false
    });
    
   
});


angular.module('myApp.controllers').controller('GalleryListController', function($scope, $state,  Gallery, $auth, toaster) {
 //Table header definitions  
        var columnDefs = [ {headerName: "Sr No", cellRenderer: function(params) {return params.node.id + 1;} },
                             {headerName: "name", field: "name", width: 100 },{headerName: "tags", field: "tags", width: 300 },
                             
                             {headerName: "Pic", width: 700,
                                cellRenderer: function(params) {
                                                return '<img src="'+params.data.path+'"  height="100" width="500">'                                                 
                                                       ;
                                                    } },
                                                                             
                             {headerName: "creation_date", field: "creation_date", width: 100 },{headerName: "category", field: "category", width: 100 },
                            
                            
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
  
  
   $scope.deleteFile = function(selected_id) { 
      file = Gallery.get({ id: selected_id});
      file.$delete({ id: selected_id},function() {
        toaster.pop({
                type: 'success',
                title: 'Sucess',
                body: "file deleted successfully",
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
  
}).controller('GalleryEditController', function($scope, $state, $stateParams, toaster, $window, Gallery) {
     $scope.loading = false;
     $scope.updateFile = function() { 
     
     $scope.loading = true;
    $scope.file.$update({ id: $stateParams.id },function() {
     toaster.pop({
                type: 'success',
                title: 'Sucess',
                body: "Update was a success",
                showCloseButton: true,
                timeout: 0
                });
        
       $state.go('gallery.list');
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

  
  $scope.loadFile = function() { //Issues a GET request to /api/images/:id to get a image to update
                       $scope.file = Gallery.get({ id: $stateParams.id },
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

  $scope.loadFile(); 
  }).controller('GalleryCreateController', function($scope, $state, Gallery, toaster, Upload) {
          $scope.file = new Gallery(); 
          $scope.loading = false;
          $scope.file.data = {};
          $scope.file.data.attributes = {};
          $scope.file.data.attributes.path = false;          
                    
          $scope.addFile = function() { 
                                $scope.loading = true;
                                $scope.file.data.type = "files";                           
                                                                       
                                // upload on file select or drop
                                $scope.file.$create(function() {
                                toaster.pop({
                                            type: 'success',
                                            title: 'Sucess',
                                            body: "File saved successfully",
                                            showCloseButton: true,
                                            timeout: 0
                                            });
                                   $state.go('gallery.list');
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




  