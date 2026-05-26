"""
Lab 4, Task 2, Variant 24
Text processing class and analysis execution.
Developer: Finsky Pavel
Date: 30.04.2026
Version: 1.0
"""
import re
import zipfile
import os
from .regex_patterns import (find_lowercase_words_and_punctuation, is_valid_mac,
                              count_sentences, count_sentence_types,
                              average_sentence_length, average_word_length,
                              count_smileys)

class TextAnalyzer:
    """A class to perform text analysis as required."""
    def __init__(self, text: str):
        self.text = text
        self._words = re.findall(r'\b\w+\b', text)

    @property
    def words(self):
        return self._words

    def individual_task(self):
        """Performs the variant-specific tasks."""
        print("--- Индивидуальные задания ---")
        # 1. Words starting with lowercase and punctuation
        print("1. Слова с маленькой буквы и знаки препинания:")
        matches = find_lowercase_words_and_punctuation(self.text)
        print(f"   {matches}")

        # 2. Check MAC address
        test_mac = "aE:dC:cA:56:76:54"
        print(f"2. Проверка MAC-адреса '{test_mac}': {is_valid_mac(test_mac)}")
        test_mac_invalid = "01:23:45:67:89:Az"
        print(f"   Проверка MAC-адреса '{test_mac_invalid}': {is_valid_mac(test_mac_invalid)}")

        # 3. Count words starting with a consonant
        consonant_words = [w for w in self.words if w[0].lower() in 'bcdfghjklmnpqrstvwxyz']
        print(f"3. Число слов, начинающихся с согласной: {len(consonant_words)}")

        # 4. Find words with double letters and their indices
        double_letter_words = []
        for i, w in enumerate(self.words, 1):
            if re.search(r'(.)\1', w):
                double_letter_words.append((i, w))
        print(f"4. Слова с двумя одинаковыми буквами подряд и их номера: {double_letter_words}")

        # 5. Sort words alphabetically
        sorted_words = sorted(self.words, key=str.lower)
        print(f"5. Слова в алфавитном порядке: {sorted_words}")

    def general_analysis(self):
        """Performs the general analysis tasks and saves to file."""
        print("\n--- Общий анализ ---")
        results = []
        sent_count = count_sentences(self.text)
        results.append(f"Количество предложений: {sent_count}")

        sent_types = count_sentence_types(self.text)
        results.append(f"Повествовательные: {sent_types['declarative']}, "
                       f"Вопросительные: {sent_types['interrogative']}, "
                       f"Побудительные: {sent_types['exclamatory']}")

        avg_sent_len = average_sentence_length(self.text)
        results.append(f"Средняя длина предложения (в словах): {avg_sent_len:.2f}")

        avg_word_len = average_word_length(self.text)
        results.append(f"Средняя длина слова (в символах): {avg_word_len:.2f}")

        smiley_count = count_smileys(self.text)
        results.append(f"Количество смайликов: {smiley_count}")

        for line in results:
            print(line)

        # Save to file
        output_file = "analysis_results.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(results))
        print(f"Результаты сохранены в {output_file}")

        # Archive the file
        zip_filename = "analysis_results.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zf:
            zf.write(output_file)
        print(f"Файл заархивирован как {zip_filename}")

        # Print archive info
        with zipfile.ZipFile(zip_filename, 'r') as zf:
            print(f"Информация об архиве: {zf.namelist()}")

        # Clean up txt file
        os.remove(output_file)

    def run_all(self):
        self.individual_task()
        self.general_analysis()