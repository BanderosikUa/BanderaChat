from src.exceptions import BadRequest, NotFound

from src.chat.constants import ErrorCode

class ChatPermissionRequired(BadRequest):
    DETAIL = ErrorCode.CHAT_PERMISSION_REQUIRED

class ChatNotFound(NotFound):
    DETAIL = ErrorCode.CHAT_NOT_FOUND
