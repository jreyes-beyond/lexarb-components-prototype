from abc import ABC, abstractmethod

class Pipeline(ABC):
    @abstractmethod
    async def process(self, *args, **kwargs):
        """Process data through the pipeline"""
        pass