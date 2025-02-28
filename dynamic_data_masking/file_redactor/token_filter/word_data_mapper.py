from collections import defaultdict

class WordDataMapper:
    """Maps words to their corresponding OCR coordinates."""
    def __init__(self, words_info):
        # Remove empty text entries
        filtered_words_info = [word for word in words_info if word['text'].strip()]
        self.word_data_map = self._build_word_data_map(filtered_words_info)

    def _build_word_data_map(self, words_info):
        word_data_map = defaultdict(list)
        for word_data in words_info:
            word_data_map[word_data['text'].lower()].append(word_data)
        return word_data_map

    def get_word_coordinates(self, differing_words):
        differing_words_data = [
            data for word in differing_words for data in self.word_data_map.get(word, [])
        ]
        return differing_words_data