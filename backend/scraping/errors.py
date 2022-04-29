class ApiError(Exception):
    pass

class ApiNoCreditsError(ApiError):
    pass

class ApiRequestsFailedError(ApiError):
    pass