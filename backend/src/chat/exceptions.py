from src.exceptions import BadRequest, NotFound, CustomValidationError

from src.chat.constants import ErrorCode

class ChatPermissionRequired(BadRequest):
    DETAIL = ErrorCode.CHAT_PERMISSION_REQUIRED

class ChatNotFound(NotFound):
    DETAIL = ErrorCode.CHAT_NOT_FOUND

class DirectChatAlreadyExists(BadRequest):
    DETAIL = ErrorCode.ChatAlreadyExists

class DirectParticipantListMustHave2Objs(CustomValidationError):
    FIELD = "participants"
    DETAIL = ErrorCode.ListOfTwoObjs
