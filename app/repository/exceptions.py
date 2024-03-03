class ExternalAPIError(Exception):
    def __init__(self, status_code, message="Request was unsuccessful", external_api_detail_error=None):
        self.status_code = status_code
        self.message = message
        self.external_api_detail_error = external_api_detail_error
        super().__init__(self.message)


class InvalidGitURLException(Exception):
    def __init__(self, url, message="Invalid Git URL format"):
        self.url = url
        self.message = f"{message}: {url}"
        super().__init__(self.message)
