'''
Constants for API result and error codes and messages
'''

class result():
    RESULT_SUCCESS = 1
    RESULT_FAILURE = 0
    
class message():
    
    MESSAGE_LOGIN_SUCCESSFUL = "login successful"
    MESSAGE_INVALID_LOGIN_DETAILS = "the username or password provided was invalid"
    MESSAGE_ACCOUNT_INACTIVE = "your account has not been activated yet"
    
    MESSAGE_REGISTRATION_SUCCESSFUL = "User successfully registered"
    MESSAGE_REGISTRATION_FAILED = "User registration failed, please see the errors for more detail"
    
    MESSAGE_EMAIL_VERIFICATION_SUCCESSFUL = "User email is successfully verified"
    MESSAGE_VERIFICATION_CODE_EXPIRED = "The verification code provided does not exist or might have been expired"
    MESSAGE_EMAIL_NOT_REGISTERED = "Given email Id is not registered"
    
    MESSAGE_PASSWORD_RESET_CODE_SENT = "Instructions to reset your password have been sent to your email id"
    
    
class error():
    '''
    error codes and messages
    '''
    ERROR_VALIDATION_EMAIL_EXISTS = "Email ID already registered"