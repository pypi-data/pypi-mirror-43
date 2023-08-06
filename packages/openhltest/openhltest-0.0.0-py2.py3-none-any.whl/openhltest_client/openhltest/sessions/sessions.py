from openhltest_client.base import Base


class Sessions(Base):
	"""A list of test tool sessions.
	Sessions can onl be accessed based on the api-key submitted as part of the request.
	To get an api-key use the authenticate rpc.

	Implements the iterator interface __iter__ and encapsulates 0..n instances of the oht:sessions resource.
	"""
	YANG_NAME = 'sessions'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'name'
	YANG_PROPERTY_MAP = {"Name": "name"}

	def __init__(self, parent):
		super(Sessions, self).__init__(parent)

	@property
	def Config(self):
		"""This container aggregates all other top level configuration submodules.

		Get an instance of the Config class.

		Returns:
			obj(openhltest_client.openhltest.sessions.config.config.Config)
		"""
		from openhltest_client.openhltest.sessions.config.config import Config
		return Config(self)._read()

	@property
	def Statistics(self):
		"""The statistics pull model

		Get an instance of the Statistics class.

		Returns:
			obj(openhltest_client.openhltest.sessions.statistics.statistics.Statistics)
		"""
		from openhltest_client.openhltest.sessions.statistics.statistics import Statistics
		return Statistics(self)._read()

	@property
	def Name(self):
		"""The unique name of the test tool session.
		Once the session has been created the name cannot be modified.

		Returns:
			string

		Raises (setter only):
			ValueError
			InvalidValueError
		"""
		return self._get_value('name')

	def create(self, Name):
		"""Create an instance of the `sessions` resource

		Args:
			Name (string): The unique name of the test tool session.Once the session has been created the name cannot be modified.
		"""
		return self._create(locals())

	def read(self, Name=None):
		"""Get `sessions` resource(s). Returns all resources from the server if `Name` is not specified

		"""
		return self._read(Name)

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `sessions` resource

		"""
		return self._delete()

