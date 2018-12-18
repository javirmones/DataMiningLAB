#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn import tree
from sklearn.model_selection import KFold
import pandas as pd
import numpy as np
import pydot
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus
import Paths as route_of

def read_dataset(path):
    return pd.read_csv(path)

def to_csv(path,dataframe):
    np.savetxt(path, dataframe, delimiter=",")

def cross_validations_aux(dataframe):
  cv = KFold(n_splits = 10, shuffle = False)
  accuracies = list()
  max_attributes = len(list(dataframe))
  depth_range = range(1, max_attributes * 2)
    
  for depth in depth_range:
      fold_accuracy = []
      tree_model = tree.DecisionTreeClassifier(criterion='entropy', 
                                               min_samples_split = 65, 
                                               min_samples_leaf = 20,
                                               max_depth = depth,
                                               class_weight={0:3.28}
                                              )
      for train_fold, test_fold in cv.split(dataframe):
          f_train = dataframe.loc[train_fold]
          f_test = dataframe.loc[test_fold]
          
          model = tree_model.fit( X = f_train.drop(['attack'], axis=1), 
                                 y = f_train['attack'])
          test_acc = model.score(X = f_test.drop(['attack'], axis=1), 
                                  y = f_test['attack'])
          fold_accuracy.append(test_acc)
          
      avg = sum(fold_accuracy)/len(fold_accuracy)
      accuracies.append(avg)

def cross_validations(dataframe, tree_model):
    cv = KFold(n_splits = 10, shuffle=False)
    acc = list()
    max_attb = len(list(dataframe))
    depth_range = range(1, max_attb * 2)

    
    for depth in depth_range:
      fold_accuracy = []
        
      for train_fold, test_fold in cv.split(dataframe):
        f_test = dataframe.loc[test_fold]

        test_acc = tree_model.score(X = f_test.drop(['attack'], axis=1), 
                                  y = f_test['attack'])
        fold_accuracy.append(test_acc)  

      average = sum(fold_accuracy)/len(fold_accuracy)
      acc.append(average)

#    plt.plot(depth_range, acc, marker='o')
#    plt.xlabel('max_depth')
#    plt.ylabel('accuracy')
#    plt.show()
#    plt.savefig("plots/accuracie.png")

def divide_datasets(df_merged):
    # Mezclamos y requetemezclamos
    df_divide = df_merged.sample(frac=1)
    # 1/3 for test  2/3 for train
    p = 0.67
    df_train = df_divide[:int((len(df_divide))*p)]
    df_test = df_divide[int((len(df_divide))*p):]
    
    return df_train,df_test

def decision_tree(train, test):
    features  = train.columns[:15]
    x_train   = train[features]
    y_train   = train['group']
    
    x_test    = test[features]
    y_test    = test['group']
    
    X, y      = x_train, y_train
  
    clf = tree.DecisionTreeClassifier(criterion='entropy')
    
    clf.fit(X, y)

    preds_dt = clf.predict(x_test)
    
    print("Decision treee: \n" 
          +classification_report(y_true=y_test, y_pred=preds_dt))
    
    # Matriz de confusión
    
    print("Matriz de confusión:\n")
    matriz = pd.crosstab(test['group'], preds_dt, rownames=['actual'], colnames=['preds'])
    print(matriz)
    
    # Variables relevantes
    
    print("Relevancia de variables:\n")
    print(pd.DataFrame({'Indicador': features ,
                  'Relevancia': clf.feature_importances_}),"\n")
    print("Máxima relevancia RF :" , max(clf.feature_importances_), "\n")
    
    dot_data = StringIO()

    export_graphviz(clf, out_file=dot_data,
                    feature_names=list(test.drop(['group'], axis=1)),
                    filled=True, rounded=True,
                    special_characters=True, class_names = ['low','regular', 'quality'])
  
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
    graph.write_png(route_of.plots.format('decision_tree_all_kind_course'))
        
    return clf,graph

def production_simulation(clf_rf, dataset_prueba):
    dataset_prod = pd.concat([dataset_prueba, test])
    dataset_prod = dataset_prod.sample(frac=1)
  
    features  = dataset_prod.columns[:13]
    x_test    = dataset_prod[features]
    y_test    = dataset_prod['attack']
  
    preds_rf = clf_rf.predict(x_test) # Test del modelo
    
#    report(random_search.cv_results_)    
    
    print("Random Forest: \n" 
          +classification_report(y_true=y_test, y_pred=preds_rf))
    
    # Matriz de confusión
    
    print("Matriz de confusión:\n")
    matriz = pd.crosstab(dataset_prod['attack'], preds_rf, rownames=['actual'], colnames=['preds'])
    print(matriz)
    
    # Variables relevantes
    
    print("Relevancia de variables:\n")
    print(pd.DataFrame({'Indicador': features ,
                  'Relevancia': clf_rf.feature_importances_}),"\n")
    print("Máxima relevancia RF :" , max(clf_rf.feature_importances_), "\n")

if __name__ == '__main__':
  data_train, data_test             = divide_datasets(data_target_treated)
#  data_train_low, data_test_low     = divide_datasets(data_target_treated[(data_target_treated['group'] == 'low_quality_course')])
#  data_train_reg, data_test_reg     = divide_datasets(data_target_treated[(data_target_treated['group'] == 'regular_course')])
#  data_train_high, data_test_high   = divide_datasets(data_target_treated[(data_target_treated['group'] == 'quality_course')])
#  
#  train.drop(train.columns[[0,1]], axis=1, inplace=True)
#  test.drop(test.columns[[0,1]], axis=1, inplace=True)
  
  decision_birch, graph = decision_tree(data_train, data_test)
   
   
   
   
   
