def levenshtein_distance(word1, word2):
    word1 = word1.lower()
    word2 = word2.lower()

    m, n = len(word1), len(word2)

    # Create a 2D table to store distances between prefixes
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: converting empty string to other string
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # no edit needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # deletion
                    dp[i][j - 1],      # insertion
                    dp[i - 1][j - 1]   # substitution
                )

    return dp[m][n]


def find_best_match(ocr_word, medicine_list):
    """
    Given a messy word from OCR, find the closest matching medicine name
    from our database list.
    Returns: (best_match_name, distance, confidence_score)
    """
    best_match = None
    best_distance = float('inf')

    for medicine in medicine_list:
        distance = levenshtein_distance(ocr_word, medicine)
        if distance < best_distance:
            best_distance = distance
            best_match = medicine

    # Convert distance into a 0-1 confidence score
    max_len = max(len(ocr_word), len(best_match))
    confidence = 1 - (best_distance / max_len) if max_len > 0 else 0

    return best_match, best_distance, round(confidence, 2)