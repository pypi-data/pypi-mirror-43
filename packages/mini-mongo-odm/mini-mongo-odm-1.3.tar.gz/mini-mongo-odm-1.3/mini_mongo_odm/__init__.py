# encoding=utf8
from collections import Iterable
from datetime import datetime

from bson import ObjectId


def make_json_encoder(superclass):
	class MongoEngineJSONEncoder(superclass):
		"""
		A JSONEncoder which provides serialization of MongoEngine
		documents and queryset objects.
		"""

		def default(self, obj):
			if isinstance(obj, Iterable):
				out = {}
				for key in obj:
					out[key] = getattr(obj, key)
				return out

			if isinstance(obj, ObjectId):
				return str(obj)

			if isinstance(obj, datetime):
				return str(obj)

			return superclass.default(self, obj)

	return MongoEngineJSONEncoder
