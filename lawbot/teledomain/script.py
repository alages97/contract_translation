from mindmeld.components.nlp import NaturalLanguageProcessor
import spacy
import os.path
spacyNlp = spacy.load("en_core_web_sm")
jobTitleNlp = spacy.load("JOB_TITLE")
dateTimeNlp = spacy.load("DATE_TIME")

input_text = input("Enter text to process:\n")
path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
nlp = NaturalLanguageProcessor(app_path=path)
nlp.build(incremental=True)
sentences = input_text.split(".")

reply = "\nThe contract has been summarized into the key details, as seen below \n\n"
personCounter = 0

for s in sentences:
    if s is not "":
        processedWord = nlp.process(s)
        intent = processedWord.get('intent')
        domain = processedWord.get('domain')
        print("Intent is : " + intent)
        print("Domain is : " + domain)

        # handle salary case
        result_salary = ''
        if intent == 'get_salary':
            for c in s:
                if c.isdigit():
                    result_salary += c
            reply += "The SALARY of the employee is " + result_salary + "/month\n"

        doc = spacyNlp(s)
        jobDoc = jobTitleNlp(s)
        dateDoc = dateTimeNlp(s)

        for ent in doc.ents:
            if ent.label_ == 'PERSON' and intent == 'employment_details':
                reply += "The EMPLOYEE in the contract is : " + ent.text + "\n"
            elif ent.label_ == 'PERSON' and intent == 'employed_by':
                reply += "The EMPLOYER in the contract is : " + ent.text + "\n"
            elif ent.label_ == 'ORG':
                reply += "The COMPANY that the employee will report to is : " + ent.text + "\n"
            elif ent.label_ == 'GPE':
                reply += "APPLICABLE LAW : " + ent.text + "\n"

        for ent in jobDoc.ents:
            if intent == 'job_details':
                reply += "The JOB TITLE of the employee is : " + ent.text + "\n"
            #print(ent.text, ent.start_char, ent.end_char, ent.label_)

        for ent in dateDoc.ents:
            if intent == 'contract_date':
                reply += "The contract was signed on : " + ent.text + "\n"
            elif intent == 'effective_date':
                reply += "The STARTING date of employment is : " + ent.text + "\n"
            elif intent == 'last_date':
                reply += "The TERMINATION date of employment is : " + ent.text + "\n"


print(reply)
