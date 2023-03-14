class LinkTuneException(Exception):
    """Base exception class for LinkTune."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
        def __str__(self):
            return self.message
    
class InvalidLinkException(LinkTuneException):
    """Raised when provided link is invalid."""
    
class TrackIdNotFoundException(LinkTuneException):
    """Raised when track ID cannot be obtained from track URL."""
    
class ServiceNotFoundException(LinkTuneException):
    """Raised when user specified service is not found."""
    
class NoResultsReturnedException(LinkTuneException):
    """Raised service API does not return any result data."""
    
class TrackNotFoundException(LinkTuneException):
    """Raised when specified track is not found."""
    
class TrackNotFoundOnAlbumException(LinkTuneException):
    """Raised when track is not found on specified album."""
    
class ConvertLinkException(LinkTuneException):
    """Generic error raised when convert link has not returned a result object and no other exceptions were caught."""
    
class SearchException(LinkTuneException):
    """Generic exception raised when search has not returned a result object and no other exceptions were caught."""
    
class ServiceConnectionError(LinkTuneException):
        """Raised when there is an error connecting to a service."""

class ServiceRequestError(LinkTuneException):
    """Raised when there is an error with a service request."""

class ServiceTimeoutError(LinkTuneException):
    """Raised when service times out during API request."""

class ServiceResponseError(LinkTuneException):
    """Raised when a service returns an unexpected response."""