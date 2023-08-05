# -*- coding: utf-8 -*-
from bson import ObjectId
from flask_mongoengine import Document

__author__ = 'afi'


class MongoEntity(Document):

	meta = {
		'abstract': True
	}

	@property
	def entity_id(self) -> ObjectId:
		"""
		ID сущностии
		:return: type: ObjectId
		"""
		# self._qs
		return self.id

	def set_entity_id(self, val):
		self.id = val

	@property
	def entity_id_str(self):
		"""
		Строковое представление ID сущности
		:return:
		"""
		return str(self.id)

