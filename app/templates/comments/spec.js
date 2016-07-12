// spec.js
describe('Testing Comments CRUD Module', function() {

var Comment = function() {
        
        var post_id = element(by.id('post_id'));
        this.setPost_Id = function(post_idText) { post_id.clear(); post_id.sendKeys(post_idText); };
        
        var author_name = element(by.id('author_name'));
        this.setAuthor_Name = function(author_nameText) { author_name.clear(); author_name.sendKeys(author_nameText); };
        
        var author_email = element(by.id('author_email'));
        this.setAuthor_Email = function(author_emailText) { author_email.clear(); author_email.sendKeys(author_emailText); };
        
        var author_url = element(by.id('author_url'));
        this.setAuthor_Url = function(author_urlText) { author_url.clear(); author_url.sendKeys(author_urlText); };
        
        var created_on = element(by.id('created_on'));
        this.setCreated_On = function(created_onText) { created_on.clear(); created_on.sendKeys(created_onText); };
        
        var content = element(by.id('content'));
        this.setContent = function(contentText) { content.clear(); content.sendKeys(contentText); };
        
        var karma = element(by.id('karma'));
        this.setKarma = function(karmaText) { karma.clear(); karma.sendKeys(karmaText); };
        
        var approved = element(by.id('approved'));
        this.setApproved = function(approvedText) { approved.clear(); approved.sendKeys(approvedText); };
        
        var agent = element(by.id('agent'));
        this.setAgent = function(agentText) { agent.clear(); agent.sendKeys(agentText); };
        
        var type = element(by.id('type'));
        this.setType = function(typeText) { type.clear(); type.sendKeys(typeText); };
        
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
    
it('Should add a new Comment', function() {
    
    var comment = new Comment();
    
    // Get comments URL
    comment.get();
    
    // Goto the new menu    
    element(by.id('comments_menu')).click();
    element(by.id('comments_new')).click();
    
    // Fill in the Fields
     
        comment.setPost_Id(56); 
        comment.setAuthor_Name("Your Title text here");
        comment.setAuthor_Email("Your Title text here");
        comment.setAuthor_Url("Your Title text here"); 
        comment.setCreated_On("2014-12-22T03:12:58.019077+00:00"); 
        comment.setContent("Your Body text here 77569yuii3wui&%$$^");  
        comment.setKarma(56); 
        comment.setApproved("Your Title text here");
        comment.setAgent("Your Body text here 77569yuii3wui&%$$^"); 
        comment.setType("Your Title text here"); 
        comment.setParent(56); 

    //Expectations
    comment.toast("Comment saved successfully");
                 
  });
      
it('Should  edit a Comment', function() {

    var comment = new Comment();
    
    comment.get();
    
    //Goto the edit menu
    element(by.id('comments_menu')).click();
    element(by.id('comments_list')).click(); 
    element(by.css('.ag-row-level-0')).click();
    element(by.id('editButton')).click();
     
    // Fill in the fields
    
        comment.setPost_Id(67); 
        comment.setAuthor_Name("Your Updated Title text here");
        comment.setAuthor_Email("Your Updated Title text here");
        comment.setAuthor_Url("Your Updated Title text here");
        comment.setCreated_On("2015-12-22T03:12:58.019077+00:00"); 
        comment.setContent("Your Updated Body text here 77569yuii3wui&%$$^"); 
        comment.setKarma(67); 
        comment.setApproved("Your Updated Title text here");
        comment.setAgent("Your Updated Body text here 77569yuii3wui&%$$^"); 
        comment.setType("Your Updated Title text here");
        comment.setParent(67); 
    
    //Expectations
    comment.toast("Update was a success");
      
 

});
    
it('Should  delete a Comment', function() {
    browser.get('http://localhost:5000/');
    element(by.id('comments_menu')).click();
    element(by.id('comments_list')).click();
    element(by.css('.ag-row-level-0')).click();
    element(by.id('deleteButton')).click()
            
    .then(function(){

        var EC = protractor.ExpectedConditions;
        var toastMessage = $('.toast-message');

         browser.wait(EC.visibilityOf(toastMessage), 60) //wait until toast is displayed
            .then(function(){

                expect(toastMessage.getText()).toBe("Comment deleted successfully")

      });
  
  });
});
      
  });
