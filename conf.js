exports.config = {
  framework: 'jasmine',
  seleniumAddress: 'http://localhost:4444/wd/hub',
  specs: [  
   'app/templates/users/spec.js'   
    
   
   
   //Specs
   , 'app/templates/terms/spec.js' 
   , 'app/templates/posts/spec.js' 
   , 'app/templates/comments/spec.js' 

  ]
}

