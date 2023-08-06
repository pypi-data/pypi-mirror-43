CLI_CONNECTION_TYPE = "SSH"
CLI_TCP_PORT = 22
SESSIONS_CONCURRENCY_LIMIT = 1

TEST_GROUP_NAME = "CS_TEST_GROUP"
TEST_GROUP_FILE = "/home/cli/cs_test_group_{}.xml"  # todo: remove "cli" from path, it may differ
TEST_RESULTS_FILE = "/home/cli/cs_test_result_{}.zip"
TEST_AGENT_NUMBER = "1"  # todo: clarify hardcode it or add another resource

CS_TEST_RESULTS_ATTACHMENTS_FILE = "Test Group Results.zip"

CHASSIS_MODEL_1G = "TeraVM Chassis"
CHASSIS_MODEL_2G = "Traffic TeraVM 2G"
VIRTUAL_CHASSIS_MODEL_2G = "TeraVM Virtual Chassis"
CHASSIS_MODELS = [CHASSIS_MODEL_1G, CHASSIS_MODEL_2G, VIRTUAL_CHASSIS_MODEL_2G]

LOGICAL_NAME_ATTR_PORT_MODEL_MAP = {
    "TeraVM Virtual Traffic Generator Port": "Logical Name",
    "Traffic TeraVM 2G.GenericTrafficGeneratorPort": "CS_TrafficGeneratorPort.Logical Name",
    "TeraVM Virtual Blade.VirtualTrafficGeneratorPort": "CS_VirtualTrafficGeneratorPort.Logical Name",
}
