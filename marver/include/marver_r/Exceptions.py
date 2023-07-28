"""
::: SAMPLE USAGE :::

class SalaryNotInRangeError(Exception):
    '''Exception raised for errors in the input salary.

    Attributes:
        salary -- input salary which caused the error
        message -- explanation of the error
    '''

    def __init__(self, salary, message="Salary is not in (5000, 15000) range"):
        self.salary = salary
        self.message = message
        super().__init__(self.message)


salary = int(input("Enter salary amount: "))
if not 5000 < salary < 15000:
    raise SalaryNotInRangeError(salary)

"""


# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class GetExecutableAuthMonitor(Error):
    """Exception raised when the monitor can't get executable authentication"""
    pass


class GetExecutableAuthGenerator(Error):
    """Exception raised when the generator can't get executable authentication"""
    pass


class GetExecutableAuthTLOracle(Error):
    """Exception raised when the TLOracle can't get executable authentication"""


class ConvertYAML2MonitorPy(Error):
    """Exception raised when the .yaml file can't convert"""
    pass


class LinkMonitor2ROSWs(Error):
    """Exception raised when the monitor folder linking to Ros workspace"""


class MonitorNotExist(Error):
    """Exception raised when the monitor is not created or imported"""


class CatkinMakeError(Error):
    """Exception raised when the ros workspace isn't selected correctly"""


class StartRVError(Error):
    """Exception raised when the monitor isn't selected correctly"""


class SocketConnectionError(Error):
    """Exception raised when socket connection is failed"""


class MonitorStart(Error):
    """Exception raised when monitor is starting"""
