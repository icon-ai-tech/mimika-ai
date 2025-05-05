from abc import ABC, abstractmethod
from typing import Any

class BaseModel(ABC):
    @abstractmethod
    def load(self, model_path: str) -> None:
        """Load model weights from file."""
        pass

    @abstractmethod
    def predict(self, input_data: Any) -> Any:
        """Run inference."""
        pass
