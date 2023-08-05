import time
import re
import inspect

from six.moves.queue import Queue

from lemoncheesecake.helpers.text import camel_case_to_snake_case
from lemoncheesecake.exceptions import serialize_current_exception

DEBUG = 0


def _get_event_name_from_class_name(class_name):
    return re.sub(r"_event$", "", camel_case_to_snake_case(class_name))


class Event(object):
    def __init__(self):
        self.time = time.time()

    @classmethod
    def get_name(cls):
        return _get_event_name_from_class_name(cls.__name__)

    def __str__(self):
        return "<Event type='%s'>" % self.get_name()


class EventType:
    def __init__(self, event_class):
        self._event_class = event_class
        self._handlers = []

    def subscribe(self, handler):
        self._handlers.append(handler)

    def unsubscribe(self, handler):
        self._handlers.remove(handler)

    def reset(self):
        self._handlers = []

    def handle(self, event):
        for handler in self._handlers:
            handler(event)


def _get_event_name(val):
    return val.get_name() if inspect.isclass(val) and issubclass(val, Event) else val


class EventManager:
    def __init__(self):
        self._event_types = {}
        self._queue = Queue()
        self._pending_failure = None, None

    def register_events(self, *event_classes):
        for event_class in event_classes:
            self._event_types[event_class.get_name()] = EventType(event_class)

    def reset(self, event_name=None):
        if event_name is None:
            for event_type in self._event_types.values():
                event_type.reset()
        else:
            self._event_types[event_name].reset()
        self._queue = Queue()
        self._pending_failure = None, None

    def subscribe_to_event(self, event, handler):
        self._event_types[_get_event_name(event)].subscribe(handler)

    def subscribe_to_events(self, event_handler_pairs):
        for event, handler in event_handler_pairs.items():
            self.subscribe_to_event(event, handler)

    def add_listener(self, listener):
        for event_name in self._event_types:
            handler_name = "on_%s" % event_name
            handler = getattr(listener, handler_name, None)
            if handler and callable(handler):
                self.subscribe_to_event(event_name, handler)

    def unsubscribe_from_event(self, event, handler):
        self._event_types[_get_event_name(event)].unsubscribe(handler)

    def fire(self, event):
        if DEBUG:
            print("Fire event %s" % event)
        self._queue.put(event)

    def end_of_events(self):
        self._queue.put(None)

    def handler_loop(self):
        while True:
            event = self._queue.get()
            if event is None:
                break
            try:
                self._event_types[event.__class__.get_name()].handle(event)
            except Exception as excp:
                self._pending_failure = excp, serialize_current_exception()
                break
            finally:
                self._queue.task_done()

    def get_pending_failure(self):
        return self._pending_failure


eventmgr = EventManager()
register_event = eventmgr.register_events
register_events = eventmgr.register_events
subscribe_to_event = eventmgr.subscribe_to_event
subscribe_to_events = eventmgr.subscribe_to_events
unsubscribe_from_event = eventmgr.unsubscribe_from_event
add_listener = eventmgr.add_listener
reset = eventmgr.reset
fire = eventmgr.fire
handler_loop = eventmgr.handler_loop
end_of_events = eventmgr.end_of_events
get_pending_failure = eventmgr.get_pending_failure


def event(class_):
    register_event(class_)
    return class_


###
# Events related to the test session
###

class _ReportEvent(Event):
    def __init__(self, report):
        super(_ReportEvent, self).__init__()
        self.report = report


@event
class TestSessionStartEvent(_ReportEvent):
    pass


@event
class TestSessionEndEvent(_ReportEvent):
    pass


@event
class TestSessionSetupStartEvent(Event):
    pass


@event
class TestSessionSetupEndEvent(Event):
    pass


@event
class TestSessionTeardownStartEvent(Event):
    pass


@event
class TestSessionTeardownEndEvent(Event):
    pass


###
# Suite events
###

class _SuiteEvent(Event):
    def __init__(self, suite):
        super(_SuiteEvent, self).__init__()
        self.suite = suite

    def __str__(self):
        return "<Event type='%s' suite='%s'>" % (self.get_name(), self.suite.path)


@event
class SuiteStartEvent(_SuiteEvent):
    pass


@event
class SuiteEndEvent(_SuiteEvent):
    pass


@event
class SuiteSetupStartEvent(_SuiteEvent):
    pass


@event
class SuiteSetupEndEvent(_SuiteEvent):
    pass


@event
class SuiteTeardownStartEvent(_SuiteEvent):
    pass


@event
class SuiteTeardownEndEvent(_SuiteEvent):
    pass


###
# Test events
###

class _TestEvent(Event):
    def __init__(self, test):
        super(_TestEvent, self).__init__()
        self.test = test

    def __str__(self):
        return "<Event type='%s' test='%s'>" % (self.get_name(), self.test.path)


@event
class TestStartEvent(_TestEvent):
    pass


@event
class TestEndEvent(_TestEvent):
    pass


@event
class TestSkippedEvent(_TestEvent):
    def __init__(self, test, reason):
        super(TestSkippedEvent, self).__init__(test)
        self.skipped_reason = reason


@event
class TestDisabledEvent(_TestEvent):
    def __init__(self, test, reason):
        super(TestDisabledEvent, self).__init__(test)
        self.disabled_reason = reason


@event
class TestSetupStartEvent(_TestEvent):
    pass


@event
class TestSetupEndEvent(_TestEvent):
    pass


@event
class TestTeardownStartEvent(_TestEvent):
    pass


@event
class TestTeardownEndEvent(_TestEvent):
    pass


###
# Transverse test execution events
###

class RuntimeEvent(Event):
    def __init__(self, location):
        super(RuntimeEvent, self).__init__()
        self.location = location


@event
class StepEvent(RuntimeEvent):
    def __init__(self, location, description, detached=False):
        super(StepEvent, self).__init__(location)
        self.step_description = description
        self.detached = detached

    def __str__(self):
        return "<Event type='%s' description='%s'>" % (
            self.get_name(), self.step_description
        )


@event
class StepEndEvent(RuntimeEvent):
    def __init__(self, location, step):
        super(StepEndEvent, self).__init__(location)
        self.step = step


class SteppedEvent(RuntimeEvent):
    def __init__(self, location, step):
        super(SteppedEvent, self).__init__(location)
        self.step = step


@event
class LogEvent(SteppedEvent):
    def __init__(self, location, step, level, message):
        super(LogEvent, self).__init__(location, step)
        self.log_level = level
        self.log_message = message

    def __str__(self):
        return "<Event type='%s' level='%s' message='%s'>" % (
            self.get_name(), self.log_level, self.log_message
        )


@event
class CheckEvent(SteppedEvent):
    def __init__(self, location, step, description, outcome, details=None):
        super(CheckEvent, self).__init__(location, step)
        self.check_description = description
        self.check_outcome = outcome
        self.check_details = details

    def __str__(self):
        return "<Event type='%s' description='%s' details='%s' outcome='%s'>" % (
            self.get_name(), self.check_description, self.check_details,
            "success" if self.check_outcome else "failure"
        )


@event
class LogAttachmentEvent(SteppedEvent):
    def __init__(self, location, step, path, filename, description, as_image):
        super(LogAttachmentEvent, self).__init__(location, step)
        self.attachment_path = path
        self.attachment_filename = filename
        self.attachment_description = description
        self.as_image = as_image

    def __str__(self):
        return "<Event type='%s' filename='%s' description='%s'>" % (
            self.get_name(), self.attachment_filename, self.attachment_description
        )


@event
class LogUrlEvent(SteppedEvent):
    def __init__(self, location, step, url, description):
        super(LogUrlEvent, self).__init__(location, step)
        self.url = url
        self.url_description = description

    def __str__(self):
        return "<Event type='%s' url='%s' description='%s'>" % (
            self.get_name(), self.url, self.url_description
        )
