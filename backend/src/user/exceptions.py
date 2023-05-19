from src.exceptions import BadRequest, NotAuthenticated, PermissionDenied, CustomValidationError

from src.user.constants import ErrorCode

class PhotoExtensionNotAlllow(BadRequest):
    DETAIL = ErrorCode.PHOTO_NOT_ALLOW
