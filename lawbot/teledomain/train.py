#!/usr/bin/env python
# coding: utf8
"""Example of training an additional entity type

This script shows how to add a new entity type to an existing pretrained NER
model. To keep the example short and simple, only four sentences are provided
as examples. In practice, you'll need many more — a few hundred would be a
good start. You will also likely need to mix in examples of other entity
types, which might be obtained by running the entity recognizer over unlabelled
sentences, and adding their annotations to the training set.

The actual training is performed by looping over the examples, and calling
`nlp.entity.update()`. The `update()` method steps through the words of the
input. At each word, it makes a prediction. It then consults the annotations
provided on the GoldParse instance, to see whether it was right. If it was
wrong, it adjusts its weights so that the correct action will score higher
next time.

After training your model, you can save it to a directory. We recommend
wrapping models as Python packages, for ease of deployment.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.1.0+
Last tested with: v2.1.0
"""
from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


# new entity label
LABEL = "DATE_TIME"

# training data
# Note: If you're using an existing model, make sure to mix in examples of
# other entity types that spaCy correctly recognized before. Otherwise, your
# model might learn the new type, but "forget" what it previously knew.
# https://explosion.ai/blog/pseudo-rehearsal-catastrophic-forgetting

#TRAIN_DATA = [('Job title: Cleaner\xa0', {'entities': [(11, 18, 'JOB_TITLE')]}), ('Job role: cleaner\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Role: cleaner\xa0', {'entities': [(6, 13, 'JOB_TITLE')]}), ('Jobscope: cleaner\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Job scope: cleaner\xa0', {'entities': [(11, 18, 'JOB_TITLE')]}), ('Title: cleaner\xa0', {'entities': [(7, 14, 'JOB_TITLE')]}), ('Employee title: cleaner\xa0', {'entities': [(16, 23, 'JOB_TITLE')]}), ('Applied role: cleaner\xa0', {'entities': [(14, 21, 'JOB_TITLE')]}), ('Role\xa0Cleaner\xa0', {'entities': [(5, 12, 'JOB_TITLE')]}), ('Job title\xa0Cleaner\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Employee’s title\xa0Cleaner\xa0', {'entities': [(17, 24, 'JOB_TITLE')]}), ('PositionCleaner\xa0', {'entities': [(8, 16, 'JOB_TITLE')]}), ('Employee’s position: cleaner\xa0', {'entities': [(21, 28, 'JOB_TITLE')]}), ('Applied position: cleaner\xa0', {'entities': [(18, 25, 'JOB_TITLE')]}), ('Offered position: cleaner\xa0', {'entities': [(18, 26, 'JOB_TITLE')]}), ('New position: cleaner\xa0', {'entities': [(14, 21, 'JOB_TITLE')]}), ('Work title: cleaner\xa0', {'entities': [(12, 19, 'JOB_TITLE')]}), ('The employee will be hired as a cleaner.\xa0', {'entities': [(32, 39, 'JOB_TITLE')]}), ('The employee will be a cleaner for the employer.\xa0', {'entities': [(23, 30, 'JOB_TITLE')]}), ('The applicant will be a cleaner.\xa0', {'entities': [(24, 31, 'JOB_TITLE')]}), ('The employee’s position will be ‘cleaner’.\xa0', {'entities': [(33, 40, 'JOB_TITLE')]}), ('The employee’s role will be as a cleaner.\xa0', {'entities': [(33, 40, 'JOB_TITLE')]}), ('The employee is hired as a cleaner.\xa0', {'entities': [(27, 34, 'JOB_TITLE')]}), ('Hired role: cleaner\xa0', {'entities': [(12, 19, 'JOB_TITLE')]}), ('Offered position: cleaner\xa0', {'entities': [(18, 25, 'JOB_TITLE')]}), ('Offered position - cleaner\xa0', {'entities': [(19, 26, 'JOB_TITLE')]}), ('Employee will serve as a cleaner.\xa0', {'entities': [(25, 32, 'JOB_TITLE')]}), ('As a cleaner, the employee will work.\xa0', {'entities': [(5, 12, 'JOB_TITLE')]}), ('The employee will henceforth be a cleaner.\xa0', {'entities': [(34, 41, 'JOB_TITLE')]}), ('The employee is hired to be a cleaner.\xa0', {'entities': [(30, 37, 'JOB_TITLE')]}), ('Job title: Janitor\xa0', {'entities': [(11, 18, 'JOB_TITLE')]}), ('Job role: janitor\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Role: janitor\xa0', {'entities': [(6, 13, 'JOB_TITLE')]}), ('Jobscope: janitor\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Job scope: janitor\xa0', {'entities': [(11, 18, 'JOB_TITLE')]}), ('Title: janitor\xa0', {'entities': [(7, 14, 'JOB_TITLE')]}), ('Employee title: janitor\xa0', {'entities': [(16, 23, 'JOB_TITLE')]}), ('Applied role: janitor\xa0', {'entities': [(14, 21, 'JOB_TITLE')]}), ('Role\xa0Janitor\xa0', {'entities': [(5, 12, 'JOB_TITLE')]}), ('Job title\xa0Janitor\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Employee’s title\xa0Janitor\xa0', {'entities': [(17, 24, 'JOB_TITLE')]}), ('PositionJanitor\xa0', {'entities': [(8, 16, 'JOB_TITLE')]}), ('Employee’s position: janitor\xa0', {'entities': [(21, 28, 'JOB_TITLE')]}), ('Applied position: janitor\xa0', {'entities': [(18, 25, 'JOB_TITLE')]}), ('Offered position: janitor\xa0', {'entities': [(18, 26, 'JOB_TITLE')]}), ('New position: janitor\xa0', {'entities': [(14, 21, 'JOB_TITLE')]}), ('Work title: janitor\xa0', {'entities': [(12, 19, 'JOB_TITLE')]}), ('The employee will be hired as a janitor.\xa0', {'entities': [(32, 39, 'JOB_TITLE')]}), ('The employee will be a janitor for the employer.\xa0', {'entities': [(23, 30, 'JOB_TITLE')]}), ('The applicant will be a janitor.\xa0', {'entities': [(24, 31, 'JOB_TITLE')]}), ('The employee’s position will be ‘janitor’.\xa0', {'entities': [(33, 40, 'JOB_TITLE')]}), ('The employee’s role will be as a janitor.\xa0', {'entities': [(33, 40, 'JOB_TITLE')]}), ('The employee is hired as a janitor.\xa0', {'entities': [(27, 34, 'JOB_TITLE')]}), ('Hired role: janitor\xa0', {'entities': [(12, 19, 'JOB_TITLE')]}), ('Offered position: janitor\xa0', {'entities': [(18, 25, 'JOB_TITLE')]}), ('Offered position - janitor\xa0', {'entities': [(19, 26, 'JOB_TITLE')]}), ('Employee will serve as a janitor.\xa0', {'entities': [(25, 32, 'JOB_TITLE')]}), ('As a janitor, the employee will work.\xa0', {'entities': [(5, 12, 'JOB_TITLE')]}), ('The employee will henceforth be a janitor.\xa0', {'entities': [(34, 41, 'JOB_TITLE')]}), ('The employee is hired to be a janitor.\xa0', {'entities': [(30, 37, 'JOB_TITLE')]}), ('Job title: Teacher\xa0', {'entities': [(11, 18, 'JOB_TITLE')]}), ('Job role: teacher\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Role: teacher\xa0', {'entities': [(6, 13, 'JOB_TITLE')]}), ('Jobscope: teacher\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Job scope: teacher\xa0', {'entities': [(11, 18, 'JOB_TITLE')]}), ('Title: teacher\xa0', {'entities': [(7, 14, 'JOB_TITLE')]}), ('Employee title: teacher\xa0', {'entities': [(16, 23, 'JOB_TITLE')]}), ('Applied role: teacher\xa0', {'entities': [(14, 21, 'JOB_TITLE')]}), ('Role\xa0Teacher\xa0', {'entities': [(5, 12, 'JOB_TITLE')]}), ('Job title\xa0Teacher\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Employee’s title\xa0Teacher\xa0', {'entities': [(17, 24, 'JOB_TITLE')]}), ('PositionTeacher\xa0', {'entities': [(8, 16, 'JOB_TITLE')]}), ('Employee’s position: teacher\xa0', {'entities': [(21, 28, 'JOB_TITLE')]}), ('Applied position: teacher\xa0', {'entities': [(18, 25, 'JOB_TITLE')]}), ('Offered position: teacher\xa0', {'entities': [(18, 26, 'JOB_TITLE')]}), ('New position: teacher\xa0', {'entities': [(14, 21, 'JOB_TITLE')]}), ('Work title: teacher\xa0', {'entities': [(12, 19, 'JOB_TITLE')]}), ('The employee will be hired as a teacher.\xa0', {'entities': [(32, 39, 'JOB_TITLE')]}), ('The employee will be a teacher for the employer.\xa0', {'entities': [(23, 30, 'JOB_TITLE')]}), ('The applicant will be a teacher.\xa0', {'entities': [(24, 31, 'JOB_TITLE')]}), ('The employee’s position will be ‘teacher’.\xa0', {'entities': [(33, 40, 'JOB_TITLE')]}), ('The employee’s role will be as a teacher.\xa0', {'entities': [(33, 40, 'JOB_TITLE')]}), ('The employee is hired as a teacher.\xa0', {'entities': [(27, 34, 'JOB_TITLE')]}), ('Hired role: teacher\xa0', {'entities': [(12, 19, 'JOB_TITLE')]}), ('Offered position: teacher\xa0', {'entities': [(18, 25, 'JOB_TITLE')]}), ('Offered position - teacher\xa0', {'entities': [(19, 26, 'JOB_TITLE')]}), ('Employee will serve as a teacher.\xa0', {'entities': [(25, 32, 'JOB_TITLE')]}), ('As a teacher, the employee will work.\xa0', {'entities': [(5, 12, 'JOB_TITLE')]}), ('The employee will henceforth be a teacher.\xa0', {'entities': [(34, 41, 'JOB_TITLE')]}), ('The employee is hired to be a teacher.\xa0', {'entities': [(30, 37, 'JOB_TITLE')]}), ('Job title: Plumber\xa0', {'entities': [(11, 18, 'JOB_TITLE')]}), ('Job role: plumber\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Role: plumber\xa0', {'entities': [(6, 13, 'JOB_TITLE')]}), ('Jobscope: plumber\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Job scope: plumber\xa0', {'entities': [(11, 18, 'JOB_TITLE')]}), ('Title: plumber\xa0', {'entities': [(7, 14, 'JOB_TITLE')]}), ('Employee title: plumber\xa0', {'entities': [(16, 23, 'JOB_TITLE')]}), ('Applied role: plumber\xa0', {'entities': [(14, 21, 'JOB_TITLE')]}), ('Role\xa0Plumber\xa0', {'entities': [(5, 12, 'JOB_TITLE')]}), ('Job title\xa0Plumber\xa0', {'entities': [(10, 17, 'JOB_TITLE')]}), ('Employee’s title\xa0Plumber\xa0', {'entities': [(17, 24, 'JOB_TITLE')]}), ('PositionPlumber\xa0', {'entities': [(8, 16, 'JOB_TITLE')]}), ('Employee’s position: plumber\xa0', {'entities': [(21, 28, 'JOB_TITLE')]}), ('Applied position: plumber\xa0', {'entities': [(18, 25, 'JOB_TITLE')]}), ('Offered position: plumber\xa0', {'entities': [(18, 26, 'JOB_TITLE')]}), ('New position: plumber\xa0', {'entities': [(14, 21, 'JOB_TITLE')]}), ('Work title: plumber\xa0', {'entities': [(12, 19, 'JOB_TITLE')]}), ('The employee will be hired as a plumber.\xa0', {'entities': [(32, 39, 'JOB_TITLE')]}), ('The employee will be a plumber for the employer.\xa0', {'entities': [(23, 30, 'JOB_TITLE')]}), ('The applicant will be a plumber.\xa0', {'entities': [(24, 31, 'JOB_TITLE')]}), ('The employee’s position will be ‘plumber’.\xa0', {'entities': [(33, 40, 'JOB_TITLE')]}), ('The employee’s role will be as a plumber.\xa0', {'entities': [(33, 40, 'JOB_TITLE')]}), ('The employee is hired as a plumber.\xa0', {'entities': [(27, 34, 'JOB_TITLE')]}), ('Hired role: plumber\xa0', {'entities': [(12, 19, 'JOB_TITLE')]}), ('Offered position: plumber\xa0', {'entities': [(18, 25, 'JOB_TITLE')]}), ('Offered position - plumber\xa0', {'entities': [(19, 26, 'JOB_TITLE')]}), ('Employee will serve as a plumber.\xa0', {'entities': [(25, 32, 'JOB_TITLE')]}), ('As a plumber, the employee will work.\xa0', {'entities': [(5, 12, 'JOB_TITLE')]}), ('The employee will henceforth be a plumber.\xa0', {'entities': [(34, 41, 'JOB_TITLE')]}), ('The employee is hired to be a plumber.\xa0', {'entities': [(30, 37, 'JOB_TITLE')]})]

TRAIN_DATA = [('date of commencement is 04/05/2019', {'entities': [(24, 34, 'DATE_TIME')]}), ('Employment will commence on the 1st of January, 2020', {'entities': [(32, 52, 'DATE_TIME')]}), ('Termination date is 04-05-1997', {'entities': [(20, 30, 'DATE_TIME')]}), ('Contract was signed on 14th December 2018', {'entities': [(23, 41, 'DATE_TIME')]}), ('Employment will commence from this date : 15th Feb 2010', {'entities': [(42, 55, 'DATE_TIME')]}), ('Employee will start work on the 15th of April, 2013.', {'entities': [
    (32, 52, 'DATE_TIME')]}), ('The contract expires on 05-05-2011.', {'entities': [(24, 34, 'DATE_TIME')]}), ('The contract was signed on 14/12/2016.', {'entities': [(27, 37, 'DATE_TIME')]}), ('DATE OF COMMENCEMENT : 12/09/2009', {'entities': [(23, 33, 'DATE_TIME')]}), ('DATE OF TERMINATION : 8th March 2008', {'entities': [(22, 36, 'DATE_TIME')]}), ('Employment will cease on the 9th of October, 2024', {'entities': [(29, 49, 'DATE_TIME')]}), ('Employment ceases on 11-11-2001', {'entities': [(21, 31, 'DATE_TIME')]})]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model="DATE_TIME", new_model_name="DATE_TIME", output_dir="./DATE_TIME", n_iter=30):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    random.seed(0)
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe("ner")

    ner.add_label(LABEL)  # add new entity label to entity recognizer
    # Adding extraneous labels shouldn't mess anything up
    ner.add_label("VEGETABLE")
    if model is None:
        optimizer = nlp.begin_training()
    else:
        optimizer = nlp.resume_training()
    move_names = list(ner.move_names)
    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [
        pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        sizes = compounding(1.0, 4.0, 1.001)
        # batch up the examples using spaCy's minibatch
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            batches = minibatch(TRAIN_DATA, size=sizes)
            losses = {}
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer,
                           drop=0.35, losses=losses)
            print("Losses", losses)

    # test the trained model
    test_text = "Date of termination : 17/09/2019"
    doc = nlp(test_text)
    print("Entities in '%s'" % test_text)
    for ent in doc.ents:
        print(ent.label_, ent.text)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta["name"] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        # Check the classes have loaded back consistently
        assert nlp2.get_pipe("ner").move_names == move_names
        doc2 = nlp2(test_text)
        for ent in doc2.ents:
            print(ent.label_, ent.text)


if __name__ == "__main__":
    plac.call(main)
