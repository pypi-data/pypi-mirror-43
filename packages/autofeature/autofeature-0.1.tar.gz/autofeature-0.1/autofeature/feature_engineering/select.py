class Select():
	def __init__(self, on_entity, on_properties):
		self._on_entity = on_entity
		self._on_properties = on_properties

	def exec(self):
		table = self._on_entity.table[self._on_properties]
		return table

	@property
	def on_properties(self):
		return self._on_properties

	@property
	def on_entity(self):
		return self._on_entity
