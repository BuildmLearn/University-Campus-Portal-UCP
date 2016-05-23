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
    
class error():
    '''
    error codes
    '''