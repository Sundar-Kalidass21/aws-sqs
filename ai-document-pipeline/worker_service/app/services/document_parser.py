import time
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def process(self, file_path: str) -> dict:
        """
        Simulate AI processing.
        """
        logger.info(f"Starting processing for {file_path}")
        time.sleep(5) # Simulate latency
        
        # Mock extraction result
        return {
            "summary": "This is a processed document.",
            "entities": ["Entity1", "Entity2"],
            "confidence": 0.98
        }

processor = DocumentProcessor()
