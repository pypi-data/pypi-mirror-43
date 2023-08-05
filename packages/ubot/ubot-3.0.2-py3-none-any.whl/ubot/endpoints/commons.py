from .exceptions import InvalidParseMode


class _ChatOrInlineMessage(object):
    def __chat_or_inline_message(self, chat_or_inline_message_id, message_id):
        if message_id is not None:
            self.args = {
                **self.args,
                'chat_id': chat_or_inline_message_id,
                'message_id': message_id
            }
        else:
            self.args = {
                **self.args,
                'inline_message_id': chat_or_inline_message_id
            }


class ReplyToMessageId(object):
    # todo
    def reply_to_message_id(self, message_id):
        self.args = {
            **self.args,
            'reply_to_message_id': message_id
        }
        return self


class DisableNotification(object):
    def disable_notification(self):
        self.args = {
            **self.args,
            'disable_notification': True
        }
        return self


class ParseMode(object):
    def parse_mode(self, _parse_mode):
        if _parse_mode not in ['Markdown', 'HTML']:
            raise InvalidParseMode

        self.args = {
            **self.args,
            'parse_mode': _parse_mode
        }
        return self
