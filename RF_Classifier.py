
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error,accuracy_score,f1_score,recall_score,precision_score
from sklearn.preprocessing import StandardScaler
import pandas as pd
from numpy import mean
from numpy import std
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_predict


def ValidateItem(file_path):
    data = pd.read_csv(file_path)
    training_set, validation_set = train_test_split(data, test_size=0.2, random_state=0)
    sc = StandardScaler()
    X_train = training_set.iloc[:, 0:-1].values
    sc.fit(X_train)
    X_train = sc.transform(X_train)
    Y_train = training_set.iloc[:, -1].values
    X_val = sc.transform(validation_set.iloc[:, 0:-1].values)
    y_val = validation_set.iloc[:, -1].values
    # Fitting the training data to the network
    classifier = RandomForestClassifier(n_estimators=3, bootstrap = True, max_features = 'sqrt', criterion='entropy')
    classifier.fit(X_train, Y_train)
    # cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
    # n_scores = cross_val_score(classifier, X_train, Y_train, scoring='recall_macro', cv=cv, n_jobs=-1, error_score='raise')
    # y_pred = cross_val_predict(classifier, X_val, y_val, cv=3)
    # print('Accuracy: %.3f (%.3f)' % (mean(n_scores), std(n_scores)))
    # Predicting y for X_val
    y_pred = classifier.predict(X_val)
    # # Comparing the predictions against the actual observations in y_val
    # print('Files: ', file_path)
    cm = confusion_matrix(y_pred, y_val)
    print(cm)
    acc = accuracy_score(y_val, y_pred)
    print("Accuracy: ", acc)
    rec = recall_score(y_val, y_pred)
    print("Recall: ", rec)
    precsn = precision_score(y_val, y_pred)
    print("Precision: ", precsn)
    f1 = f1_score(y_val, y_pred)
    print("F1 Score: ", f1)
    mse = mean_squared_error(y_val, y_pred)
    print("MSE: ", mse)
    rmse = mean_squared_error(y_val, y_pred, squared=False)
    print("RMSE: ", rmse)
    # return acc, rec, precsn, f1, mse, rmse


ValidateItem('resources/users_features/33595.csv')