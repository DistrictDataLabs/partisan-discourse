# arbiter.management.commands.train
# Command to train red/blue classifiers from the command line.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Aug 02 10:38:54 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: train.py [] benjamin@bengfort.com $

"""
Command to train red/blue classifiers from the command line.
"""

##########################################################################
## Imports
##########################################################################

import numpy as np

from datetime import datetime
from arbiter.models import Estimator, Score
from django.contrib.auth.models import User
from corpus.reader import TranscriptCorpusReader
from corpus.models import Corpus, Document, LabeledDocument
from corpus.reader import QueryCorpusReader, CorpusModelReader
from corpus.learn import CorpusLoader, build_model
from django.core.management.base import BaseCommand, CommandError

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression


##########################################################################
## Training Command
##########################################################################

class Command(BaseCommand):

    help = "Trains red/blue classifiers and stores them in the database."

    # The types of estimators that this command knows how to train
    estimators = {
        'maxent': (LogisticRegression, {}),
        'svm': (SGDClassifier, {'loss':'hinge', 'penalty':'l2', 'alpha':1e-3}),
        'nbayes': (MultinomialNB, {}),
    }

    # The minimum number of documents to train an estimator
    min_docs = 12

    def add_arguments(self, parser):
        """
        Add command line argparse arguments.
        """
        # Model selection argument
        parser.add_argument(
            '-m', '--model', choices=self.estimators, default='maxent',
            help='specify the model form to fit on the given corpus',
        )

        # Number of folds for cross-validation
        parser.add_argument(
            '-f', '--folds', type=int, default=12,
            help='number of folds to use in cross-validation',
        )

        # Optional ownership argument/build model for user
        parser.add_argument(
            '-u', '--username', default=None, metavar='NAME',
            help='specify a user to build the model for or to assign ownership',
        )

        # Path on disk to build a corpus from transcripts
        parser.add_argument(
            '-t', '--transcripts', default=None, type=str, metavar='PATH',
            help='specify a path on disk to the directory containing transcripts',
        )

        # Specify a corpus id to specifically build for
        parser.add_argument(
            '-c', '--corpus', type=int, default=None, metavar='ID',
            help='specify the id of a corpus to build the model for',
        )

    def handle(self, *args, **options):
        """
        Handles the model training process as follows:

            1. If a transcript path is specified build that and assign to the
               owner if given in the arguments (ignore other args)
            2. If a corpus id is specified, build the model for that corpus and
               assign to the owner if given in the arguments
            3. If just a username is given, construct a user-specific corpus
               and build a model for that corpus
            4. If none of those arguments are given, construct a corpus that
               utilizes the entire state of the current database, and build
               a model for that corpus.

        Note that items 1 and 2 do not create a corpus, whereas 3 and 4 do.
        """

        # Get the owner from the options
        owner  = self.get_user(options['username'])

        # Create the reader from the options
        if options['transcripts']:
            # Get the transcripts reader
            reader = TranscriptCorpusReader(options['transcripts'])
            corpus = None
            description = "transcripts located at {}".format(options['transcripts'])
        else:
            # Get or create the corpus object
            reader, corpus = self.get_corpus(owner=owner, **options)
            if corpus:
                description = str(reader.corpus)
            else:
                description = "Corpus read by {}".format(
                    reader.__class__.__name__
                )

        # Build the model from the corpus and owner.
        estimator = self.build_model(reader, owner, description, **options)

        # If corpus, assign it to the estimator and save
        if corpus:
            estimator.corpus = corpus
            estimator.save()

    def build_model(self, reader, owner, description, **options):
        """
        Once the reader has been
        """
        # Get the details from the command line arguments
        model, kwargs = self.estimators[options['model']]

        # Construct the loader from the passed in reader object.
        loader = CorpusLoader(reader, options['folds'])

        # Inform the user that the training process is beginning
        self.stdout.write((
            "Starting training of {} {} models on {}\n"
            "This may take quite a bit of time, please be patient!\n"
        ).format(
            loader.n_folds + 1, model.__name__, description
        ))

        # GO! Build the model forever! Whooo!!!
        (clf, scores), total_time = build_model(loader, model, **kwargs)

        # Save the estimator model
        estimator = Estimator.objects.create(
            model_type  = Estimator.TYPES.classifier,
            model_class = model.__name__,
            model_form  = repr(clf),
            estimator   = clf,
            build_time  = total_time,
            owner       = owner,
        )

        # Save the scores objects.
        for metric, values in scores.items():

            # Handle the time key in particular.
            if metric == 'times':
                Score.objects.create(
                    metric    = Score.METRICS.time,
                    score     = values['final'].total_seconds(),
                    folds     = [td.total_seconds() for td in values['folds']],
                    estimator = estimator,
                )
                continue

            # Handle generic scores for the model
            for label, folds in values.items():
                if metric == 'support' and label == 'average':
                    # This will be an array of None values, so skip.
                    continue

                Score.objects.create(
                    metric    = metric,
                    score     = np.asarray(folds).mean(),
                    label     = label,
                    folds     = folds,
                    estimator = estimator,
                )


        # Report model construction complete
        self.stdout.write(
            "Training complete in {}! Estimator saved to the database\n".format(total_time)
        )

        return estimator

    def get_user(self, username):
        """
        Returns a user or None, raising a command error if no user with the
        specified username is found in the database.
        """
        if username is None: return None
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(
                "No user with username '{}' in the database".format(username)
            )

    def get_corpus(self, owner=None, **options):
        """
        Uses the supplied options to get or create a corpus from the args
        that have been passed in. Note can raise a CommandError for not enough
        documents in a constructed corpus.

        Returns a corpus model reader object as well as a corpus.
        """

        # If an ID is supplied fetch the corpus from the database.
        if options['corpus']:
            try:
                corpus = Corpus.objects.get(id=options['corpus'])
                reader = CorpusModelReader(corpus)
                return reader, corpus
            except Corpus.DoesNotExist:
                raise CommandError(
                    "No corpus with id {} in the database".format(options['corpus'])
                )

        # If an owner is supplied then create a corpus for that specific user.
        if owner is not None:
            corpus = Corpus.objects.create_for_user(
                owner, title="{} user corpus created on {}".format(
                    owner.username, datetime.now().strftime("%Y-%m-%d")
                )
            )

        # Create a corpus from every document that has annotator agreement!
        else:
            corpus = Corpus.objects.create(
                labeled=True, title="global corpus created on {}".format(
                    datetime.now().strftime("%Y-%m-%d")
                )
            )

            for document in Document.objects.all():
                label = document.label()
                if label is not None:
                    LabeledDocument.objects.create(
                        corpus=corpus, document=document, label=label,
                    )

        # Perform the check for the corpus count.
        if corpus.documents.count() < self.min_docs:
            corpus.delete() # Delete any too small corpora
            raise CommandError(
                "Could not create a corpus with less than {} documents".format(self.min_docs)
            )

        # Otherwise return the corpus
        return CorpusModelReader(corpus), corpus
