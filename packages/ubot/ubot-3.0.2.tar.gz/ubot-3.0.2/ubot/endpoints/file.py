from . import TelegramEndpoint
from .commons import DisableNotification, ParseMode, ReplyToMessageId, _ChatOrInlineMessage
from .reply_markup import ReplyMarkup


class FileEndpoint(TelegramEndpoint, DisableNotification, ReplyMarkup, ReplyToMessageId):
    file_type = None
    attributes = []

    def __init__(self, chat_id, file, is_path=True):
        super().__init__()
        self.args = {
            'chat_id': chat_id
        }

        if is_path is True:
            self.method = 'POST'
            with open(file, 'r') as f:
                content = f.read()
            self.fields = {
                **self.fields,
                self.file_type: content
            }
        else:
            self.method = 'GET'
            self.args = {
                **self.args,
                self.file_type: file
            }


class SerializableToInputMedia(object):
    serialized_fields = []

    def to_input_media(self):

        serialized = {
            'type': self.file_type,
        }

        # todo
        # upload + attach
        if self.file_type in self.fields:
            raise Exception('Must target updated file')
            pass

        serialized['media'] = self.args[self.file_type]

        attributes = [*self.attributes, *self.serialized_fields]
        for attribute in attributes:
            if attribute in self.args:
                serialized[attribute] = self.args[attribute]

        return serialized


class Caption(object):
    def caption(self, caption):
        self.args = {
            **self.args,
            'caption': caption
        }
        return self


# todo
class Thumb(object):
    pass


class SendPhoto(FileEndpoint, Caption, ParseMode, SerializableToInputMedia):
    file_type = 'photo'
    serialized_fields = ['caption', 'parse_mode']


class SendAudio(FileEndpoint, Caption, ParseMode, Thumb, SerializableToInputMedia):
    file_type = 'audio'
    attributes = ['duration', 'performer', 'title']
    serialized_fields = ['caption', 'parse_mode', 'thumb']


class SendDocument(FileEndpoint, Caption, ParseMode, Thumb, SerializableToInputMedia):
    file_type = 'document'
    serialized_fields = ['caption', 'parse_mode', 'thumb']


class SendVideo(FileEndpoint, Caption, ParseMode, Thumb, SerializableToInputMedia):
    file_type = 'video'
    attributes = ['duration', 'width', 'height']
    serialized_fields = ['caption', 'parse_mode', 'thumb', 'supports_streaming']

    def supports_streaming(self):
        self.args = {
            **self.args,
            'supports_streaming': True
        }
        return self


class SendAnimation(FileEndpoint, Caption, ParseMode, Thumb, SerializableToInputMedia):
    file_type = 'animation'
    attributes = ['duration', 'width', 'height']
    serialized_fields = ['caption', 'parse_mode', 'thumb']


class SendVoice(FileEndpoint, Caption, ParseMode):
    file_type = 'animation'
    attributes = ['duration']


class SendVideoNote(FileEndpoint, Thumb):
    file_type = 'video_note'
    attributes = ['duration', 'length']


class SendMediaGroup(TelegramEndpoint, DisableNotification, ReplyToMessageId):
    def __init__(self, chat_id, media_array):
        super().__init__()
        self.args = {
            'chat_id': chat_id,
            'media': [x.to_input_media() for x in media_array]
        }


class GetFile(TelegramEndpoint):
    # https://api.telegram.org/file/bot<token>/<file_path>
    def __init__(self, file_id):
        super().__init__()
        self.args = {
            'file_id': file_id
        }


class EditMessageCaption(TelegramEndpoint, Caption, ParseMode, ReplyMarkup, _ChatOrInlineMessage):
    def __init__(self, chat_or_inline_message_id, message_id):
        super().__init__()
        self.__chat_or_inline_message(chat_or_inline_message_id, message_id)


class EditMessageMedia(TelegramEndpoint, ReplyMarkup, _ChatOrInlineMessage):
    def __init__(self, chat_or_inline_message_id, message_id, media):
        super().__init__()
        self.args = {
            'media': media.to_input_media()
        }
        self.__chat_or_inline_message(chat_or_inline_message_id, message_id)
