from src.exceptions import BadRequest, NotAuthenticated, PermissionDenied, HTTPException

from src.auth.constants import ErrorCode

class AuthRequired(NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED

class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorCode.AUTHORIZATION_FAILED

class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN

class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS

class EmailTaken(BadRequest):
    DETAIL = ErrorCode.EMAIL_TAKEN
    
class UsernameTaken(BadRequest):
    DETAIL = ErrorCode.USERNAME_TAKEN

class PasswordNotMatch(BadRequest):
    DETAIL = ErrorCode.PASSWORD_NOT_MATCH

class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_NOT_VALID
    
class RefreshTokenRequired(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_REQUIRED

class UserNotExistsWithRefreshToken(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_USER_NOT_EXISTS
    
