from abc import abstractmethod, ABC


class BaseService(ABC):

    @abstractmethod
    def extract_ruts_from_pdf(*args, **kwargs):
        pass