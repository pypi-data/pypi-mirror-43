from lambdabase.invokers import InvokerFactory
from lambdabase.invokers.LambdaInvoker import LambdaInvoker


class LambdaInvokerFactory(InvokerFactory):
    """
    Factory class for generating lambda invokers
    """
    def __init__(self, environment):
        self.environment = environment
        super(LambdaInvokerFactory, self).__init__()

    def register(self, service, function_name, source_type, result_type):
        """
        Register an invoker with the factory
        """
        name = self.get_function_name(self.environment, service, function_name)
        self.invokers[name] = LambdaInvoker(function_name, source_type, result_type)

    @classmethod
    def get_function_name(cls, environment, service, function_name):
        """
        Gets the appropriate function name to call
        :param environment: the execution environment
        :param service: the name of the service to which the function belongs
        :param function_name: the base name of the function to call
        :return: the actual function name to call
        """
        return service + '-' + environment + '-' + function_name

