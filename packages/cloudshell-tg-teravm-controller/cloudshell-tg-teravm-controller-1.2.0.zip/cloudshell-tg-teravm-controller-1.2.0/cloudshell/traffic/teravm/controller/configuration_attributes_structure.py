import re

from cloudshell.traffic.teravm.controller import constants


class TrafficGeneratorControllerResource(object):
    def __init__(self, address=None, family=None, shell_type=None, shell_name=None, fullname=None, name=None,
                 default_test_user=None, user=None, password=None, attributes=None):
        """

        :param str address: IP address of the resource
        :param str family: resource family
        :param str shell_name: shell name
        :param str fullname: full name of the resource
        :param str name: name of the resource
        :param str default_test_user: test user for running tests (will be used in case when "Test User" attr
        is not provided)
        :param str user: controller CLI user
        :param str password: controller CLI password
        :param dict[str, str] attributes: attributes of the resource
        """
        self.address = address
        self.family = family
        self.shell_name = shell_name
        self.fullname = fullname
        self.name = name
        self.attributes = attributes or {}
        self.default_test_user = default_test_user
        self.user = user
        self.password = password

        if shell_name:
            self.namespace_prefix = "{}.".format(self.shell_name)
            self.shell_type = "{}.".format(shell_type)
        else:
            self.namespace_prefix = ""
            self.shell_type = ""

    @property
    def cli_connection_type(self):
        """

        :rtype: str
        """
        return constants.CLI_CONNECTION_TYPE

    @property
    def cli_tcp_port(self):
        """

        :rtype: str
        """
        return constants.CLI_TCP_PORT

    @property
    def sessions_concurrency_limit(self):
        """

        :rtype: float
        """
        return constants.SESSIONS_CONCURRENCY_LIMIT

    @property
    def test_files_location(self):
        """

        :rtype: float
        """
        return self.attributes.get("{}Test Files Location".format(self.namespace_prefix), "")

    @property
    def test_user(self):
        """

        :rtype: float
        """
        return self.attributes.get("{}Test User".format(self.namespace_prefix)) or self.default_test_user

    @property
    def test_user_password(self):
        """

        :rtype: float
        """
        return self.attributes.get("{}Test User Password".format(self.namespace_prefix), "")

    @staticmethod
    def _get_default_test_user(reservation_id):
        """Get valid test username based on reservation id

        :param str reservation_id:
        :return:
        """
        return re.sub("[^0-9a-zA-Z]", "", reservation_id)[:32]

    @staticmethod
    def _get_resource_attribute_value(resource, attribute_name, namespace_prefix):
        """

        :param resource cloudshell.api.cloudshell_api.ResourceInfo:
        :param str attribute_name:
        """
        for attribute in resource.ResourceAttributes:
            if attribute.Name.lower() == "{namespace}{attribute_name}".format(namespace=namespace_prefix,
                                                                              attribute_name=attribute_name).lower():
                return attribute.Value

    @staticmethod
    def _get_chassis_model(cs_api, reservation_id):
        """

        :param cs_api:
        :param reservation_id:
        :return:
        """
        for resource in cs_api.GetReservationDetails(reservationId=reservation_id).ReservationDescription.Resources:
            if resource.ResourceModelName in constants.CHASSIS_MODELS:
                return cs_api.GetResourceDetails(resource.Name)

        raise Exception("Unable to find {} model in the current reservation".format(constants.CHASSIS_MODELS))

    @classmethod
    def from_context(cls, context, shell_type=None, shell_name=None):
        """

        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :param str shell_type: shell type
        :param str shell_name: shell name
        :return:
        """
        return cls(address=context.resource.address,
                   family=context.resource.family,
                   shell_type=shell_type,
                   shell_name=shell_name,
                   fullname=context.resource.fullname,
                   name=context.resource.name,
                   attributes=dict(context.resource.attributes))

    @classmethod
    def create_from_chassis_resource(cls, context, cs_api, shell_type=None, shell_name=None):
        """Create an instance of TrafficGeneratorControllerResource from the given context

        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :param cs_api:
        :param str shell_type: shell type
        :param str shell_name: shell name
        :rtype: TrafficGeneratorControllerResource
        """
        reservation_id = context.reservation.reservation_id
        default_test_user = cls._get_default_test_user(reservation_id)
        chassis_resource = cls._get_chassis_model(cs_api=cs_api, reservation_id=reservation_id)

        if chassis_resource.ResourceModelName in (constants.CHASSIS_MODEL_2G, constants.VIRTUAL_CHASSIS_MODEL_2G):
            namespace_prefix = "{}.".format(chassis_resource.ResourceModelName)
        else:
            namespace_prefix = ""

        user = cls._get_resource_attribute_value(resource=chassis_resource,
                                                 attribute_name="User",
                                                 namespace_prefix=namespace_prefix)

        password = cls._get_resource_attribute_value(resource=chassis_resource,
                                                     attribute_name="Password",
                                                     namespace_prefix=namespace_prefix)

        return cls(address=chassis_resource.FullAddress,
                   family=context.resource.family,
                   shell_type=shell_type,
                   shell_name=shell_name,
                   fullname=context.resource.fullname,
                   name=context.resource.name,
                   default_test_user=default_test_user,
                   user=user,
                   password=password,
                   attributes=dict(context.resource.attributes))
