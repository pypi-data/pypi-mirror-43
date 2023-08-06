import os

from sacred import Experiment
from sacred.observers import MongoObserver

from urllib.parse import quote_plus

class MyExperiment(Experiment):

	@staticmethod
	def get_creds():
		return dict(
			user=quote_plus(os.environ["MONGODB_USER_NAME"]),
			password=quote_plus(os.environ["MONGODB_PASSWORD"]),
			db_name=quote_plus(os.environ["MONGODB_DB_NAME"]),
		)

	@staticmethod
	def auth_url(creds, host="localhost", port=27017):
		url = "mongodb://{user}:{password}@{host}:{port}/{db_name}?authSource=admin".format(
			host=host, port=port, **creds)
		return url


	def __init__(self, host, no_observer=False, *args, **kwargs):
		super(MyExperiment, self).__init__(*args, **kwargs)

		if no_observer:
			return

		creds = MyExperiment.get_creds()
		self.observers.append(MongoObserver.create(
			url=MyExperiment.auth_url(creds, host=host),
			db_name=creds["db_name"]
			)
		)

	def __call__(self, args):
		self.add_config(**args.__dict__)
		return self._create_run()(args)
