class LinkTuneException(Exception):
    """Base exception class for LinkTune."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
        def __str__(self):
            return self.message
    
class InvalidLinkException(LinkTuneException):
    """Raised when provided link is invalid."""
    
class ServiceNotFoundException(LinkTuneException):
    """Raised when user specified service is not found."""
    
class NoResultsReturnedException(LinkTuneException):
    """Raised service API does not return any result data."""
    
class TrackNotFoundException(LinkTuneException):
    """Raised when specified track is not found."""
    
class TrackNotFoundOnAlbumException(LinkTuneException):
    """Raised when track is not found on specified album."""
    
class ServiceConnectionError(LinkTuneException):
        """Raised when there is an error connecting to a service."""

class ServiceRequestError(LinkTuneException):
    """Raised when there is an error with a service request."""

class ServiceResponseError(LinkTuneException):
    """Raised when a service returns an unexpected response."""