class FeatureBase():
    def __init__(self, name):
        self._name = name
        self._on_properties = None
        self._on_entity = None
        self._return_name = None
        self._optionals = {}

    def verify(self):
        pass

    def exec(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def on_properties(self):
        return self._on_properties

    @property
    def on_entity(self):
        return self._on_entity

    @property
    def return_name(self):
        return self._return_name

    @property
    def optionals(self):
        return self._optionals

