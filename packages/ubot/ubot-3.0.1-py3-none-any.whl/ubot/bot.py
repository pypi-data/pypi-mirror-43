import enum
import json
import logging
from asyncio import PriorityQueue, get_event_loop, iscoroutinefunction
from urllib.parse import urlencode

from .requests import get_pool_manager


class ExceptionThrownWhen(enum.Enum):
    checking_update = 10
    executing_handler = 20
    executing_matcher = 30


class Bot(object):
    update_types = [
        ('message', 'message'),
        ('edited_message', 'message'),
        ('channel_post', 'message'),
        ('edited_channel_post', 'message'),
        ('inline_query', 'inline_query'),
        ('chosen_inline_result', 'chosen_inline_result'),
        ('callback_query', 'callback_query'),
        ('shipping_query', 'shipping_query'),
        ('pre_checkout_query', 'pre_checkout_query')
    ]
    discover_type_and_flavor = False

    def __init__(self, token, json_lib=json, max_handlers=1):
        """
        The Class(TM).

        :param token: The Telegram-given token
        """

        self.token = token
        self.json = json_lib
        self.max_handlers = max_handlers

        self.http = get_pool_manager()
        self.logger = logging.getLogger('ubot')
        self.triggers = []
        self.ignore_check_triggers = []
        self.update_queue = PriorityQueue()

    @property
    def base_url(self):
        return 'https://api.telegram.org:443/bot{}/'.format(self.token)

    async def api_request(self, method, endpoint, fields=None):
        """
        Wraps the urllib3 request in a more user friendly way, making it async and premitting the base Telegram API url.

        :param method: The HTTP method name (GET, POST, PUT, DELETE, HEAD)
        :param endpoint: A Telegram API endpoint (e.g. sendMessage), omitting
            the first slash
        :param fields: A dict of params to be used in the request (used as
            query params with GET/HEAD/DELETE, used as from parans with
            POST/PUT)
        :return: The response from the server, in the form of a dict
        """

        url = '{}{}'.format(self.base_url, endpoint)
        loop = get_event_loop()
        res = await loop.run_in_executor(None, self.http.request, method, url, fields)

        return res

    async def set_webhook_url(self, url):
        await self.api_request('GET', 'setWebhook?url={}'.format(url))

    async def start(self):  # noqa: C901
        """
        Main loop

        >>> import asyncio
        >>> bot = Bot('token')
        >>> loop = asyncio.new_event_loop()
        >>> loop.create_task(bot.start())
        >>> # create all the other tasks
        >>> loop.run_forever()
        """

        while True:
            update = await self.update_queue.get()

            # get type and flavor if needed or simply leave them to None
            if self.discover_type_and_flavor is True:
                for _type, flavor in self.update_types:
                    if _type in update:
                        update_type, update_flavor = _type, flavor
                        break
                else:
                    update_type, update_flavor = None, None
            else:
                update_type, update_flavor = None, None

            # check the update if the function is implemented and skip if it's not passed
            if hasattr(self, 'check_update'):
                check_update = self.check_update
                try:
                    if iscoroutinefunction(check_update):
                        is_check_passed = await check_update(update, update_type, update_flavor)
                    else:
                        is_check_passed = check_update(update, update_type, update_flavor)
                except Exception as e:
                    when = ExceptionThrownWhen.checking_update
                    await self.handle_exception(update, e, when)
                    continue

                if is_check_passed is True:
                    checked_triggers = [*self.ignore_check_triggers, *self.triggers]
                else:
                    checked_triggers = self.triggers
            else:
                checked_triggers = self.triggers

            # loop through the triggers to find one that matches
            curr_handlers = 0

            for trigger in checked_triggers:
                if curr_handlers > self.max_handlers:
                    break

                match = trigger.match

                try:
                    if iscoroutinefunction(match):
                        is_update_matched = await match(update, update_type, update_flavor)
                    else:
                        is_update_matched = match(update, update_type, update_flavor)
                except Exception as e:
                    when = ExceptionThrownWhen.executing_matcher
                    await self.handle_exception(update, e, when)
                    continue

                if is_update_matched is not True:
                    continue

                curr_handlers += 1

                # if a matching one is found call the corresponding handler
                handle = trigger.handle

                try:
                    if iscoroutinefunction(handle):
                        endpoint = await handle(update, update_type, update_flavor)
                    else:
                        endpoint = handle(update, update_type, update_flavor)
                except Exception as e:
                    when = ExceptionThrownWhen.executing_handler
                    await self.handle_exception(update, e, when)
                    continue

                if endpoint is None:
                    continue

                method, url, args, fields = endpoint

                _url = '{}?{}'.format(url, urlencode(args))
                response = await self.api_request(method, _url, fields)

                # call the callback if existing
                callback = trigger.callback

                if callback is None:
                    continue

                try:
                    if iscoroutinefunction(callback):
                        await callback(response)
                    else:
                        callback(response)
                except Exception as e:
                    when = ExceptionThrownWhen.executing_handler
                    await self.handle_exception(update, e, when)
                    continue

    def push_update(self, update):
        """
        Pushes an update (already json decoded) into the queue.

        :param update: The update to be pushed in the queue
        """

        self.update_queue.put_nowait((update['update_id'], update))

    async def handle_exception(self, update, exception, when):
        """
        Logs the exception and calls the on_exception function if it exists.
        N.B.: this *must* be used only to log *externally* originated exception

        :param update: The update whose processing triggered the exception
        :param exception: The exception object
        :param when: A string containing info about when the Exception was thrown
        """

        _when = str(ExceptionThrownWhen(when).name)
        error = 'Exception {0}\n occurred when {1}\n during handling of' \
                ' update:\n {2}' \
            .format(str(exception), _when, self.json.dumps(update))

        self.logger.exception(error, exc_info=True)

        if hasattr(self, 'on_exception'):
            on_exception = self.on_exception
            if iscoroutinefunction(on_exception):
                await on_exception(update, exception, _when)
            else:
                on_exception(update, exception, _when)

    def trigger(self, requires_type_and_flavor=False, ignore_check=False):
        """
        Decorates a Trigger, inserting it into the bot check list

        :param requires_type_and_flavor: Forces the bot to discover the type and the flavor of an update and to call
            the trigger methods with those as arguments
        :param ignore_check: ignores a possible "check_update" function
        """

        def decorator(trigger):
            if ignore_check is True:
                self.ignore_check_triggers.append(trigger)
            else:
                self.triggers.append(trigger)

            if requires_type_and_flavor is True:
                self.discover_type_and_flavor = True

            return trigger

        return decorator
