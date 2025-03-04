from abc import ABC, abstractmethod
class WordDifferenceFinder:
    def __init__(self, comparison_strategy):
        self.comparison_strategy = comparison_strategy

    def find_differing_words(self, original_text, masked_text):
        return self.comparison_strategy.compare(original_text, masked_text)
    
class ComparisonStrategy(ABC):
    @abstractmethod
    def compare(self, original_text, masked_text):
        pass


class DefaultComparisonStrategy(ComparisonStrategy):
    def compare(self, original_text, masked_text):
        original_words = set(original_text.lower().split())
        masked_words = set(masked_text.lower().split())
        return original_words.difference(masked_words)
        