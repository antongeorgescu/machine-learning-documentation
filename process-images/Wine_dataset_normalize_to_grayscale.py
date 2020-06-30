import pandas as pd
import numpy as np

REDWINE_PATH = "./datasets/winequality-red.csv"
WHITEWINE_PATH = "./datasets/winequality-white.csv"

# read red wine set of observations
data_red = pd.read_csv(REDWINE_PATH,sep=',')
data_red['color'] = 1 #redwine

print(data_red.shape)

# read white wine set of observations
data_white = pd.read_csv(WHITEWINE_PATH,sep=',')
data_white['color'] = 0 #whitewine

print(data_white.shape)

# merge the two sets in one
data = data_red.merge(data_white, how='outer')
fields = list(data.columns)
print(fields)

print(data)

import pandas as pd
import numpy as np

data_red = pd.read_csv(REDWINE_PATH,sep=',')
data_red['color'] = 1 #redwine

print(data_red.shape)

data_white = pd.read_csv(WHITEWINE_PATH,sep=',')
data_white['color'] = 0 #whitewine

print(data_white.shape)

data = data_red.merge(data_white, how='outer')

data.quality.value_counts()


fields = list(data.columns)
print(fields)


# split the data set in two: 1) color+features (observations)  2) quality (actuals)

fields = list(data.columns[:-2])
fields.append('color')  #adding color back
X = data[fields]
y = data['quality']
print(fields)

from sklearn.preprocessing import MinMaxScaler

X = data[fields]

scaler = MinMaxScaler(feature_range=(0,255))
X = scaler.fit_transform(X)
X = pd.DataFrame(X, columns=['%s_scaled' % fld for fld in fields])
print(X.columns) #scaled columns

Xint = X.astype(np.int64).to_numpy()
print(Xint.shape)

# reshape to 2d
Xint2d = np.reshape(Xint,(6497,12)).astype(np.int64)

np.savetxt('./converted/winequality.csv',Xint2d,delimiter=",",fmt="%3d")



