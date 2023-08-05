# coding=utf-8
from __future__ import print_function

import functools
import itertools
import time
import traceback

import redis

from suanpan import utils
from suanpan.log import logger


MQ_DELIVER_KEY = "_suanpan_mq_deliver"


class RedisMQ(object):
    def __init__(
        self,
        redisHost="localhost",
        redisPort=6379,
        redisRealtime=False,
        options=None,
        client=None,
        **kwargs
    ):
        self.options = options or {}
        self.options.update(host=redisHost, port=redisPort, realtime=redisRealtime)
        if client and not isinstance(client, redis.Redis):
            raise Exception("Invalid client: {}".format(client))
        self.client = client or redis.Redis(
            host=self.options["host"], port=self.options["port"], decode_responses=True
        )

    @property
    def connected(self):
        return bool(self.client.connection)

    def createQueue(self, name, group="default", consumeID="0", force=False):
        if force:
            self.deleteQueue(name)
        return self._createQueue(name, group=group, consumeID=consumeID)

    def _createQueue(self, name, group="default", consumeID="0"):
        try:
            return self.client.xgroup_create(name, group, id=consumeID, mkstream=True)
        except Exception:
            traceback.print_exc()
            raise Exception("Queue existed: {}".format(name))

    def deleteQueue(self, *names):
        return self.client.delete(*names)

    # def hasQueue(self, name, group="default"):
    #     try:
    #         queue = self.client.xinfo_stream(name)
    #         groups = self.client.xinfo_groups(name)
    #         return any(g["name"].decode() == group for g in groups)
    #     except Exception:
    #         return False

    def sendMessage(
        self, queue, data, messageID="*", maxlen=1000, trimImmediately=False
    ):
        return self.client.xadd(
            queue, data, id=messageID, maxlen=maxlen, approximate=(not trimImmediately)
        )

    def recvMessages(
        self,
        queue,
        group="default",
        consumer="unknown",
        noack=False,
        block=None,
        count=1,
        consumeID=">",
    ):
        messages = self.client.xreadgroup(
            group, consumer, {queue: consumeID}, count=count, block=block, noack=noack
        )
        return list(self._parseMessagesGenerator(messages, group))

    def subscribeQueue(
        self,
        queue,
        group="default",
        consumer="unknown",
        noack=False,
        block=None,
        count=1,
        consumeID=">",
        delay=1,
        errDelay=1,
        errCallback=logger.error,
    ):
        while True:
            try:
                messages = self.recvMessages(
                    queue,
                    group=group,
                    consumer=consumer,
                    noack=noack,
                    block=block,
                    count=count,
                    consumeID=consumeID,
                )
            except Exception as e:
                errCallback(e)
                time.sleep(errDelay)
                continue

            if not messages:
                time.sleep(delay)
                continue

            for message in messages:
                yield message
                self.client.xack(queue, group, message["id"])

    def recvPendingMessagesInfo(
        self,
        queue,
        group="default",
        consumer="unknown",
        start="-",
        end="+",
        count=None,
        countEveryTime=None,
    ):
        countEveryTime = countEveryTime or count or 100
        messages = []
        while True:
            msgs = self.client.xpending_range(
                queue, group, start, end, countEveryTime, consumername=consumer
            )
            messages.extend(msgs)
            if not msgs or (count and len(messages) >= count):
                return messages

    def retryPendingMessages(
        self,
        queue,
        group="default",
        consumer="unknown",
        count=100,
        maxTimes=3,
        timeout=1000,
        errCallback=logger.error,
        maxlen=1000,
        trimImmediately=False,
    ):
        pendingMessages = {
            msg["id"]: msg
            for msg in self.recvMessages(
                queue, group=group, consumer=consumer, count=count, consumeID="0"
            )
        }
        pendingInfos = {
            msg["message_id"]: msg
            for msg in self.recvPendingMessagesInfo(
                queue, group=group, consumer=consumer, count=count
            )
        }
        for mid in pendingMessages.keys():
            message = pendingMessages[mid]
            info = pendingInfos.get(mid, {})
            message = utils.merge(message, info)
            data = message["data"]
            deliveredTimes = int(data.pop(MQ_DELIVER_KEY, 1))
            if deliveredTimes >= maxTimes:
                logger.error(
                    "Message {} retry failed {} times. Drop!".format(
                        message["id"], deliveredTimes
                    )
                )
                errCallback(message)
                self.client.xack(queue, group, message["id"])
                continue
            timeSinceDelivered = message.get("time_since_delivered", 0) * 1000
            if timeSinceDelivered < timeout:
                logger.warning(
                    "Message {} maybe lost: {} < {}".format(
                        message["id"], timeSinceDelivered, timeout
                    )
                )
                continue
            success = self.client.xack(queue, group, message["id"])
            if success:
                data.update({MQ_DELIVER_KEY: deliveredTimes + 1})
                self.sendMessage(
                    queue, data, maxlen=maxlen, trimImmediately=trimImmediately
                )
                logger.warning("Message send back to queue: {}".format(data))

    def _parseMessagesGenerator(self, messages, group):
        for message in messages:
            queue, items = message
            for item in items:
                mid, data = item
                if not data:
                    import pdb

                    pdb.set_trace()
                yield {"id": mid, "data": data, "queue": queue, "group": group}
