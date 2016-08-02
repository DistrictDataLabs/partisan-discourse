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

from arbiter.models import Estimator, Score
from django.contrib.auth.models import User
from corpus.reader import TranscriptCorpusReader
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

    estimators = {
        'maxent': (LogisticRegression, {}),
        'svm': (SGDClassifier, {'loss':'hinge', 'penalty':'l2', 'alpha':1e-3}),
        'nbayes': (MultinomialNB, {}),
    }

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

        # Optional ownership argument
        parser.add_argument(
            '-u', '--username', default=None,
            help='specify the username to associate with the model',
        )

        # TODO: Change this to allow for a query or a path on disk
        parser.add_argument('corpus', nargs=1, help='path to the corpus on disk')

    def handle(self, *args, **options):
        """
        Handles the model training process
        """

        # Get the details from the command line arguments
        model, kwargs = self.estimators[options['model']]
        owner  = self.get_user(options['username'])

        # Construct the corpus and loader in preparation for training.
        # TODO: Make the corpus loader construction a method to handle querysets
        corpus = TranscriptCorpusReader(options['corpus'][0])
        loader = CorpusLoader(corpus, options['folds'])

        # Inform the user that the training process is beginning
        self.stdout.write((
            "Starting training of {} {} models on the corpus at {}\n"
            "This may take quite a bit of time, please be patient!\n"
        ).format(
            loader.n_folds + 1, model.__name__, options['corpus'][0]
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
