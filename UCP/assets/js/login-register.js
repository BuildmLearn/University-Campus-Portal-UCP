function showRegisterForm(){
    $('#registration-form').css("zIndex",2);
    $('#login-form').css("zIndex",1);
    $("#login-tab-button").removeClass('tab-selected');
    $("#register-tab-button").addClass('tab-selected');
    
    window.history.pushState('register', 'Register', '/user/register');
}

function showLoginForm(){
    $('#login-form').css("zIndex",2);
    $('#registration-form').css("zIndex",1);
    $("#login-tab-button").addClass('tab-selected');
    $("#register-tab-button").removeClass('tab-selected');
    
    window.history.pushState('login', 'Login', '/user/login');
}
