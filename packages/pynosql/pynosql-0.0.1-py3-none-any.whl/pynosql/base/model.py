from pynosql.base.base_model import BaseModel
from pynosql.common.model_helper import ModelHelper


class Model(BaseModel):
    """ Model """

    BASE = {}

    def __init__(self, base_model=BASE):
        self.mh = ModelHelper(base_model)

    @property
    def model(self):
        """ Return Model

        :return: obj model
        """
        return self.mh.model

    def reset(self):
        """ Reset Model

        :return: None
        """
        self.mh.reset()

    def load(self, values):
        """ Load Model Values

        :param values: obj values
        :return: obj model
        """
        return self.mh.load(values)
