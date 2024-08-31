import math

def break_to_characters(text):
    """Remove the spaces, newline and tab characters

    Args:
        text (String): text to be processed

    Returns:
        String : processed string
    """
    char_list = ""
    for char in text:
        if char != " " and char != "\n" and char != "\t":
            char_list += char
    return char_list



def break_to_words(text):
    """Remove the spaces, newline and tab characters

    Args:
        text (String): text to be processed

    Returns:
        String : processed string
    """
    one_line_text = ""
    for char in text:
        if char != "\n" and char != "\t":
            one_line_text += char
    words = one_line_text.split(" ")
    for i in words:
        if i == "":
            words.remove(i)
    return words


def character_error_rate(predicted_text,ground_truth):
    """Calculate the character error rate

    Args:
        predicted_text (String): Predicted text for a image
        ground_truth (String): Ground truth of the image

    Returns:
        Float: Chatacter Error Rate (CER)
    """
        
    predicted_chars = break_to_characters(predicted_text)
    ground_truth_chars = break_to_characters(ground_truth)
    
    min_char_text = predicted_chars if len(predicted_chars) < len(ground_truth_chars) else ground_truth_chars
    max_chars = max(len(predicted_chars), len(ground_truth_chars))
    accurate_instances = 0

    for i in range(0,len(min_char_text)):
        if predicted_chars[i] == ground_truth_chars[i]:
            accurate_instances += 1

    return (max_chars - accurate_instances)/max_chars
    

def charater_difference(predicted_text,ground_truth):
    """return the Number of character difference

    Args:
        predicted_text (String): _description_
        ground_truth (String): _description_

    Returns:
        Int: Number of character difference between the predicted text and ground truth
    """
    predicted_chars = break_to_characters(predicted_text)
    ground_truth_chars = break_to_characters(ground_truth)

    char_difference = len(predicted_chars) - len(ground_truth_chars)

    return char_difference


def word_error_rate(predicted_text,ground_truth):
    """Calculate the word error rate

    Args:
        predicted_text (String): Predicted text for a image
        ground_truth (String): Ground truth of the image

    Returns:
        Float: Chatacter Word Rate (CWR)
    """
        
    predicted_words = break_to_words(predicted_text)
    ground_truth_words = break_to_words(ground_truth)
    
    min_word_text = predicted_words if len(predicted_words) < len(ground_truth_words) else ground_truth_words
    max_words = max(len(predicted_words), len(ground_truth_words))
    accurate_instances = 0

    for i in range(0,len(min_word_text)):
        if predicted_words[i] == ground_truth_words[i]:
            accurate_instances += 1

    return (max_words - accurate_instances)/max_words


def Levenshtein_distance(predicted_text,ground_truth):
    """Return the Levenshtein distance(Edit distance) between the predicted text and ground truth

    Args:
        predicted_text (String): Predicted text for a image
        ground_truth (String): Ground truth of the image

    Returns:
        Int:  Levenshtein distance(Edit distance)
    """
    grid =  [[float("inf")]*(len(ground_truth)+1) for i in range(len(predicted_text)+1)]

    for i in range(len(ground_truth)+1):
        grid[len(predicted_text)][i] = len(ground_truth) - i
    for j in range(len(ground_truth)+1):
        grid[len(predicted_text)][j] = len(ground_truth) - j

    for i in range(len(predicted_text)-1,-1,-1):
        for j in range(len(ground_truth)-1,-1,-1):
            if predicted_text[i] == ground_truth[j]:
                grid[i][j] = grid[i+1][j+1]
            else:
                grid[i][j] = 1 + min(grid[i+1][j],grid[i][j+1],grid[i+1][j+1])
    return grid[0][0]


def avg_Levenshtein_distance(predicted_text,ground_truth):
    """Return the average Levenshtein distance(Edit distance) between the predicted text and ground truth

    Args:
        predicted_text (String): Predicted text for a image
        ground_truth (String): Ground truth of the image

    Returns:
        Float: Average Levenshtein distance(Edit distance)
    """
    ld = Levenshtein_distance(predicted_text,ground_truth)
    return ld/len(ground_truth)

def metrics_report(filename,predicted_text,ground_truth):
    """Summerize all the metrics for a prediction

    Args:
        filename (_type_): _description_
        predicted_text (_type_): _description_
        ground_truth (_type_): _description_

    Returns:
        _type_: _description_
    """
    cer = character_error_rate(predicted_text,ground_truth)
    cdiff = charater_difference(predicted_text,ground_truth)
    wer = word_error_rate(predicted_text,ground_truth)
    ld = Levenshtein_distance(predicted_text,ground_truth)
    ald = avg_Levenshtein_distance(predicted_text,ground_truth)

    print(f"Metric Score Summerization for {filename}\n\tCER : {cer}\n\tCDiff : {cdiff}\n\tWER : {wer}\n\tLD : {ld}\n\tALD : {ald}\n\n")
    return cer,cdiff,wer,ld,ald