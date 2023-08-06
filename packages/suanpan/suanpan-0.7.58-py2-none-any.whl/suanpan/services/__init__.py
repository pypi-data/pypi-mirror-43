# coding=utf-8
from __future__ import print_function

import argparse
import contextlib
import itertools
import tempfile
import time
import traceback
import uuid
from concurrent import futures

import grpc

from suanpan import asyncio, objects
from suanpan.arguments import Int, String
from suanpan.components import Component
from suanpan.dw import dw
from suanpan.log import logger
from suanpan.services import common_pb2, common_pb2_grpc
from suanpan.storage import storage
from suanpan.utils import json


class Handler(Component):
    def __call__(self, serviceObj, request, context, *arg, **kwargs):
        return self.run(serviceObj, request, context, *arg, **kwargs)

    def run(self, serviceObj, request, context, *arg, **kwargs):
        handlerContext = self.init(request, context)
        results = self.runFunc(serviceObj, handlerContext)
        return self.save(handlerContext, results)

    def init(self, request, context):
        restArgs = self.getArgList(request)
        handlerContext = self.getContext(request, context)
        args, restArgs = self.parseArguments(self.getArguments(), restArgs)
        args = self.transformArguments(handlerContext, args)
        setattr(handlerContext, "args", args)
        return handlerContext

    def save(self, context, results):
        outputs = self.saveOutputs(context, results)
        outputs = self.formatAsOuts(outputs)
        outputs = self.stringifyOuts(outputs)
        self.closeContext()
        return outputs

    @contextlib.contextmanager
    def context(self, request, context):
        yield objects.Context(request=request, context=context)

    def getArgList(self, request):
        inputArguments = itertools.chain(
            *[
                ["--{}".format(arg.key), getattr(request, "in{}".format(i + 1), None)]
                for i, arg in enumerate(self.getArguments("inputs"))
                if getattr(request, "in{}".format(i + 1), None) is not None
            ]
        )

        extra = json.loads(request.extra) if request.extra else {}
        output = extra.get("output", {})
        outputArguments = itertools.chain(
            *[
                [
                    "--{}".format(arg.key),
                    self.getOutputTmpValue(request, output.get("out{}".format(i + 1))),
                ]
                for i, arg in enumerate(self.getArguments("outputs"))
                if output.get("out{}".format(i + 1)) is not None
            ]
        )
        return list(itertools.chain(inputArguments, outputArguments))

    def formatAsOuts(self, results):
        return {
            "out{}".format(i + 1): results[arg.key]
            for i, arg in enumerate(self.getArguments("outputs"))
        }

    def stringifyOuts(self, outs):
        return {k: str(v) for k, v in outs.items()}

    def shortenRequestID(self, requestID):
        return requestID.replace("-", "")

    def getOutputTmpValue(self, request, output):
        shortRequestID = self.shortenRequestID(request.id)
        return (
            storage.storagePathJoin(output, shortRequestID)
            if self.isStoragePath(output)
            else "{}_{}".format(output, shortRequestID)
        )

    def isStoragePath(self, value):
        return storage.delimiter in value


class Service(common_pb2_grpc.CommonServicer):

    defaultServiceCall = "call"
    grpcArguments = [
        Int("port", default=8980),
        Int("workers", default=asyncio.WORKERS),
        Int("grpc-max-send-message-length", default=1024 * 1024 * 20),
        Int("grpc-max-recv-message-length", default=1024 * 1024 * 20),
    ]
    dataWarehouseArguments = [
        String("dw-type", default="hive"),
        String("dw-hive-host", default="localhost"),
        Int("dw-hive-port"),
        String("dw-hive-database", default="default"),
        String("dw-hive-username"),
        String("dw-hive-password"),
        String("dw-hive-auth"),
        String("dw-odps-access-id"),
        String("dw-odps-access-key"),
        String(
            "dw-odps-endpoint", default="http://service.cn.maxcompute.aliyun.com/api"
        ),
        String("dw-odps-project"),
    ]
    storageArguments = [
        String("storage-type", default="oss"),
        String("storage-oss-access-id"),
        String("storage-oss-access-key"),
        String("storage-oss-bucket-name", default="suanpan"),
        String("storage-oss-endpoint", default="http://oss-cn-beijing.aliyuncs.com"),
        String("storage-oss-delimiter", default="/"),
        String("storage-oss-temp-store", default=tempfile.gettempdir()),
        Int("storage-oss-download-num-threads", default=1),
        String("storage-oss-download-store-name", default=".py-oss-download"),
        Int("storage-oss-upload-num-threads", default=1),
        String("storage-oss-upload-store-name", default=".py-oss-upload"),
    ]
    defaultArguments = grpcArguments + dataWarehouseArguments + storageArguments
    arguments = []

    def __init__(self):
        logger.setLogger(self.name)
        self.args = self.parseArgs()
        self.transformArguments(objects.Context(), self.args)
        self.setDataWarehouse(self.args)
        self.setStorage(self.args)
        self.afterInit()

    @property
    def name(self):
        return self.__class__.__name__

    def generateRequestId(self):
        return uuid.uuid4().hex

    def formatMessage(self, request, msg, costTime=None):
        msgs = [request.id, request.type or self.defaultServiceCall, msg]
        if costTime is not None:
            msgs.insert(-1, "{}s".format(costTime))
        return " - ".join(msgs)

    def predict(self, request, context):
        try:
            logger.info(self.formatMessage(request, msg="Start"))
            startTime = time.time()
            callFunction = self.getCallFunction(request, context)
            outputs = callFunction(self, request, context) or {}
            result = dict(success=True, **outputs)
            endTime = time.time()
            costTime = round(endTime - startTime, 3)
            logger.info(self.formatMessage(request, msg="Done", costTime=costTime))
        except Exception:
            tracebackInfo = traceback.format_exc()
            result = dict(success=False, msg=tracebackInfo)
            endTime = time.time()
            costTime = round(endTime - startTime, 3)
            logger.error(
                self.formatMessage(request, msg=tracebackInfo, costTime=costTime)
            )
        finally:
            return common_pb2.Response(request_id=request.id, **result)

    def getCallFunction(self, request, context):
        serviceCall = request.type or self.defaultServiceCall
        callFunction = getattr(self, serviceCall, None)
        if not callFunction:
            raise Exception(
                "Unknown service call: {}.{}".format(self.name, serviceCall)
            )
        return callFunction

    def call(self, request, context, *args):
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def start(self):
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=self.args.workers),
            options=[
                (
                    "grpc.max_send_message_length",
                    self.args.grpc_max_send_message_length,
                ),
                (
                    "grpc.max_receive_message_length",
                    self.args.grpc_max_recv_message_length,
                ),
            ],
        )
        common_pb2_grpc.add_CommonServicer_to_server(self, server)
        server.add_insecure_port("[::]:{}".format(self.args.port))
        server.start()
        logger.info("{} started!".format(self.name))
        try:
            _ONE_DAY_IN_SECONDS = 60 * 60 * 24
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)

    def setDataWarehouse(self, args):
        return dw.setBackend(
            **self.defaultArgumentsFormat(args, self.dataWarehouseArguments)
        )

    def setStorage(self, args):
        return storage.setBackend(
            **self.defaultArgumentsFormat(args, self.storageArguments)
        )

    def getArguments(self):
        return itertools.chain(self.defaultArguments, self.arguments)

    def parseArgs(self):
        return self.parseArguments(self.getArguments())

    def parseArguments(self, arguments, *args, **kwargs):
        parser = argparse.ArgumentParser(*args, **kwargs)
        for arg in arguments:
            arg.addParserArguments(parser)
        return parser.parse_known_args()[0]

    def transformArguments(self, context, args):
        self.loadArguments(args, self.arguments)
        self.formatArguments(context, self.arguments)
        for arg in self.arguments:
            setattr(self.args, arg.key, arg.value)
        return self.args

    def loadArguments(self, args, arguments):
        return {arg.key: arg.load(args) for arg in arguments}

    def formatArguments(self, context, arguments):
        return {arg.key: arg.format(context) for arg in arguments}

    def defaultArgumentsFormat(self, args, arguments):
        arguments = (arg.key.replace("-", "_") for arg in arguments)
        return {
            self.defaultArgumentKeyFormat(arg): getattr(args, arg) for arg in arguments
        }

    def defaultArgumentKeyFormat(self, key):
        return self.toCamelCase(self.removePrefix(key))

    def removePrefix(self, string, delimiter="_", num=1):
        pieces = string.split(delimiter)
        pieces = pieces[num:] if len(pieces) > num else pieces
        return delimiter.join(pieces)

    def toCamelCase(self, string, delimiter="_"):
        camelCaseUpper = lambda i, s: s[0].upper() + s[1:] if i and s else s
        return "".join(
            [camelCaseUpper(i, s) for i, s in enumerate(string.split(delimiter))]
        )

    def afterInit(self):
        pass
