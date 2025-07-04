import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

data = {
    'menu_code': [0, 1, 2, 3, 4, 5, 6, 7],
    'num_items': [1, 2, 3, 1, 2, 1, 1, 1],
    'time_of_day': [12, 14, 13, 18, 19, 11, 10, 9],
    'kitchen_load': [2, 3, 4, 3, 5, 1, 1, 2],
    'wait_time': [5, 10, 15, 9, 20, 4, 5, 6]
}

df = pd.DataFrame(data)
X = df[['menu_code', 'num_items', 'time_of_day', 'kitchen_load']]
y = df['wait_time']

model = LinearRegression()
model.fit(X, y)

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved.")
