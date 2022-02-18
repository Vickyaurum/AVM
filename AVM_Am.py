import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier
from scipy.stats import norm
import xgboost

# df= pd.read_csv(r"D:\python folder\PycharmProjects\pythonProject2\Gis_Final_Pune_ml_new.csv")
# df= pd.read_excel(r"C:\Users\Yogesh.Tiwari\PycharmProjects\pythonProject\Final_Pune_listing_amenity_data.xlsx")
# df= pd.read_excel(r"C:\Users\Yogesh.Tiwari\PycharmProjects\pythonProject\Persqft_pune.xlsx")
dd=pd.read_csv(r"ABC_ref.csv")
df= pd.read_excel(r"Positive_Pune_AVM15Fev.xlsx")

################################ project name handling #######################################

# Import label encoder
from sklearn import preprocessing

# label_encoder object knows how to understand word labels.
laben = preprocessing.LabelEncoder()
print("LABEN")
# Encode labels in column 'species'.
dd['encoded_project_name']= laben.fit_transform(dd['Project_Name'])
dd['encoded_project_name'].unique()
print(len(dd['encoded_project_name'].unique()))
def get_proj(list1):
  ss = list1
  for k,v in le_project_mapping.items():
    if ss[-1] in str(f"{k}"):
      print("PPPPPPPPPPPPPPPPPPPPPPPP",le_project_mapping[k])
      return le_project_mapping[k]
    else:
      return 0

le_project_mapping = dict(zip(laben.classes_, laben.transform(laben.classes_)))
# print(le_project_mapping)

df=df.drop(['Unnamed: 0'],axis='columns')
dd=dd.drop(['Unnamed: 0'],axis='columns')

maxy=df['Per_Sq_Ft'].quantile(0.99)
print(maxy)
miny=df['Per_Sq_Ft'].quantile(0.01)
print(miny)
df2 = df[(df.Per_Sq_Ft<maxy) & (df.Per_Sq_Ft>miny)]
print(df2.shape)
# df2 = df[(df.Price<60000000) & (df.Price>2000000)]
# print(df2.shape)

#################### Train Test split (80:20) ###########################
# dff_Train = df2.iloc[:8992,:]
# dff_Test = df2.iloc[8992:,:]

### with per_sq_ft
dff_Train = df2.iloc[:9449,:]
dff_Test = df2.iloc[9449:,:]
################# From Train dataset we create x_train and y_train #####################
##### with price
# X_train=dff_Train.drop(['Price'],axis=1)
# y_train=dff_Train['Price']
# y_train.shape
# dff_Test.drop(['Price'],axis=1,inplace=True)

# with perSqFT
X_train=dff_Train.drop(['Per_Sq_Ft'],axis=1)
y_train=dff_Train['Per_Sq_Ft']
y_train.shape
dff_Test.drop(['Per_Sq_Ft'],axis=1,inplace=True)



X_train1, X_test1, y_train1, y_test1 = train_test_split(X_train, y_train, test_size=0.33, random_state=7)

import xgboost
regressor = xgboost.XGBRegressor(base_score=0.75, max_depth=5, min_child_weight=2,
             n_estimators=1100)
regressor.fit(X_train1,y_train1)

import joblib

# file_name = "Pune_am_xgb_reg_gis.pkl"

### persqft
file_name = "Positive_Per_Sq_Pune_pk_15feb.pkl"
#save model
joblib.dump(regressor, file_name)

#load saved model
xgb = joblib.load(file_name)
