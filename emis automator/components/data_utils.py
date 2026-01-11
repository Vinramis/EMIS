from typing import Union


def numbers_in_string(string: str) -> list[int]:
    numbers_found = []
    number_buffer = ""
    for char in string:
        if char.isdigit():
            number_buffer += char
        else:
            if number_buffer:
                numbers_found.append(int(number_buffer))
                number_buffer = ""
    return numbers_found


def compare_two_trigrams(
    trigram1: str,
    trigram2: str,
    case_sensitive: bool = False,
    developer_mode: bool = False,
) -> Union[bool, int]:
    """
    Compares two trigrams, returns True if they are equal, False otherwise.
    Returns number of matching characters if developer_mode is True.
    """
    result: Union[bool, int] = 0

    if not case_sensitive:
        trigram1 = trigram1.lower()
        trigram2 = trigram2.lower()

    for i in range(min(len(trigram1), len(trigram2))):
        result += 1 if trigram1[i] == trigram2[i] else 0

    if not developer_mode:
        result = result == max(len(trigram1), len(trigram2))

    return result


def compare_trigrams(
    trigrams1: list[str],
    trigrams2: list[str],
    case_sensitive: bool = False,
    developer_mode: bool = False,
) -> list[list[Union[bool, int]]]:
    result: list[list[Union[bool, int]]] = []

    for i, j in zip(range(len(trigrams1)), range(len(trigrams2))):
        result.append(
            compare_two_trigrams(
                trigrams1[i],
                trigrams2[j],
                case_sensitive=case_sensitive,
                developer_mode=developer_mode,
            )
        )

    if not developer_mode:
        result = all(result)

    return result


def compare_two_words(
    word1: str,
    word2: str,
    case_sensitive: bool = False,
    developer_mode: bool = False,
    threshold: float = 0.8,
) -> Union[float, tuple[int, int]]:
    """
    Compares two words, returns similarity ratio.
    Returns tuple of (number of matching trigrams, total number of trigrams) if developer_mode is True.
    """
    matching_trigrams: int = 0
    total_trigrams: int = 0

    if len(word1) == len(word2):
        word1_trigrams: list[str] = [word1[i : i + 3] for i in range(len(word1) - 2)]
        word2_trigrams: list[str] = [word2[i : i + 3] for i in range(len(word2) - 2)]

        for i in range(len(word1_trigrams)):
            if compare_two_trigrams(
                word1_trigrams[i], word2_trigrams[i], case_sensitive=case_sensitive
            ):
                matching_trigrams += 1
            total_trigrams += 1
    else:
        bigger_one = word1 if len(word1) > len(word2) else word2
        smaller_one = word1 if len(word1) < len(word2) else word2
        spaced_smaller_ones = []
        weak_threshold = threshold * (1 - 1 / len(smaller_one))

        difference = len(bigger_one) - len(smaller_one)
        if difference / len(smaller_one) > 0.2:
            return False
        results = []

        for i in range(difference):
            spaced_smaller_ones.append(smaller_one[:i] + " " + smaller_one[i:])

        for i in range(len(spaced_smaller_ones)):
            results.append(
                compare_two_words(
                    spaced_smaller_ones[i],
                    bigger_one,
                    case_sensitive=case_sensitive,
                    threshold=weak_threshold,
                    developer_mode=True,
                )
            )
        found_matching_trigrams = [i[0] for i in results]
        found_total_trigrams = [i[1] for i in results]

        matching_trigrams = max(found_matching_trigrams)
        total_trigrams = max(found_total_trigrams)

    if developer_mode:
        return matching_trigrams, total_trigrams
    return matching_trigrams / total_trigrams


def compare_words(
    words1: list[str],
    words2: list[str],
    case_sensitive: bool = False,
    developer_mode: bool = False,
    threshold: float = 1,
) -> Union[float, list[list[float]]]:
    pass


def compare_two_sentences(
    sentence1: str,
    sentence2: str,
    case_sensitive: bool = False,
    developer_mode: bool = False,
) -> Union[float, tuple[int, int]]:
    """
    Compares two texts, returns similarity ratio.
    Returns tuple of (number of matching words, total number of words) if developer_mode is True.
    """
    pass


def compare_sentences(
    sentences1: list[str],
    sentences2: list[str],
    case_sensitive: bool = False,
    developer_mode: bool = False,
) -> Union[float, list[list[float]]]:
    pass


def cut_string(string: str, *, to_length: int = 20, ellipsis: str = "...") -> str:
    if len(string) > to_length:
        return string[:to_length - len(ellipsis)] + ellipsis
    return string
