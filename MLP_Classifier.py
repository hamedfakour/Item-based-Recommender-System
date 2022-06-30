
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error,accuracy_score,f1_score,recall_score,precision_score
import glob


def ValidateItem(file_path, classifier):
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
    classifier.fit(X_train, Y_train)
    # Predicting y for X_val
    y_pred = classifier.predict(X_val)
    # Comparing the predictions against the actual observations in y_val
    print('Files: ', file_path)
    cm = confusion_matrix(y_pred, y_val)
    print(cm)
    acc = accuracy_score(y_val, y_pred)
    print("Accuracy: ", acc)
    # rec = recall_score(y_val, y_pred)
    rec = cm[1][1:] / (cm[1][1:] + cm[0][1:])
    print("Recall: ", rec)
    # precsn = precision_score(y_val, y_pred)
    precsn = cm[1][1:] / (cm[1][1:] + cm[1][:1])
    print("Precision: ", precsn)
    f1 = f1_score(y_val, y_pred)
    print("F1 Score: ", f1)
    mse = mean_squared_error(y_val, y_pred)
    print("MSE: ", mse)
    rmse = mean_squared_error(y_val, y_pred, squared=False)
    print("RMSE: ", rmse)
    return acc, rec, precsn, f1, mse, rmse



def ResultValidateAllItems():
    files = glob.glob("resources/users_features/*_MLP.csv")
    RMSE = 0.0
    MSE = 0.0
    Accuracy = 0.0
    Recall = 0.0
    Precision = 0.0
    F1 = 0.0
    # Initializing the MLPClassifier
    # classifier = MLPClassifier(solver='lbfgs', alpha=0.001, hidden_layer_sizes=(45,45,10), random_state=1,  max_iter=6000, activation='relu')
    classifier = MLPClassifier(solver='lbfgs', alpha=0.001, hidden_layer_sizes=(45, 10), random_state=1, max_iter=5000, activation='relu')
    for f in files:
        acc, rec, precsn, f1, mse, rmse = ValidateItem(f, classifier)
        Accuracy += acc
        Recall += rec
        Precision += precsn
        F1 += f1
        MSE += mse
        RMSE += rmse
        print('==============================================')
    print('\t\t\tResults\n==============================================\n')
    Num = len(files)
    print('Accuracy: {:.2f}\nPrecision: {:.2f}\nRecall: {:.2f}\nF1: {:.2f}\nMSE: {:.2f}\nRMSE: {:.2f}'
          .format(Accuracy/Num, Precision/Num, Recall/Num, F1/Num, MSE/Num, RMSE/Num))



# ResultValidateAllItems()
features_file_path = 'resources/users_features/10623.csv'
classifier = MLPClassifier(solver='lbfgs', alpha=0.001, hidden_layer_sizes=(45, 15), random_state=1, max_iter=3000, activation='relu')
ValidateItem(features_file_path, classifier)
