class MvRequests:
    endpoints = {}

    parameter_types_mapping = {}

    @staticmethod
    def add_endpoint(request_name, endpoint):
    	MvRequests.endpoints[request_name] = endpoint

    @staticmethod
    def add_parameter_mapping(request_name, parameter_name, conversion_func):
        MvRequests.parameter_types_mapping[f"{request_name}-{parameter_name}"] = conversion_func

    @staticmethod
    def get_request_string(request_name, params):
        if request_name not in MvRequests.endpoints:
            raise ValueError(f"Request {request_name} is not a valid endpoint")

        endpoint = MvRequests.endpoints[request_name]
        param_str = '&'.join(f"{key}={value}" for key, value in params.items())

        return f"{endpoint}?{param_str}" if param_str else endpoint

    @staticmethod
    def get_parameter_func(request_name, parameter_name):
        specific_key = f"{request_name}-{parameter_name}"
        
        return MvRequests.param_types[specific_key]

    @staticmethod
    def get_parameters_mapping(request_name, parameter_names, user_mappings=None):
        return {
            f"{request_name}-{param}": (user_mappings.get(param) 
                                        if user_mappings and param in user_mappings
                                        else MvRequests.parameter_types_mapping.get(f"{request_name}-{param}")
                                       )
            for param in parameter_names
        }
