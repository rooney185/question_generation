import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag


# Helper function to create WH-questions from a sentence
def create_wh_question(sentence):
    words = word_tokenize(sentence)
    tagged = pos_tag(words)

    if not words:
        return None

    # Simple rules to frame questions
    if words[0].lower() in ["the", "a", "an"]:
        question = "Define " + sentence[0].lower() + sentence[1:] + "?"
    elif any(tag.startswith('VB') for word, tag in tagged):
        question = "what is " + sentence
    elif any(word.lower() in ["when", "where", "why", "how"] for word in words):
        question = sentence
    else:
        question = "Explain " + sentence[0].lower() + sentence[1:] + "?"

    return question

# Main function to generate subjective questions
def generate_subjective_questions(text, num_2marks, num_5marks, num_10marks):
    sentences = sent_tokenize(text)
    sentences = [s.strip() for s in sentences if s.strip()]

    questions_with_marks = []
    idx = 0

    # Prepare a list of generated questions
    all_questions = []
    for sent in sentences:
        q = create_wh_question(sent)
        if q:
            all_questions.append(q)

    # Assign questions to marks
    for _ in range(num_2marks):
        if idx < len(all_questions):
            questions_with_marks.append({"question": all_questions[idx], "marks": 2})
            idx += 1

    for _ in range(num_5marks):
        if idx < len(all_questions):
            questions_with_marks.append({"question": all_questions[idx], "marks": 5})
            idx += 1

    for _ in range(num_10marks):
        if idx < len(all_questions):
            questions_with_marks.append({"question": all_questions[idx], "marks": 10})
            idx += 1

    return questions_with_marks

