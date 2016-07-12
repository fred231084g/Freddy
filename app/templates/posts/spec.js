// spec.js
describe('Testing Posts CRUD Module', function() {

var Post = function() {
        
        var author = element(by.id('author'));
        this.setAuthor = function(authorText) { author.clear(); author.sendKeys(authorText); };
        
        var title = element(by.id('title'));
        this.setTitle = function(titleText) { title.clear(); title.sendKeys(titleText); };
        
        var slug = element(by.id('slug'));
        this.setSlug = function(slugText) { slug.clear(); slug.sendKeys(slugText); };
        
        var date = element(by.id('date'));
        this.setDate = function(dateText) { date.clear(); date.sendKeys(dateText); };
        
        var date_gmt = element(by.id('date_gmt'));
        this.setDate_Gmt = function(date_gmtText) { date_gmt.clear(); date_gmt.sendKeys(date_gmtText); };
        
        var content = element(by.id('content'));
        this.setContent = function(contentText) { content.clear(); content.sendKeys(contentText); };
        
        var excerpt = element(by.id('excerpt'));
        this.setExcerpt = function(excerptText) { excerpt.clear(); excerpt.sendKeys(excerptText); };
        
        var status = element(by.id('status'));
        this.setStatus = function(statusText) { status.clear(); status.sendKeys(statusText); };
        
        var modified = element(by.id('modified'));
        this.setModified = function(modifiedText) { modified.clear(); modified.sendKeys(modifiedText); };
        
        var modified_gmt = element(by.id('modified_gmt'));
        this.setModified_Gmt = function(modified_gmtText) { modified_gmt.clear(); modified_gmt.sendKeys(modified_gmtText); };
        
        var type = element(by.id('type'));
        this.setType = function(typeText) { type.clear(); type.sendKeys(typeText); };
        
        var parent = element(by.id('parent'));
        this.setParent = function(parentText) { parent.clear(); parent.sendKeys(parentText); };
        
        var terms = element(by.id('terms'));
        this.setTerms = function(termsText) { terms.clear(); terms.sendKeys(termsText); };
        
        var comments = element(by.id('comments'));
        this.setComments = function(commentsText) { comments.clear(); comments.sendKeys(commentsText); };
        
         
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
    
it('Should add a new Post', function() {
    
    var post = new Post();
    
    // Get posts URL
    post.get();
    
    // Goto the new menu    
    element(by.id('posts_menu')).click();
    element(by.id('posts_new')).click();
    
    // Fill in the Fields
    
        post.setAuthor("Your Title text here");
        post.setTitle("Your Body text here 77569yuii3wui&%$$^"); 
        post.setSlug("Your Title text here"); 
        post.setDate("2014-12-22T03:12:58.019077+00:00");  
        post.setDate_Gmt("2014-12-22T03:12:58.019077+00:00"); 
        post.setContent("Your Body text here 77569yuii3wui&%$$^"); 
        post.setExcerpt("Your Body text here 77569yuii3wui&%$$^"); 
        post.setStatus("Your Title text here"); 
        post.setModified("2014-12-22T03:12:58.019077+00:00");  
        post.setModified_Gmt("2014-12-22T03:12:58.019077+00:00"); 
        post.setType("Your Title text here"); 
        post.setParent(56); 
        post.setTerms("Your Title text here");
        post.setComments("Your Title text here");

    //Expectations
    post.toast("Post saved successfully");
                 
  });
      
it('Should  edit a Post', function() {

    var post = new Post();
    
    post.get();
    
    //Goto the edit menu
    element(by.id('posts_menu')).click();
    element(by.id('posts_list')).click(); 
    element(by.css('.ag-row-level-0')).click();
    element(by.id('editButton')).click();
     
    // Fill in the fields
    
        post.setAuthor("Your Updated Title text here");
        post.setTitle("Your Updated Body text here 77569yuii3wui&%$$^"); 
        post.setSlug("Your Updated Title text here");
        post.setDate("2015-12-22T03:12:58.019077+00:00"); 
        post.setDate_Gmt("2015-12-22T03:12:58.019077+00:00"); 
        post.setContent("Your Updated Body text here 77569yuii3wui&%$$^"); 
        post.setExcerpt("Your Updated Body text here 77569yuii3wui&%$$^"); 
        post.setStatus("Your Updated Title text here");
        post.setModified("2015-12-22T03:12:58.019077+00:00"); 
        post.setModified_Gmt("2015-12-22T03:12:58.019077+00:00"); 
        post.setType("Your Updated Title text here");
        post.setParent(67); 
        post.setTerms("Your Updated Title text here");
        post.setComments("Your Updated Title text here");
    
    //Expectations
    post.toast("Update was a success");
      
 

});
    
it('Should  delete a Post', function() {
    browser.get('http://localhost:5000/');
    element(by.id('posts_menu')).click();
    element(by.id('posts_list')).click();
    element(by.css('.ag-row-level-0')).click();
    element(by.id('deleteButton')).click()
            
    .then(function(){

        var EC = protractor.ExpectedConditions;
        var toastMessage = $('.toast-message');

         browser.wait(EC.visibilityOf(toastMessage), 60) //wait until toast is displayed
            .then(function(){

                expect(toastMessage.getText()).toBe("Post deleted successfully")

      });
  
  });
});
      
  });
