import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestRegressor

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler

import os

seed = 524

def test_data():
    """Create training and test data for function tests. Dataset is checked, cleaned and StandardScaled."""
    # read dataset from .csv
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test_data.csv'))
    # convert 'color' column to binary column 'is_red' with values 0 (white wine) and 1 (red wine)
    data['is_red'] = data['color'].apply(lambda x: 1 if x == 'red' else 0)
    data = data.drop(['color'], axis=1)
    # split into training and test sets with 80/20 ratio and random_state
    train_df, test_df = train_test_split(data, test_size=0.2, random_state=seed)
    X_train, X_test, y_train, y_test = (train_df.drop(columns='quality'), test_df.drop(columns='quality'),
                                    train_df['quality'], test_df['quality']
                                    )
    # apply StandardScaling to data since all columns are numerical (as a best practice)
    ss = StandardScaler()
    X_train_ss = ss.fit_transform(X_train)
    X_test_ss = ss.transform(X_test)
    # apply RobustScaling to X_test to be used for test cases with pipeline estimators
    rs = RobustScaler()
    rs.fit(X_train)
    X_test_rs = rs.transform(X_test)
    
    return {'X_train': X_train, 'X_train_ss': X_train_ss, 'X_test_ss': X_test_ss, 'X_test_rs': X_test_rs, 'y_train': y_train, 'y_test': y_test}


def models():
    """Create models as estimators for function tests.
    Note: Please use individual classifiers with X_train_ss and X_test_ss and pipeline with X_train and X_test_rs"""

    # create valid classifiers
    rf = RandomForestClassifier(n_estimators=10, random_state=seed)
    svm = SVC(kernel='rbf', decision_function_shape='ovr', random_state=seed)
    logreg = LogisticRegression(multi_class='multinomial', solver='lbfgs', random_state=seed)
    gb = GradientBoostingClassifier(random_state=seed)
    knn5 = KNeighborsClassifier(n_neighbors=5)
    mnp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=300, random_state=seed)
    pipe_svm = make_pipeline(RobustScaler(), svm)
    pipe_rf = make_pipeline(RobustScaler(), rf)
    pipe_knn5 = make_pipeline(RobustScaler(), knn5)
    pipe_gb = make_pipeline(RobustScaler(), gb)
    pipe_mnp = make_pipeline(RobustScaler(), mnp)

    # create lists of valid estimators
    knn5_and_mnb = [
    ('knn5', knn5),
    ('mnp', mnp)
    ]
    two_pipes = [
        ('pipe_rf', pipe_rf),
        ('pipe_svm', pipe_svm)
    ]
    multi_ind = [
        ('logreg', logreg),
        ('gb', gb),
        ('svm', svm),
        ('rf', rf),
        ('knn5', knn5)
    ]
    multi_pipe = [
        ('pipe_svm', pipe_svm),
        ('pipe_rf', pipe_rf),
        ('pipe_knn5', pipe_knn5),
        ('pipe_gb', pipe_gb),
        ('pipe_mnp', pipe_mnp)
    ]

    # create invalid estimators
    rfr = RandomForestRegressor()
    pipe_regressor = make_pipeline(RobustScaler(), rfr)
    
    return {'knn5': knn5, 'knn5_and_mnb': knn5_and_mnb, 'two_pipes': two_pipes, 'multi_ind': multi_ind, 'multi_pipe': multi_pipe, 'rfr': rfr, 'pipe_regressor': pipe_regressor}

