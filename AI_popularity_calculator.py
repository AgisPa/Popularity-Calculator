import time
from openai import OpenAI
import Google_Search
import numpy as np
import pandas as pd

#Set term of interest.
query="Bitcoin cryptocurrency"

#Connect with your OpenAI API by inpitting your API key below.
api_key="OPENAI_API_KEY"

#Initialization Class.
class get_popularity():
    def __int__(self,query):
        #The trust equates to the percentage of the AI guidelines feeded into OpenAI to get the evaluation.
        trust=0.8
        #Setting starting time frame row for the analysis.
        start_pos=0
        #Number of terms for each evaluation.
        num_of_terms=4
        #Time increment is set according to time frame data. In this example daily searches have been separated into 10 day periods.
        increment = 10
        get_popularity(query=query,accuracy=num_of_terms,increment=increment,trust=trust,start_pos=start_pos)

#Execution.
get_popularity(query)

#AI Guidelines
evaluation_criteria = {
    "Relevance": "Does the title directly relate to the specified item of interest?",
    "Clarity": "Is the title clear and easy to understand without ambiguity?",
    "Accuracy": "Does the title accurately represent the content of the page?",
    "Objectivity": "Is the title neutral and unbiased, or does it seem to have a subjective or promotional tone?",
    "Descriptiveness": "Does the title provide enough information to give a clear idea of what the page is about?",
    "Use of Keywords": "Are relevant keywords present in the title that align with the item of interest?",
    "Context": "Does the title consider the broader context of the item and its value?",
    "Authenticity": "Can the information in the title be trusted, and is the source reliable?",
    "Currency": "Is the information in the title up-to-date, or does it risk being outdated?",
    "Conciseness": "Is the title succinct, or does it contain unnecessary information?",
    "Engagement": "Does the title encourage the reader to explore the content further?",
    "Audience Consideration": "Is the title tailored to the intended audience's interests and needs?",
    "Credibility": "Does the title convey a sense of authority or expertise on the subject?",
    "Uniqueness": "Is the title distinctive, or does it resemble other titles on the same topic?",
    "Tone": "Does the title strike an appropriate tone for the subject matter and audience?",
    "Positive/Negative Bias": "Is there any evident bias in the title, either positive or negative?",
    "Sensationalism": "Does the title use sensational language to grab attention, possibly at the expense of accuracy?",
    "Ethical Considerations": "Does the title adhere to ethical standards in its presentation of information?",
    "Accessibility": "Can the title be easily understood by a diverse audience, considering different levels of expertise?",
    "Completeness": "Does the title provide a comprehensive view of the item's value, or does it oversimplify the topic?"
}

client = OpenAI(
    api_key=api_key,
)


def ai_check_to_list(query, acc, srch_range):
    reply = rel_fact(query, acc, srch_range)
    check = False
    while not check:
        if reply.count(",") != srch_range:
            check = True
            return reply.split(",")
        else:
            reply = rel_fact(query, acc, srch_range)


def pick_rand_from_dict(acc):
    eval = ""
    for i in range(acc):
        rand = np.random.choice(range(len(evaluation_criteria)), acc, replace=False)
        dict_to_list = list(evaluation_criteria.items())
        for j in range(len(rand)):
            eval = eval + " \n" + str(dict_to_list[rand[j]]) + "\n"
    return eval


def rel_fact(a_thing, acc, srch_range):
    txt = "Write only " + str(srch_range) + " words separated by commas with a maximum of " + str(
        acc) + " characters. These words are the top one word factors contributing to a " + str(
        a_thing) + "'s value today in finance. "
    return ask_ai(txt, acc)


def ask_ai(query, acc):
    time.sleep(1)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        max_tokens=acc,
        model="gpt-3.5-turbo",
    )
    ai_reply = response.choices[0].message.content
    return ai_reply.replace(".", " ")


def relevant_factors(query, search_range):
    acc = int(3.5 * search_range)
    reply = ai_check_to_list(query, acc, search_range)
    return reply


def ai_evaluate(query, title, acc, trust):
    txt = "You can only reply with a number." \
          "Read the title of this page about " + str(query) + " and " + str(title) + \
          "Rate the title on whether it insinuates negative of positive growth for " + str(
        query) + " by giving it a score from -100 to 100 based on the following criterea:" \
          + pick_rand_from_dict(int(len(evaluation_criteria) * trust)) + \
          "Reply only with the score."
    return ask_ai(txt, acc)


def ai_evaluate_and_check(query, title, acc, trust):
    reply = ai_evaluate(query, title, acc, trust)
    try:
        reply = int(reply)
    except:
        reply = ai_evaluate(query, title, acc, trust)

    return reply


def ai_popularity_indexes(query, accuracy, trust, save, start_date, end_date):
    acc = accuracy
    results = []
    par = True
    while par:
        a = 0

        factors = relevant_factors(query, acc)
        for o in range(len(factors)):
            if factors.count(" ") != 0:
                a = 1
        if a == 1:
            par = True
        else:
            par = False

    for factor in factors:
        results.append(Google_Search.get_google_titles(str(factor) + " news about " + str(query), start_date, end_date))
    evaluations = []
    avrg_eval = []
    for elements, fac in zip(results, factors):
        titles = elements
        eval = []
        for i in titles:
            eval.append(int(ai_evaluate_and_check(query, i, acc, trust)))
        evaluations.append(eval)
        avrg_eval.append(np.average(eval))
    data = {}

    for j in range(len(factors)):
        eval_pack = evaluations[j]
        row = results[j]
        data[str(factors[j])] = row
        data[str(factors[j]) + "(-100,100): " + str(avrg_eval[j])] = eval_pack

    if save:
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.transpose()
        outname =  str(start_date.replace("/", "-")) + ".csv"
        print(outname,"has been created")
        df.to_csv(f"{outname}", index=False)


def get_popularity(query, accuracy, increment, trust, start_pos):
    data = pd.read_csv("TimeFrame.csv")
    dates = np.array(data["Date"])
    dates = [str(dates[i].split("-")[2]) + "/" + str(dates[i].split("-")[1]) + "/" + str(dates[i].split("-")[0]) for i
             in range(start_pos, len(dates))]
    for i in range(len(dates)):
        if i % increment == 0 and increment + i < len(dates):
            ai_popularity_indexes(query=query, accuracy=accuracy, trust=trust, save=True, start_date=dates[i],
                                  end_date=dates[i + increment])













