import pytest

import json
import sdk_cmd as command
import sdk_spin as spin

from tests.config import (
    DEFAULT_PARTITION_COUNT,
    DEFAULT_REPLICATION_FACTOR,
    PACKAGE_NAME,
    DEFAULT_BROKER_COUNT,
    DEFAULT_PLAN_NAME,
    DEFAULT_PHASE_NAME,
    DEFAULT_POD_TYPE,
    DEFAULT_TASK_NAME
)

SERVICE_NAME = PACKAGE_NAME

DEFAULT_TOPIC_NAME = 'topic1'
EPHEMERAL_TOPIC_NAME = 'topic_2'

STATIC_PORT_OPTIONS_DICT = {"brokers": {"port": 9092}}
DYNAMIC_PORT_OPTIONS_DICT = {"brokers": {"port": 0}}
DEPLOY_STRATEGY_SERIAL_CANARY = {"service": {"deploy_strategy": "serial-canary"}}


def service_cli(cmd_str, get_json=True, service_name=SERVICE_NAME):
    full_cmd = '{} --name={} {}'.format(PACKAGE_NAME, service_name, cmd_str)
    ret_str = command.run_cli(full_cmd)
    if get_json:
        return json.loads(ret_str)
    else:
        return ret_str


def broker_count_check(count, service_name=SERVICE_NAME):
    def fun():
        try:
            if len(service_cli('broker list', service_name=service_name)) == count:
                return True
        except:
            pass
        return False

    spin.time_wait_return(fun)


# Only use if need to wait for plan resource to start
def service_plan_wait(plan_name):
    def fun():
        try:
            return service_cli('plan show --json {}'.format(plan_name))
        except:
            return False

    return spin.time_wait_return(fun)
