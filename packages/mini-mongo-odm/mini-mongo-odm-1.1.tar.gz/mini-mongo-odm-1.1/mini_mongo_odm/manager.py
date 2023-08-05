# encoding=utf8
from bson import ObjectId
from mongoengine import DoesNotExist
from mongoengine.connection import get_db, get_connection
from abc import ABC
from pymongo.results import DeleteResult
from mini_mongo_odm.entity import MongoEntity


class MongoEntityManager(ABC):
	"""
	Базовый класс для работы с сущностями
	"""

	"""
	Здесь можно указать класс сущности, с которой работает менеджер
	В базовых класссах будут доступны методы ORM для сущностей mongoengine
	"""

	_entity = None  # type: MongoEntity

	def get_default_entity(self):
		return self._entity

	def save(self, entity, **kwargs):
		"""
		Создание новой сущности или обновление уже существующей
		Пример:
		tum = TestUserManager()
		data = { "id": "59810932d3aaea1eccd2d642", "title": '__22__', "done": True}
		tu = TestUser(**data)
		tum.save(tu)

		"""
		return entity.save(**kwargs)

	def update(self, condition, update_query):
		"""
		Метод для обновления полей одного или нескольких документов по условию.
		Должен обладать максимальной гибкостью, поэтому предлагаю
		не использовать методы ORM, а напрямую вызывать метод драйвера.

		Пример:
		tum = TestUserManager()
		user = tum.get_by_id("59810932d3aaea1eccd2d642")
		query = {"$set": {"title": 'some value', "done": True}}
		# res= tum.update_by_condition({"_id": ObjectId("59810932d3aaea1eccd2d642")}, query)
		res= tum.update_by_condition({"done": False}, query)

		:param condition:
		:param query:
		:param alias:
		:return: pymongo.results.UpdateResult
		"""

		return self.get_collection().update_many(condition, update_query)

	def update_by_id(self, entity_id, update_query):
		"""
		Метод обновления части сущности по ID c использованием нативного синтаксиса mongo

		cm = ClientManager()
		uid = "5999488e962d7408d859423a"
		cm.update_by_id_native(uid, {"$set": {"metadata.signin_at" : "200"}})

		:param entity_id:
		:param query:
		:param alias:
		:return:
		"""

		cond = {"_id": ObjectId(str(entity_id))}
		return self.update(cond, update_query)

	def get_collection(self):
		"""
		Метод возвращает коллекцию для нативных вызовов
		напр. return self.get_collection().find()
		"""
		return self._entity._get_collection()

	# db = self.get_db(alias=alias)
	# return db[self._default_collection]

	def get_by_id(self, entity_id):
		"""
		Базовый метод для получения сущности по ID

		:param entity_id:
		:param id:
		:return: Document
		"""
		try:
			return self._entity.objects.get(id=entity_id)
		except DoesNotExist:
			return None

	def get(self, condition):
		"""
		Возвращает список сущностей

		:param condition:
		:return:
		"""
		return self._entity.objects(__raw__=condition)

	def get_one(self, condition):
		"""
		Возвращает одну сущность

		Example: res = manager.get_one({"name": "some value"})

		:param condition:
		:return:
		"""
		try:
			return self._entity.objects.get(__raw__=condition)
		except DoesNotExist:
			return None

	def get_fields(self, condition, fields, include_id=False, **kwargs):
		"""
		Возвращает только указанный набор полей
		# projection={'_id': False}

		res = manager.get_fields({"name": "some value"}, ["age", "name"])

		:param include_id:
		:param condition:
		:param fields:
		:return:
		"""

		field_set = {key: True for key in fields}
		field_set["_id"] = include_id

		return self.get_collection().find(filter=condition, projection=field_set, **kwargs)

	def remove(self, condition) -> int:
		"""
		Удаляет объекты по условию. Нативный запрос
		"""

		result = self.get_collection().delete_many(condition)
		return result.deleted_count

	def remove_by_id(self, entity_id) -> DeleteResult:
		""""
		Удаляет объект по ObjectId

		:param id: ObjectId | string
		:return:
		"""

		cond = {"_id": ObjectId(str(entity_id))}
		return self.get_collection().delete_one(cond)

	def get_db(self, alias="default", reconnect=False):
		"""
		Возвращает объект БД для нативных запросов
		:param alias:
		:param reconnect:
		:return:
		"""
		return get_db(alias=alias, reconnect=reconnect)

	def get_connection(self, alias="default", reconnect=False):
		"""
		Возвращает соединение к БД
		:param alias:
		:param reconnect:
		:return:
		"""
		return get_connection(alias=alias, reconnect=reconnect)

	def get_all(self):
		"""
		Возвращает список всех объектов
		:return:
		"""

		out = []
		res = self._entity.objects

		if res.count() == 0:
			return []
		else:
			for obj in res:
				out.append(obj)
			return out
