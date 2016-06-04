function showRegisterForm(){
    $('#registration-form').show();
    $('#login-form').hide();
    $("#login-tab-button").removeClass('tab-selected');
    $("#register-tab-button").addClass('tab-selected');
    
    window.history.pushState('register', 'Register', '/user/register');
}

function showLoginForm(){
    $('#login-form').show();
    $('#registration-form').hide();
    $("#login-tab-button").addClass('tab-selected');
    $("#register-tab-button").removeClass('tab-selected');
    
    window.history.pushState('login', 'Login', '/user/login');
}
