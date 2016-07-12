// spec.js
describe('Testing Terms CRUD Module', function() {

var Term = function() {
        
        var name = element(by.id('name'));
        this.setName = function(nameText) { name.clear(); name.sendKeys(nameText); };
        
        var slug = element(by.id('slug'));
        this.setSlug = function(slugText) { slug.clear(); slug.sendKeys(slugText); };
        
        var description = element(by.id('description'));
        this.setDescription = function(descriptionText) { description.clear(); description.sendKeys(descriptionText); };
        
        var taxonomy = element(by.id('taxonomy'));
        this.setTaxonomy = function(taxonomyText) { taxonomy.clear(); taxonomy.sendKeys(taxonomyText); };
        
        var parent = element(by.id('parent'));
        this.setParent = function(parentText) { parent.clear(); parent.sendKeys(parentText); };
        
         
        this.get = function() {
                                   browser.get('http://localhost:5000/');
                                       };    
        
        this.toast = function(message){
                                        $('.form-button .button-primary').click()  // css selectors http://angular.github.io/protractor/#/api?view=build$  
                                            .then(function() {     
                                                  var EC = protractor.ExpectedConditions;
                                                  var toastMessage = $('.toast-message');                                      
                                                  browser.wait(EC.visibilityOf(toastMessage), 6000) //wait until toast is displayed
                                                             .then(function(){
                                                                    expect(toastMessage.getText()).toBe(message);

                                                                        });
                                                                  });                                                    
                                    }                    
                    };
    
it('Should add a new Term', function() {
    
    var term = new Term();
    
    // Get terms URL
    term.get();
    
    // Goto the new menu    
    element(by.id('terms_menu')).click();
    element(by.id('terms_new')).click();
    
    // Fill in the Fields
    
        term.setName("Your Title text here");
        term.setSlug("Your Title text here");
        term.setDescription("Your Title text here");
        term.setTaxonomy("Your Title text here"); 
        term.setParent(56); 

    //Expectations
    term.toast("Term saved successfully");
                 
  });
      
it('Should  edit a Term', function() {

    var term = new Term();
    
    term.get();
    
    //Goto the edit menu
    element(by.id('terms_menu')).click();
    element(by.id('terms_list')).click(); 
    element(by.css('.ag-row-level-0')).click();
    element(by.id('editButton')).click();
     
    // Fill in the fields
    
        term.setName("Your Updated Title text here");
        term.setSlug("Your Updated Title text here");
        term.setDescription("Your Updated Title text here");
        term.setTaxonomy("Your Updated Title text here");
        term.setParent(67); 
    
    //Expectations
    term.toast("Update was a success");
      
 

});
    
it('Should  delete a Term', function() {
    browser.get('http://localhost:5000/');
    element(by.id('terms_menu')).click();
    element(by.id('terms_list')).click();
    element(by.css('.ag-row-level-0')).click();
    element(by.id('deleteButton')).click()
            
    .then(function(){

        var EC = protractor.ExpectedConditions;
        var toastMessage = $('.toast-message');

         browser.wait(EC.visibilityOf(toastMessage), 60) //wait until toast is displayed
            .then(function(){

                expect(toastMessage.getText()).toBe("Term deleted successfully")

      });
  
  });
});
      
  });
