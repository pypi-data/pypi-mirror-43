import json
import datetime
import logging
from hippodamia.agentshadow.properties import Properties
import hippodamia.agentshadow.states.state_machine
import pelops.mylogger
from hippodamia.enums import Necessity
from hippodamia.agentshadow.states.event_ids import event_ids
from hippodamia.agentshadow.states.state_ids import state_ids
from hippodamia.agentshadow.shadowdata import ShadowData
from hippodamia.enums import Health
from hippodamia.enums import Necessity


class AgentShadow:
    _mqtt_client = None
    _logger = None
    _update_available = None

    _state_machine = None

    _basic_topics = None

    service_timings = None
    _agent_timings = None
    activity_topics = None
    shadow_data = None
    properties = None
    states = None

    def __init__(self, topics, service_timings, agent_timings, update_available, mongo_client, mqtt_client, logger,
                 preload_config=None, gid=None):
        self._mqtt_client = mqtt_client
        self._logger = pelops.mylogger.get_child(logger, "AgentShadow")
        self._basic_topics = topics
        self.service_timings = service_timings
        self._agent_timings = agent_timings
        self._update_available = update_available

        self.properties = Properties(self._logger)

        if gid:
            self._logger.info("__init__ - setting gid")
            self.properties.gid = str(gid)
            self.properties.necessity = Necessity.SPONTANEOUS
        elif preload_config:
            self._process_preload_config(preload_config)
        else:
            self._logger.error("__init__ - preload_config and gid are None")
            raise ValueError("__init__ - preload_config and gid are None")

        if self.properties.gid is None:
            self._logger.error("__init__ - gid is None")
            raise ValueError("__init__ - gid is None")
        else:
            self._logger = pelops.mylogger.get_child(logger, str(self.properties.gid))

        self.shadow_data = ShadowData(str(self.properties.gid), self.set_log_health)
        self.shadow_data.process_properties(self.properties)

        self._set_basic_topics()
        self._init_state_machine()

    def get_state_id(self):
        return self._state_machine.get_active_state().id

    def set_state_health(self, health):
        if self.properties.necessity == Necessity.REQUIRED:
            self.properties.state_health = health
        else:
            self.properties.state_health = min(Health.YELLOW, health)
        self._logger.debug("set_state_health to {} (original: {})"
                           .format(self.properties.state_health.name, health.name))

    def set_log_health(self, max_level):
        if max_level >= logging.ERROR:
            self.properties.log_health = Health.RED
        else:
            self.properties.log_health = Health.GREEN
        self._logger.debug("set_log_health to {} (level: {})"
                           .format(self.properties.log_health.name, logging.getLevelName(max_level)))

    def _set_basic_topics(self):
        self.activity_topics = {}
        activity_base = self._basic_topics["activity-base"]
        if activity_base[-1] == "/":
            activity_base = activity_base[:-1]
        self.activity_topics["ping"] = "{}/{}/ping".format(activity_base, self.properties.gid)
        self.activity_topics["runtime"] = "{}/{}/runtime".format(activity_base, self.properties.gid)
        self.activity_topics["config"] = "{}/{}/config".format(activity_base, self.properties.gid)
        self.activity_topics["end"] = "{}/{}/end".format(activity_base, self.properties.gid)
        self.activity_topics["logger"] = "{}/{}/logger".format(activity_base, self.properties.gid)

    def _process_preload_config(self, preload_config):
        self._logger.info("_process_preload_config - start")
        self._logger.debug("_process_preload_config: {}".format(preload_config))

        if "gid" in preload_config:
            self.properties.gid = str(preload_config["gid"])
        if "name" in preload_config:
            self.properties.name = preload_config["name"]
        if "location" in preload_config:
            self.properties.location = preload_config["location"]
        if "room" in preload_config:
            self.properties.room = preload_config["room"]
        if "device" in preload_config:
            self.properties.device = preload_config["device"]
        if "necessity" in preload_config:
            necessity = Necessity.get_enum(preload_config["necessity"])
            if necessity != Necessity.OPTIONAL and necessity != Necessity.REQUIRED:
                msg = "_process_preload_config - unexpected value '{}' for necessity. must " \
                      "be 'required' or 'optional'.",format(preload_config["necessity"])
                self._logger.error(msg)
                raise ValueError(msg)
            self.properties.necessity = necessity
        self._logger.info("_process_preload_config - finished")

    def _init_state_machine(self):
        self._state_machine, self.states = hippodamia.agentshadow.states.\
            state_machine.create(self._update_available, self.service_timings, self.set_state_health,
                                 self.shadow_data.logger.reset_max_level, self._logger)
        self.states[state_ids.ONBOARDING].func_send_onboarding_response = self._send_onboarding_response
        self.states[state_ids.ONBOARDING].func_deactivate_recv_messages = self.deactivate_recv_messages
        self.states[state_ids.ONBOARDING].func_activate_recv_messages = self.activate_recv_messages
        self.states[state_ids.STOPPED].func_deactivate_recv_messages = self.deactivate_recv_messages

    def start(self):
        self._state_machine.start()

    def stop(self):
        try:
            # trying to initiate offboarding no matter what the current state is
            self._state_machine.asyncoperate(event_ids.OFFBOARDING)
        except KeyError:
            pass  # not every every state has a link to offboarding
        self._state_machine.stop()

    def process_onboarding_request(self, message):
        """
        {
          "uuid": "550e8400-e29b-11d4-a716-446655440000",
          "onboarding-topic": "/hippodamia/550e8400-e29b-11d4-a716-446655440000",
          "protocol-version": 1,
          "timestamp": "1985-04-12T23:20:50.520Z",
          "identifier": {
            "gid": 1,
            "type": "copreus",
            "version": "0.3.1",
            "name": "display-driver",
            "location": "flat",
            "room": "living room",
            "device": "thermostat",
            "decription": "lorem ipsum",
            "host-name": "rpi",
            "node-id": "00-07-E9-AB-CD-EF",
            "ips": [
              "192.168.0.1",
              "10.0.1.2",
              "2001:0db8:85a3:08d3:1319:8a2e:0370:7344"
            ],
            "config-hash": "cf23df2207d99a74fbe169e3eba035e633b65d94"
          }
        }
        """
        self._logger.info("process_onboarding_request - start")
        self._logger.debug("process_onboarding_request - message: {}".format(message))

        self.properties.uuid = message["uuid"]
        self.properties.onboarding_topic = message["onboarding-topic"]
        self.properties.protocol_version = message["protocol-version"]

        self.properties.gid = str(message["identifier"]["gid"])
        self.properties.location = message["identifier"]["location"]
        self.properties.room = message["identifier"]["room"]
        self.properties.device = message["identifier"]["device"]

        self.properties.type = message["identifier"]["type"]
        self.properties.version = message["identifier"]["version"]
        self.properties.name = message["identifier"]["name"]
        self.properties.description = message["identifier"]["description"]
        self.properties.host_name = message["identifier"]["host-name"]
        self.properties.node_id = message["identifier"]["node-id"]
        self.properties.ips = message["identifier"]["ips"]
        self.properties.config_hash = message["identifier"]["config-hash"]

        self.shadow_data.process_request(message)
        self.shadow_data.process_properties(self.properties)

        self._logger.info("process_onboarding_request - finished")

        self._state_machine.asyncoperate(event_ids.ONBOARDING_REQUEST)
        
    def _send_onboarding_response(self):
        """
        {
            "uuid": "550e8400-e29b-11d4-a716-446655440000",
            "gid": 1,
            "topics-activity": {
                "ping": "/hippodamia/commands",
                "runtime": "/hippodamia/commands",
                "config": "/hippodamia/commands",
                "end": "/hippodamia/commands",
                "logger": "/hippodamia/commands"
            },
            "topics-commands": {
                "end": "/hippodamia/commands",
                "reonboarding": "/hippodamia/commands",
                "ping_on_request": "/hippodamia/commands",
                "config_on_request": "/hippodamia/commands",
                "runtime_on_request": "/hippodamia/commands",
                "heartbeat": "/hippodamia/commands"
            },
            "timings": {
                "send-ping": 60,
                "send-runtime": 500,
                "send-config": 3600,
                "expect-heartbeat": 120
            }
        }
        """
        message = {
            "uuid": self.properties.uuid,
            "gid": self.properties.gid,
            "topics-activity": {
                "ping": self.activity_topics["ping"],
                "runtime": self.activity_topics["runtime"],
                "config": self.activity_topics["config"],
                "end": self.activity_topics["end"],
                "logger": self.activity_topics["logger"],
            },
            "topics-commands": {
                "end": self._basic_topics["command-end"],
                "reonboarding": self._basic_topics["command-reonboarding"],
                "ping_on_request": self._basic_topics["command-ping-on-request"],
                "config_on_request": self._basic_topics["command-config-on-request"],
                "runtime_on_request": self._basic_topics["command-runtime-on-request"],
                "heartbeat": self._basic_topics["heartbeat"],
            },
            "timings": {
                "send-ping": self._agent_timings["send-ping"],
                "send-runtime": self._agent_timings["send-runtime"],
                "send-config": self._agent_timings["send-config"],
                "expect-heartbeat": self._agent_timings["expect-heartbeat"]
            }
        }
        message = json.dumps(message)
        self._logger.debug("_send_onboarding_response - topic: {}, message: {}"
                           .format(self.properties.onboarding_topic, message))
        self._logger.debug(self.properties.export_dict())
        self._mqtt_client.publish(self.properties.onboarding_topic, message)

    def activate_recv_messages(self):
        self._logger.info("activate_recv_messages")

        self._logger.debug("activate_recv_messages - topic ping {}".format(self.activity_topics["ping"]))
        self._mqtt_client.subscribe(self.activity_topics["ping"], self._handler_ping, ignore_duplicate=True)

        self._logger.debug("activate_recv_messages - topic runtime {}".format(self.activity_topics["runtime"]))
        self._mqtt_client.subscribe(self.activity_topics["runtime"], self._handler_runtime, ignore_duplicate=True)

        self._logger.debug("activate_recv_messages - topic config {}".format(self.activity_topics["config"]))
        self._mqtt_client.subscribe(self.activity_topics["config"], self._handler_config, ignore_duplicate=True)

        self._logger.debug("activate_recv_messages - topic end {}".format(self.activity_topics["end"]))
        self._mqtt_client.subscribe(self.activity_topics["end"], self._handler_end, ignore_duplicate=True)

        self._logger.debug("activate_recv_messages - topic logger {}".format(self.activity_topics["logger"]))
        self._mqtt_client.subscribe(self.activity_topics["logger"], self._handler_logger, ignore_duplicate=True)

    def deactivate_recv_messages(self):
        self._logger.info("deactivate_recv_messages")

        self._logger.debug("activate_recv_messages - topic ping {}".format(self.activity_topics["ping"]))
        self._mqtt_client.unsubscribe(self.activity_topics["ping"], self._handler_ping, ignore_not_found=True)

        self._logger.debug("activate_recv_messages - topic runtime {}".format(self.activity_topics["runtime"]))
        self._mqtt_client.unsubscribe(self.activity_topics["runtime"], self._handler_runtime, ignore_not_found=True)

        self._logger.debug("activate_recv_messages - topic config {}".format(self.activity_topics["config"]))
        self._mqtt_client.unsubscribe(self.activity_topics["config"], self._handler_config, ignore_not_found=True)

        self._logger.debug("activate_recv_messages - topic end {}".format(self.activity_topics["end"]))
        self._mqtt_client.unsubscribe(self.activity_topics["end"], self._handler_end, ignore_not_found=True)

        self._logger.debug("activate_recv_messages - topic logger {}".format(self.activity_topics["logger"]))
        self._mqtt_client.unsubscribe(self.activity_topics["logger"], self._handler_logger, ignore_not_found=True)

    def _handler_ping(self, message):
        self._logger.info("_handler_ping - received ping")
        message = json.loads(message.decode("utf8"))
        self.shadow_data.process_ping(message)
        self._state_machine.asyncoperate(event_ids.REGULAR_MESSAGE)

    def _handler_runtime(self, message):
        self._logger.info("_handler_runtime - received runtime")
        message = json.loads(message.decode("utf8"))
        self.shadow_data.process_runtime(message)
        self._state_machine.asyncoperate(event_ids.REGULAR_MESSAGE)

    def _handler_config(self, message):
        self._logger.info("_handler_config - received config")
        message = json.loads(message.decode("utf8"))
        self.shadow_data.process_config(message)
        self._state_machine.asyncoperate(event_ids.REGULAR_MESSAGE)

    def _handler_end(self, message):
        self._logger.info("_handler_end - received end")
        message = json.loads(message.decode("utf8"))
        self.shadow_data.process_end(message)
        self._state_machine.asyncoperate(event_ids.OFFBOARDING)

    def _handler_logger(self, message):
        self._logger.info("_handler_logger - received logger")
        message = json.loads(message.decode("utf8"))
        self.shadow_data.process_logger(message)
        self._state_machine.asyncoperate(event_ids.REGULAR_MESSAGE)

    def general_stats(self):
        stats = {}

        stats["micro-service"] = {
            "name": self.properties.name,
            "type": self.properties.type,
            "uptime": self.properties.service_uptime
        }

        since = self.states[self.get_state_id()].timestamp_on_entry
        try:
            duration = datetime.datetime.now() - since
        except TypeError:
            duration = None
        stats["active-state"] = {
            "output": self.get_state_id().name,
            "since": since,
            "duration": duration
        }

        stats["machine-state-states"] = {}
        for id, state in self.states.items():
            try:
                duration = state.timestamp_on_exit - state.timestamp_on_entry
            except TypeError:
                try:
                    duration = datetime.datetime.now() - state.timestamp_on_entry
                except TypeError:
                    duration = "-"
            stats["machine-state-states"][id.name] = {
                "counter_on_entry": state.counter_on_exit,
                "timestamp_on_entry": state.timestamp_on_entry,
                "counter_on_exit": state.counter_on_exit,
                "timestamp_on_exit": state.timestamp_on_exit,
                "duration": duration
            }

        stats["message-stats"] = {}
        for id, counter in self.shadow_data.get_counter_dict().items():
            stats["message-stats"][id] = counter

        stats["topics"] = {}
        for id, topic in self.activity_topics.items():
            stats["topics"][id] = topic

        stats["timings"] = {}
        for id, timing in self.service_timings.items():
            stats["timings"][id] = timing

        return stats

    def logger_stats(self):
        stats = {
            "max-level": self.shadow_data.logger.max_level,
            "combined list": self.shadow_data.logger.flat_list.stats(),
            "CRITICAL": self.shadow_data.logger.level_dict[logging.CRITICAL].stats(),
            "ERROR": self.shadow_data.logger.level_dict[logging.ERROR].stats(),
            "WARNING": self.shadow_data.logger.level_dict[logging.WARNING].stats(),
            "INFO": self.shadow_data.logger.level_dict[logging.INFO].stats(),
            "DEBUG": self.shadow_data.logger.level_dict[logging.DEBUG].stats()
        }
        return stats

    def overall_stats(self):
        stats = {
            "general": self.general_stats(),
            "logger": self.logger_stats()
        }
        stats["properties"] = {
            "timestamp": self.shadow_data.properties_time,
            "entries": self.shadow_data.properties
        }
        stats["ping"] = {
            "counter": self.shadow_data.ping_counter,
            "timestamp": self.shadow_data.ping_time,
            "message": self.shadow_data.ping
        }
        stats["config"] = {
            "counter": self.shadow_data.config_counter,
            "timestamp": self.shadow_data.config_time,
            "message": self.shadow_data.config
        }
        stats["runtime"] = {
            "counter": self.shadow_data.runtime_counter,
            "timestamp": self.shadow_data.runtime_time,
            "message": self.shadow_data.runtime
        }
        stats["request"] = {
            "counter": self.shadow_data.request_counter,
            "timestamp": self.shadow_data.request_time,
            "message": self.shadow_data.request
        }

        return stats
