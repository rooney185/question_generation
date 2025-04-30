import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag

# Helper function to create WH-questions from a sentence
def create_wh_question(sentence):
    words = word_tokenize(sentence)
    tagged = pos_tag(words)

    if not words:
        return None

    if words[0].lower() in ["the", "a", "an"]:
        question = "What " + sentence[0].lower() + sentence[1:] + "?"
    elif any(tag.startswith('VB') for word, tag in tagged):
        question = "Explain: " + sentence
    elif any(word.lower() in ["when", "where", "why", "how"] for word in words):
        question = sentence
    else:
        question = "What is " + sentence[0].lower() + sentence[1:] + "?"

    return question

# Updated helper function to generate distinct fake options
def generate_fake_options(correct_answer):
    words = word_tokenize(correct_answer)
    important_words = [word for word, pos in pos_tag(words) if pos.startswith('NN') or pos.startswith('VB')]

    fake_options = set()
    tries = 0

    while len(fake_options) < 3 and tries < 10:
        tries += 1
        if important_words:
            fake_word = random.choice(important_words)
            modified = correct_answer.replace(fake_word, fake_word + random.choice(['ly', 'ing', 'ness', 'ment']))
        else:
            modified = correct_answer + random.choice([' today', ' quickly', ' sometimes', ' forever'])

        if modified != correct_answer:
            fake_options.add(modified)

    while len(fake_options) < 3:
        fake_options.add(correct_answer + random.choice([' again', ' at once', ' once more']))

    return list(fake_options)

# Main function to generate objective questions
def generate_objective_questions(text, num_questions):
    sentences = sent_tokenize(text)
    sentences = [s.strip() for s in sentences if s.strip()]

    questions_with_marks = []
    idx = 0

    all_questions = []
    for sent in sentences:
        question_text = create_wh_question(sent)
        if not question_text:
            continue

        correct_answer = sent
        options = generate_fake_options(correct_answer)
        options.append(correct_answer)
        random.shuffle(options)

        all_questions.append({
            "question": question_text,
            "options": options,
            "answer": correct_answer
        })

    for _ in range(num_questions):
        if idx < len(all_questions):
            q = all_questions[idx]
            q['marks'] = 1
            questions_with_marks.append(q)
            idx += 1

    return questions_with_marks
