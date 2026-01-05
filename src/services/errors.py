class BaseServiceError(ValueError):
    """Base class for all business service exceptions, inherits from built-in ValueError"""
    def __init__(self, description: str | None = None):
        super().__init__(description)
        self.description = description


class FileIsEmptyError(BaseServiceError):
    """Raised when the uploaded file contains no content"""
    def __init__(self):
        super().__init__(description="Uploaded file is empty, empty files are not allowed to be saved")


class FileFoundError(BaseServiceError):
    """Raised when a file with the same name already exists in the target path"""
    def __init__(self):
        super().__init__(description="A file with the same name already exists in the target path, duplicate upload is prohibited")