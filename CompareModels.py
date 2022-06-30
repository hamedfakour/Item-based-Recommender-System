
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error,accuracy_score,f1_score,recall_score,precision_score
import glob


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

    RF = RandomForestClassifier(n_estimators=3, bootstrap=True, max_features='sqrt', criterion='entropy')
    MLP = MLPClassifier(solver='lbfgs', alpha=0.001, hidden_layer_sizes=(20, 10), random_state=1, max_iter=3000, activation='relu')

    MLP.fit(X_train, Y_train)
    y_pred_mlp = MLP.predict(X_val)

    RF.fit(X_train, Y_train)
    y_pred_rf = RF.predict(X_val)
    # Comparing the predictions against the actual observations in y_val
    print('Files: ', file_path)
    cm_rf = confusion_matrix(y_pred_rf, y_val)
    print('RF: ', cm_rf)
    cm_mlp = confusion_matrix(y_pred_mlp, y_val)
    print('MLP: ' , cm_mlp)
    acc_rf = accuracy_score(y_val, y_pred_rf)
    acc_mlp = accuracy_score(y_val, y_pred_mlp)
    print("Accuracy: RF = {} , MLP = {}".format(acc_rf, acc_mlp) )
    rec_mlp = recall_score(y_val, y_pred_mlp)
    rec_rf = recall_score(y_val, y_pred_rf)
    print("Recall: RF = {} , MLP = {}".format(rec_rf, rec_mlp))
    precsn_mlp = precision_score(y_val, y_pred_mlp)
    precsn_rf = precision_score(y_val, y_pred_rf)
    print("Precision: RF = {} , MLP = {}".format(precsn_rf, precsn_mlp))
    f1_mlp = f1_score(y_val, y_pred_mlp)
    f1_rf = f1_score(y_val, y_pred_rf)
    print("F1 Score: RF = {} , MLP = {}".format(f1_rf, f1_mlp))
    mse_mlp = mean_squared_error(y_val, y_pred_mlp)
    mse_rf = mean_squared_error(y_val, y_pred_rf)
    print("MSE: RF = {} , MLP = {}".format(mse_rf, mse_mlp))
    rmse_mlp = mean_squared_error(y_val, y_pred_mlp, squared=False)
    rmse_rf = mean_squared_error(y_val, y_pred_rf, squared=False)
    print("RMSE: RF = {} , MLP = {}".format(rmse_rf, rmse_mlp))
    return acc_mlp, acc_rf, rec_mlp, rec_rf, precsn_mlp, precsn_rf, f1_mlp, f1_rf, mse_mlp, mse_rf, rmse_mlp, rmse_rf


def ResultValidateAllItems():
    files = glob.glob("resources/users_features/*.csv")
    RMSE_MLP = MSE_MLP = Accuracy_MLP = Recall_MLP = Precision_MLP = F1_MLP =0.0
    RMSE_RF = MSE_RF = Accuracy_RF = Recall_RF = Precision_RF = F1_RF = 0.0
    for f in files:
        acc_mlp, acc_rf, rec_mlp, rec_rf, precsn_mlp, precsn_rf, f1_mlp, f1_rf, mse_mlp, mse_rf, rmse_mlp, rmse_rf = ValidateItem(f)
        Accuracy_MLP += acc_mlp
        Recall_MLP += rec_mlp
        Precision_MLP += precsn_mlp
        F1_MLP += f1_mlp
        MSE_MLP += mse_mlp
        RMSE_MLP += rmse_mlp
        Accuracy_RF += acc_rf
        Recall_RF += rec_rf
        Precision_RF += precsn_rf
        F1_RF += f1_rf
        MSE_RF += mse_rf
        RMSE_RF += rmse_rf
        print('==============================================')
    print('\t\t\tResults\n==============================================\n')
    Num = len(files)
    print('=============== MLP ===============\nAccuracy: {:.2f}\nPrecision: {:.2f}\nRecall: {:.2f}\nF1: {:.2f}\nMSE: {:.2f}\nRMSE: {:.2f}'
          .format(Accuracy_MLP/Num, Precision_MLP/Num, Recall_MLP/Num, F1_MLP/Num, MSE_MLP/Num, RMSE_MLP/Num))
    print('=============== RF ===============\nAccuracy: {:.2f}\nPrecision: {:.2f}\nRecall: {:.2f}\nF1: {:.2f}\nMSE: {:.2f}\nRMSE: {:.2f}'
          .format(Accuracy_RF / Num, Precision_RF / Num, Recall_RF / Num, F1_RF / Num, MSE_RF / Num, RMSE_RF / Num))



ResultValidateAllItems()