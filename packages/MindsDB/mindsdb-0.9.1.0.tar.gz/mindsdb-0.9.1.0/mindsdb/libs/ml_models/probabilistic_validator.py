from sklearn.naive_bayes import GaussianNB, ComplementNB, MultinomialNB


from mindsdb.libs.constants.mindsdb import *
from mindsdb.libs.data_types.probability_evaluation import ProbabilityEvaluation
import numpy as np
import pickle



class ProbabilisticValidator():
    """
    # The probabilistic validator is a quick to train model used for validating the predictions
    of our main model
    # It is fit to the results our model gets on the validation set
    """
    _smoothing_factor = 0.5 # TODO: Autodetermine smotthing factor depending on the info we know about the dataset
    _value_bucket_probabilities = {}
    _probabilistic_model = None
    X_buff = None
    Y_buff = None


    def __init__(self, buckets, data_type=None):
        """
        Chose the algorithm to use for the rest of the model
        As of right now we go with ComplementNB
        """
        # <--- Pick one of the 3
        self._probabilistic_model = ComplementNB(alpha=self._smoothing_factor)
        #, class_prior=[0.5,0.5]
        #self._probabilistic_model = GaussianNB(var_smoothing=1)
        #self._probabilistic_model = MultinomialNB(alpha=self._smoothing_factor)
        self.X_buff = []
        self.Y_buff = []

        self.buckets = buckets
        if self.buckets is not None:
            self.bucket_keys = [i for i in range(len(self.buckets))]

        self.data_type = data_type

    def pickle(self):
        """
        Returns a version of self that can be serialized into mongodb or tinydb

        :return: The data of a ProbabilisticValidator serialized via pickle and decoded as a latin1 string
        """

        return pickle.dumps(self).decode(encoding='latin1')

    @staticmethod
    def unpickle(pickle_string):
        """
        :param pickle_string: A latin1 encoded python str containing the pickle data
        :return: Returns a ProbabilisticValidator object generated from the pickle string
        """
        return pickle.loads(pickle_string.encode(encoding='latin1'))

    @staticmethod
    def _closest(arr, value):
        """
        :return: The index of the member of `arr` which is closest to `value`
        """

        for i,ele in enumerate(arr):
            if ele > value:
                return i - 1

        return len(arr)-1

    # For contignous values we want to use a bucket in the histogram to get a discrete label
    def _get_value_bucket(self, value):
        """
        :return: The bucket in the `histogram` in which our `value` falls
        """
        if type(value) == type(''):
            if value in self.buckets:
                i = self.buckets.index(value)
            else:
                i = 1 # todo make sure that there is an index for values not in list
        else:
            i = self._closest(self.buckets, value)
        return i


    def register_observation(self, features_existence, real_value, predicted_value):
        """
        # Register an observation in the validator's internal buffers

        :param features_existence: A vector of 0 and 1 representing the existence of all the features (0 == not exists, 1 == exists)
        :param real_value: The real value/label for this prediction
        :param predicted_value: The predicted value/label
        :param histogram: The histogram for the predicted column, which allows us to bucketize the `predicted_value` and `real_value`
        """
        predicted_value = predicted_value if self.data_type != DATA_TYPES.NUMERIC else float(predicted_value)
        real_value = real_value if self.data_type != DATA_TYPES.NUMERIC else float(real_value)

        if self.buckets is not None:
            predicted_value_b = self._get_value_bucket(predicted_value)
            real_value_b = self._get_value_bucket(real_value)
            X = [False] * len(self.buckets)
            X[predicted_value_b] = True
            X = X + features_existence
            self.X_buff.append(X)
            self.Y_buff.append(real_value_b)
        else:
            predicted_value_b = predicted_value
            real_value_b = real_value
            self.X_buff.append(features_existence)
            self.Y_buff.append(real_value_b == predicted_value_b)

    def partial_fit(self):
        """
        # Fit the probabilistic validator on all observations recorder that haven't been taken into account yet
        """
        log_types = np.seterr()
        np.seterr(divide='ignore')

        if self.buckets is not None:
            self._probabilistic_model.partial_fit(self.X_buff, self.Y_buff, classes=self.bucket_keys)
        else:
            self._probabilistic_model.partial_fit(self.X_buff, self.Y_buff, classes=[True, False])

        np.seterr(divide=log_types['divide'])

        self.X_buff= []
        self.Y_buff= []

    def fit(self):
        """
        # Fit the probabilistic validator on all observations recorder that haven't been taken into account yet
        """
        log_types = np.seterr()
        np.seterr(divide='ignore')
        self._probabilistic_model.fit(self.X_buff, self.Y_buff)
        np.seterr(divide=log_types['divide'])

        self.X_buff= []
        self.Y_buff= []

    def evaluate_prediction_accuracy(self, features_existence, predicted_value):
        """
        # Fit the probabilistic validator on an observation

        :param features_existence: A vector of 0 and 1 representing the existence of all the features (0 == not exists, 1 == exists)
        :param predicted_value: The predicted value/label
        :param histogram: The histogram for the predicted column, which allows us to bucketize the `predicted_value`
        :return: The probability (from 0 to 1) of our prediction being accurate (within the same histogram bucket as the real value)
        """

        if self.buckets is not None:
            predicted_value_b = self._get_value_bucket(predicted_value)
            X = [False] * len(self.buckets)
            X[predicted_value_b] = True
            X = [X + features_existence]
        else:
            X = [features_existence]

        #X = [[predicted_value_b, *features_existence]]
        log_types = np.seterr()
        np.seterr(divide='ignore')
        distribution = self._probabilistic_model.predict_proba(np.array(X))
        np.seterr(divide=log_types['divide'])

        if self.buckets is not None:
            return ProbabilityEvaluation(self.buckets, distribution[0].tolist(), predicted_value).most_likely_probability
        else:
            return distribution[0][1]



if __name__ == "__main__":

    import random



    values = [2,2,2,3,5,2,2,2,3,5]
    predictions = [2,2,2,3,2,2,2,2,3,2]

    feature_rows = [
        [bool(random.getrandbits(1)), bool(random.getrandbits(1)), bool(random.getrandbits(1))]
        for i in values
    ]

    print(feature_rows)

    pbv = ProbabilisticValidator(buckets=[1,2,3,4,5])

    for i in range(len(feature_rows)):
        pbv.register_observation(feature_rows[i],values[i], predictions[i])

    pbv.partial_fit()
    print(pbv.evaluate_prediction_accuracy([True,True,True], 2))

    # Now test text tokens
    values = ['2', '2', '2', '3', '5', '2', '2', '2', '3', '5']
    predictions = ['2', '2', '2', '3', '2', '2', '2', '2', '3', '2']

    feature_rows = [
        [bool(random.getrandbits(1)), bool(random.getrandbits(1)), bool(random.getrandbits(1))]
        for i in values
    ]

    print(feature_rows)

    pbv = ProbabilisticValidator(buckets=['1', '2', '3', '4', '5'], data_type=DATA_TYPES.CATEGORICAL)

    for i in range(len(feature_rows)):
        pbv.register_observation(feature_rows[i], values[i], predictions[i])

    pbv.partial_fit()
    print(pbv.evaluate_prediction_accuracy([True, True, True], '2'))
