from abc import ABC, abstractmethod
class WordDifferenceFinder:
    """Identifies words that differ between original and masked text."""
    def __init__(self, comparison_strategy):
        self.comparison_strategy = comparison_strategy

    def find_differing_words(self, original_text, masked_text):
        return self.comparison_strategy.compare(original_text, masked_text)
    
class ComparisonStrategy(ABC):
    """Abstract Strategy for comparing original and masked text."""
    @abstractmethod
    def compare(self, original_text, masked_text):
        pass


class DefaultComparisonStrategy(ComparisonStrategy):
    """Uses set difference to find missing words (case-insensitive)."""
    def compare(self, original_text, masked_text):
        original_words = set(original_text.lower().split())
        masked_words = set(masked_text.lower().split())
        return original_words.difference(masked_words)
        