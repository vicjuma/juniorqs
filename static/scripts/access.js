'use strict';

/**
 * Handles admin log in
 * @param {type} e
 * @returns {undefined}
 */

function handleLogin(email, password, callback){
  var jsonToReturn = "";
  
  $.ajax('http://localhost/login', {
      method: "POST",
      data: {email:email, password:password}
  }).done(function(returnedData){
      if(returnedData.status === 1){
          jsonToReturn = {status:1, msg:"Authenticated..."};
      }

      else{
          //display error messages
          jsonToReturn = {status:0, msg:"Invalid email/password combination"};
      }
  
  typeof(callback) === "function" ? callback(jsonToReturn) : "";
  
  }).fail(function(xhr){
      //set error message based on the internet connectivity of the user
      var msg = xhr.status+' '+xhr.statusText;
      
      //display error messages
      jsonToReturn = {status:0, msg:msg};
  
      typeof(callback) === "function" ? callback(jsonToReturn) : "";
  });
}


loginForm.onsubmit = function(e){
    e.preventDefault();
    
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    
    if(!email || !password){
        var errMsg = !email ? "Enter your email" : "Enter your password";
        
        document.getElementById('errMsg').innerHTML = errMsg;
    }
    
    else{
        document.getElementById('errMsg').innerHTML = "Authenticating......";
	
	//call function to handle log in and get the returned data through a callback
	handleLogin(email, password, function(returnedData){
	          if(true){
                document.getElementById('errMsg').innerHTML = "Authenticated. Redirecting....";
                
                handleLoginRedirect();
            }

            else{
                //display error message
                document.getElementById('errMsg').innerHTML = returnedData.msg;
            }
        });
    }
};




function handleLoginRedirect(){
    //get the current url to check whether "red_uri" is set. Red_uri is suppose to hold details about the url user was trying to access
    //before been redirected to log in
    
    var currentUrl = window.location.href;
    
    //split the url using "red_uri", then get the 1st part after the red_uri (i.e. key 1)
    var uriToRedirectTo = currentUrl.split("red_uri=")[1] || "home";
    
    //redirect to dashboard
    window.location.href("http://localhost:3000/home");    
}
