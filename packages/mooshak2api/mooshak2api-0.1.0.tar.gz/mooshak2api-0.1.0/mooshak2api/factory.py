class GenericObject:

    def __init__(self):
        self.property_names = {"type", "id"}
        self.reserved_propertys = {"type"}
        super(GenericObject, self).__init__()

    @property
    def type(self):
        return self.__class__.__name__.lower()

    def update(self, connection):
        raise NotImplemented

    def delete(self, connection):
        raise NotImplemented

    def create(self, connection):
        raise NotImplemented

    def load_from_dict(self, json: dict) -> object:
        """
        Reads data from a JSON Object/Dict, and sets the attributes of this object with each corresponding key
        """
        for key in json.keys():
            self.property_names.add(key)
            if key not in self.reserved_propertys:
                setattr(self, key, json[key])

        return self

    def as_json(self) -> dict:
        """
        Returns the JSON representation of the object, based on the keys set in self.property_names
        :return:
        """
        json = {}
        for key in self.property_names:
            json.update({key: getattr(self, key)})

        return json


