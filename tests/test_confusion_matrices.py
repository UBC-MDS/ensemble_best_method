from compare_classifiers.confusion_matrices import confusion_matrices

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tests.test_data import test_data, models

import matplotlib

# Create test data

data_dict = test_data()
X_train = data_dict['X_train']
X_train_ss = data_dict['X_train_ss']
X_test_ss = data_dict['X_test_ss']
X_test_rs = data_dict['X_test_rs']
y_train = data_dict['y_train']
y_test = data_dict['y_test']

model_dict = models()
knn5 = model_dict['knn5']
knn5 = model_dict['knn5']
knn5_and_mnb = model_dict['knn5_and_mnb']
two_pipes = model_dict['two_pipes']
multi_ind = model_dict['multi_ind']
multi_pipe = model_dict['multi_pipe']

matplotlib.use('Agg')

def test_individual_success():
    """When estimators is a list of individual Classifiers, returns the plot containing one confusion matrix for each estimator."""
    axes = confusion_matrices(knn5_and_mnb, X_train_ss, X_test_ss, y_train, y_test)
    # Check if the plot contains the correct number of subplots
    assert(axes.shape == (2,))
    # Check if the subplots are sklearn confusion matrices corresponding to the estimators
    for i, ax in enumerate(axes.flatten()):
        assert([e[0] for e in knn5_and_mnb][i] == ax.title.get_text())
        assert(ax.has_data() and ax.get_xaxis().get_label() is not None)

def test_pipeline_success():
    """When estimators is a list of pipelines, returns the plot containing one confusion matrix for each estimator."""
    axes = confusion_matrices(two_pipes, X_train_ss, X_test_ss, y_train, y_test)
    # Check if the plot contains the correct number of subplots
    assert(axes.shape == (2,))
    # Check if the subplots are sklearn confusion matrices corresponding to the estimators
    for i, ax in enumerate(axes.flatten()):
        assert([e[0] for e in two_pipes][i] == ax.title.get_text())
        assert(ax.has_data() and ax.get_xaxis().get_label() is not None)

def test_multi_individual_success():
    """When estimators is a list of more than 2 individual Classifiers, returns the plot containing one confusion matrix for each estimator."""
    axes = confusion_matrices(multi_ind, X_train_ss, X_test_ss, y_train, y_test)
    # Check if the plot contains the correct number of subplots
    assert(axes.shape == (5,))
    # Check if the subplots are sklearn confusion matrices corresponding to the estimators
    for i, ax in enumerate(axes.flatten()):
        assert([e[0] for e in multi_ind][i] == ax.title.get_text())
        assert(ax.has_data() and ax.get_xaxis().get_label() is not None)

def test_multi_pipeline_success():
    """When estimators is a list of more than 2 pipelines, returns the plot containing one confusion matrix for each estimator."""
    axes = confusion_matrices(multi_pipe, X_train_ss, X_test_ss, y_train, y_test)
    # Check if the plot contains the correct number of subplots
    assert(axes.shape == (5,))
    # Check if the subplots are sklearn confusion matrices corresponding to the estimators
    for i, ax in enumerate(axes.flatten()):
        assert([e[0] for e in multi_pipe][i] == ax.title.get_text())
        assert(ax.has_data() and ax.get_xaxis().get_label() is not None)