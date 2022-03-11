# Copyright 2021 Massimiliano Angelino
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
try:
    import tracepointdebug
    tracepointdebug.start()
except ImportError as e:
    pass

import time
import os
import glob
from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import (
    QOS
)
from threading import Event

device_id=os.environ.get("AWS_IOT_THING_NAME", "nil")

topic = os.environ.get("TOPIC", "test/docker_comp")
message = os.environ.get("MESSAGE", f"Hello, World from {device_id}")
qos = QOS.AT_LEAST_ONCE

client = GreengrassCoreIPCClientV2()

def message_handler(msg):
    try:
        print(f"Got new message \"{msg.message.payload.decode('utf8')}\" from AWS IOT Core on \"{msg.message.topic_name}\"")
        print(msg)
        client.publish_to_iot_core(topic_name=topic+"/resp", payload=bytes(message, "utf8"), qos=qos)
        print("done.")
    except Exception as ex:
        print(ex)
    
client.subscribe_to_iot_core(topic_name=topic, qos=QOS.AT_LEAST_ONCE, on_stream_event=message_handler)

while True: 
    try:
        client.publish_to_iot_core(topic_name=topic, qos=0, payload=bytes(message, "utf8"))
    except Exception as ex:
        print(ex)
    time.sleep(5)
