// spec.js
describe('Testing Images CRUD Module', function() {

var Image = function() {
        
        var name = element(by.id('name'));
        this.setName = function(nameText) { name.clear(); name.sendKeys(nameText); };
        
        var tags = element(by.id('tags'));
        this.setTags = function(tagsText) { tags.clear(); tags.sendKeys(tagsText); };
        
        var path = element(by.id('path'));
        this.setPath = function(pathText) { path.clear(); path.sendKeys(pathText); };
        
        var creation_date = element(by.id('creation_date'));
        this.setCreation_Date = function(creation_dateText) { creation_date.clear(); creation_date.sendKeys(creation_dateText); };
        
        var category = element(by.id('category'));
        this.setCategory = function(categoryText) { category.clear(); category.sendKeys(categoryText); };
        
         
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
    
it('Should add a new Image', function() {
    
    var image = new Image();
    
    // Get images URL
    image.get();
    
    // Goto the new menu    
    element(by.id('images_menu')).click();
    element(by.id('images_new')).click();
    
    // Fill in the Fields
    
        image.setName("Your Title text here");
        image.setTags("Your Body text here 77569yuii3wui&%$$^"); 
        image.setPath("Your Body text here 77569yuii3wui&%$$^");  
        image.setCreation_Date("2014-12-22T03:12:58.019077+00:00"); 
        image.setCategory("Your Title text here");

    //Expectations
    image.toast("Image saved successfully");
                 
  });
      
it('Should  edit a Image', function() {

    var image = new Image();
    
    image.get();
    
    //Goto the edit menu
    element(by.id('images_menu')).click();
    element(by.id('images_list')).click(); 
    element(by.css('.ag-row-level-0')).click();
    element(by.id('editButton')).click();
     
    // Fill in the fields
    
        image.setName("Your Updated Title text here");
        image.setTags("Your Updated Body text here 77569yuii3wui&%$$^"); 
        image.setPath("Your Updated Body text here 77569yuii3wui&%$$^"); 
        image.setCreation_Date("2015-12-22T03:12:58.019077+00:00"); 
        image.setCategory("Your Updated Title text here");
    
    //Expectations
    image.toast("Update was a success");
      
 

});
    
it('Should  delete a Image', function() {
    browser.get('http://localhost:5000/');
    element(by.id('images_menu')).click();
    element(by.id('images_list')).click();
    element(by.css('.ag-row-level-0')).click();
    element(by.id('deleteButton')).click()
            
    .then(function(){

        var EC = protractor.ExpectedConditions;
        var toastMessage = $('.toast-message');

         browser.wait(EC.visibilityOf(toastMessage), 60) //wait until toast is displayed
            .then(function(){

                expect(toastMessage.getText()).toBe("Image deleted successfully")

      });
  
  });
});
      
  });
