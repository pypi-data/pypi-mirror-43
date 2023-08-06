from lambdabase.invokers.InvokerFactory import InvokerFactory


class LocalInvokerFactory(InvokerFactory):
    """
    Factory class for generating local invokers
    """
    def register(self, service, function_name, source_type, result_type, query_key, invoker_type):
        """
        Register an invoker with the factory
        """
        name = self.get_function_name(service, function_name)
        self.invokers[name] = invoker_type()

    @classmethod
    def get_function_name(cls, service, function_name=None):
        """
        Gets the appropriate function name to call
        :param service: the name of the service to which the function belongs
        :param function_name: the base name of the function to call
        :return: the actual function name to call
        """
        if function_name is not None:
            return service[5:] + '/' + function_name
        else:
            return service[5:]
