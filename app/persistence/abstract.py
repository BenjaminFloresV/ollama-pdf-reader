from abc import ABC, abstractmethod

class AbstractPersistenceClient(ABC):

    @abstractmethod
    async def get_causa_by_id(self, causa_id: str):
        pass


    @abstractmethod
    async def update_causa_detail(self, causa: dict):
        pass
    
    @abstractmethod
    async def save_execution_time(self, main_task_id: str, end_time: float, start_time: float, verbose: bool = False):
        pass