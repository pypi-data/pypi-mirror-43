# coding: utf-8

import typing
import functools
import logging
import uuid
import json


X_APPLICATION_TRACE_ID: str = 'x-application-trace-id'


class LamBlackBox():
    class Logger():
        def __init__(self, trace_id: str, debug: bool = False) ->None:
            self.trace_id = trace_id
            self.logger = logging.getLogger()
            if debug:
                self.logger.setLevel(logging.DEBUG)
            else:
                self.logger.setLevel(logging.INFO)

        def set_trace_id(self, obj: typing.Dict)->typing.Dict:
            obj.update({X_APPLICATION_TRACE_ID: self.trace_id})
            return obj

        def debug(self, obj: typing.Dict)->None:
            log = json.dumps(self.set_trace_id(obj))
            self.logger.debug(log)

        def info(self, obj: typing.Dict)->None:
            log = json.dumps(self.set_trace_id(obj))
            self.logger.info(log)

        def warning(self, obj: typing.Dict)->None:
            log = json.dumps(self.set_trace_id(obj))
            self.logger.warning(log)

        def error(self, obj: typing.Dict)->None:
            log = json.dumps(self.set_trace_id(obj))
            self.logger.error(log)

        def critical(self, obj: typing.Dict)->None:
            log = json.dumps(self.set_trace_id(obj))
            self.logger.critical(log)

    def __init__(self)->None:
        pass

    def gen_uuid(self)->str:
        return str(uuid.uuid4())


def apigateway(func):
    @functools.wraps(func)
    def wrapper(event, context):
        lbb = LamBlackBox()
        trace_id = event['headers'].get(X_APPLICATION_TRACE_ID, lbb.gen_uuid())
        logger = LamBlackBox.Logger(trace_id)
        logger.info({'event': event})

        try:
            if 'headers' not in event:
                event['headers'] = {}
            event['headers'][X_APPLICATION_TRACE_ID] = trace_id
            ret = func(event, context)
            if 'headers' not in ret:
                ret['headers'] = {}
            ret['headers'][X_APPLICATION_TRACE_ID] = trace_id
            logger.info({'result': ret})
        except Exception as e:
            error_string = str(e)
            logger.error({'result': error_string})
            ret = {
                'statusCode': 500,
                'headers': {
                    X_APPLICATION_TRACE_ID: trace_id,
                },
                'body': json.dumps({'result': error_string})
            }
        return ret
    return wrapper
