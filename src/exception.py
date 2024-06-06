import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys): #creates a personalized error message
    _,_,exc_tb = error_detail.exc_info()#this is the execution info. details of error
    file_name = exc_tb.tb_frame.f_code.co_filename#details of file with error
    error_message = "An error occured in python script name [{0}] line number[{1}] error message[{2}]".format(
    file_name,exc_tb.tb_lineno,str(error))

    return error_message

#whenever the an error occurs we need to call the above function
class CustomException(Exception):
    def __init__(self, error_message,error_detail:sys):
        super().__init__(error_message)#super helpsinherit the exception class
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
    

# if __name__=="__main__":
#     try:
#         a=1/0
#     except Exception as e:
#         raise CustomException(e,sys)