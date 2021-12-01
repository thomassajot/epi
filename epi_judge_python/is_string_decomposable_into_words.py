import functools
from typing import List, Set

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def decompose_into_dictionary_words_perso(domain: str,
                                    dictionary: Set[str]) -> List[str]:
    if len(dictionary) == 0:
        return []
    max_len = max(len(domain), max(len(x) for x in dictionary))

    @functools.lru_cache(None)
    def prefix_decomposition(i: int) -> list:
        words = list()
        for j in range(i + 1, min(max_len, len(domain)) + 1):
            value = domain[i:j]
            if value in dictionary:  # O(1)
                if j < len(domain):
                    decomposition = prefix_decomposition(j)
                    if len(decomposition) != 0:
                        words.append(value)
                        words.extend(decomposition)
                        return words
                else:
                    words.append(value)
        return words
    return list(prefix_decomposition(0))



def decompose_into_dictionary_words(domain: str,
                                    dictionary: Set[str]) -> List[str]:
    last_length = [-1] * len(domain)
    for i in range(len(domain)):
        if domain[:i+1] in dictionary:
            last_length[i] = i + 1
            continue

        for j in range(i):
            if last_length[j] != -1 and domain[j + 1: i+1] in dictionary:
                last_length[i] = i - j
                break

    decomposition = []
    if last_length[-1] != -1:
        idx = len(domain) - 1
        while idx >= 0:
            decomposition.append(domain[idx + 1 - last_length[idx]:idx + 1])
            idx -= last_length[idx]
        decomposition = decomposition[::-1]
    return decomposition

# res = decompose_into_dictionary_words('ahellomana', {'hello', 'hell', 'man', 'a', 'mana'})
# print(res)

@enable_executor_hook
def decompose_into_dictionary_words_wrapper(executor, domain, dictionary,
                                            decomposable):
    result = executor.run(
        functools.partial(decompose_into_dictionary_words, domain, dictionary))

    if not decomposable:
        if result:
            raise TestFailure('domain is not decomposable')
        return

    if any(s not in dictionary for s in result):
        raise TestFailure('Result uses words not in dictionary')

    if ''.join(result) != domain:
        raise TestFailure('Result is not composed into domain')


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main(
            'is_string_decomposable_into_words.py',
            'is_string_decomposable_into_words.tsv',
            decompose_into_dictionary_words_wrapper))
