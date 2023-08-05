class CustomException(Exception):
   """Base class for other exceptions"""
   pass

class Nodata(CustomException):
   """Raised when no data is there"""
   pass
   
class PostFailed(CustomException):
   """Raised when post call is failed"""
   pass
