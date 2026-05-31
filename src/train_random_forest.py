#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
try:
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    import numpy as np
except Exception as e:
    print('scikit-learn not installed. Skip AI training. Install with: pip install scikit-learn')
    raise SystemExit

df=pd.read_csv(ROOT/'results/hydrogen_ai_dataset.csv')
if len(df)<10:
    print('Not enough cases for AI training. Run more cases.'); raise SystemExit
features=[c for c in df.columns if c.startswith('S')]
X=df[features]
y=df[['leak_x','leak_y','leak_z']]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=7)
model=RandomForestRegressor(n_estimators=250,random_state=7,min_samples_leaf=2)
model.fit(X_train,y_train)
pred=model.predict(X_test)
mae=mean_absolute_error(y_test,pred,multioutput='raw_values')
rmse=np.sqrt(mean_squared_error(y_test,pred,multioutput='raw_values'))
report=pd.DataFrame({'axis':['x','y','z'],'MAE_m':mae,'RMSE_m':rmse})
report.to_csv(ROOT/'results/ai_random_forest_metrics.csv',index=False)
imp=pd.DataFrame({'sensor_id':features,'importance':model.feature_importances_}).sort_values('importance',ascending=False)
imp.to_csv(ROOT/'results/ai_sensor_importance.csv',index=False)
print('Random Forest metrics:'); print(report)
print('Top AI sensor importance:'); print(imp.head(10))
