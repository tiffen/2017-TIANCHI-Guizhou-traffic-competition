# coding: utf-8
# pylint: disable = invalid-name, C0111
import lightgbm as lgb
import pandas as pd
import numpy as np
import gc

from scipy.stats import mode
def add_constact(df):
    return np.sum(1.0/df) / np.sum(1.0/df/df)
# customes 
def mape_object(y,d):
    d = d.get_label()
    g = 1.0*np.sign(y-d)/d
    h = 1.0/d
    return g,h
# 评价函数ln形式
def mape_ln(y,d):
    c=d.get_label()
    result= np.sum(np.abs(np.expm1(y)-np.abs(np.expm1(c)))/np.abs(np.expm1(c)))/len(c)
    return "mape",result,False
# 中位数
def mode_function(df):
    # print df
    df = df.astype(int)
    # print df
    counts = mode(df)
    return counts[0][0]
# load or create your dataset

print('Load data...')

print u'8'
feature_data = pd.read_csv('./pre_data/feature_data.csv')
feature_data['link_ID'] = feature_data['link_ID'].astype(str)
week = pd.get_dummies(feature_data['time_interval_week'],prefix='week')
feature_data.drop(['time_interval_week','link_class'],inplace=True,axis=1)
feature_data = pd.concat([feature_data,week],axis=1)
print feature_data.head()
# print feature_data[feature_data.time_interval_begin_hour== 8]

train48 = feature_data.loc[(feature_data.time_interval_month == 4)&(feature_data.time_interval_begin_hour==8),: ]
for i in [58,48,38,28,18,8,0]:
    tmp = feature_data.loc[(feature_data.time_interval_month == 4)&(feature_data.time_interval_begin_hour == 7)&(feature_data.time_interval_minutes >= i),:]
    tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
            'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                ('mode_%d' % (i), mode_function), ('std_%d' % (i), np.std),('min_%d' % (i), np.min)]).reset_index()
    tmp['std_%d' % (i)] = tmp['std_%d' % (i)].fillna(0)
    train48 = pd.merge(train48,tmp,on=['link_ID','time_interval_day'],how='left')

train58 = feature_data.loc[(feature_data.time_interval_month == 5)&(feature_data.time_interval_begin_hour== 8),: ]
for i in [58,48,38,28,18,8,0]:
    tmp = feature_data.loc[(feature_data.time_interval_month == 5)&(feature_data.time_interval_begin_hour == 7)&(feature_data.time_interval_minutes >= i),:]
    tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
            'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                ('mode_%d' % (i), mode_function), ('std_%d' % (i), np.std),('min_%d' % (i), np.min)]).reset_index()
    tmp['std_%d' % (i)] = tmp['std_%d' % (i)].fillna(0)
    train58 = pd.merge(train58,tmp,on=['link_ID','time_interval_day'],how='left')

train67 = feature_data.loc[(feature_data.time_interval_month == 6)&(feature_data.time_interval_begin_hour==7),: ]
for i in [58,48,38,28,18,8,0]:
    tmp = feature_data.loc[(feature_data.time_interval_month == 6)&(feature_data.time_interval_begin_hour == 6)&(feature_data.time_interval_minutes >= i),:]
    tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
            'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                ('mode_%d' % (i), mode_function), ('std_%d' % (i), np.std),('min_%d' % (i), np.min)]).reset_index()
    tmp['std_%d' % (i)] = tmp['std_%d' % (i)].fillna(0)
    train67 = pd.merge(train67,tmp,on=['link_ID','time_interval_day'],how='left')

train66 = feature_data.loc[(feature_data.time_interval_month == 6)&(feature_data.time_interval_begin_hour== 6),: ]
for i in [58,48,38,28,18,8,0]:
    tmp = feature_data.loc[(feature_data.time_interval_month == 6)&(feature_data.time_interval_begin_hour == 5)&(feature_data.time_interval_minutes >= i),:]
    tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
            'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                ('mode_%d' % (i), mode_function), ('std_%d' % (i), np.std),('min_%d' % (i), np.min)]).reset_index()
    tmp['std_%d' % (i)] = tmp['std_%d' % (i)].fillna(0)
    train66 = pd.merge(train66,tmp,on=['link_ID','time_interval_day'],how='left')


train56 = feature_data.loc[(feature_data.time_interval_month == 5)&(feature_data.time_interval_begin_hour==6),: ]
for i in [58,48,38,28,18,8,0]:
    tmp = feature_data.loc[(feature_data.time_interval_month == 5)&(feature_data.time_interval_begin_hour == 5)&(feature_data.time_interval_minutes >= i),:]
    tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
             'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                 ('mode_%d' % (i), mode_function), ('std_%d' % (i), np.std),('min_%d' % (i), np.min)]).reset_index()
    tmp['std_%d' % (i)] = tmp['std_%d' % (i)].fillna(0)
    train56 = pd.merge(train56,tmp,on=['link_ID','time_interval_day'],how='left')

train57 = feature_data.loc[(feature_data.time_interval_month == 5)&(feature_data.time_interval_begin_hour==7),: ]
for i in [58,48,38,28,18,8,0]:
    tmp = feature_data.loc[(feature_data.time_interval_month == 5)&(feature_data.time_interval_begin_hour == 6)&(feature_data.time_interval_minutes >= i),:]
    tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
             'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                 ('mode_%d' % (i), mode_function), ('std_%d' % (i), np.std),('min_%d' % (i), np.min)]).reset_index()
    tmp['std_%d' % (i)] = tmp['std_%d' % (i)].fillna(0)
    train57 = pd.merge(train57,tmp,on=['link_ID','time_interval_day'],how='left')

train47 = feature_data.loc[(feature_data.time_interval_month == 4)&(feature_data.time_interval_begin_hour==7),: ]
for i in [58,48,38,28,18,8,0]:
    tmp = feature_data.loc[(feature_data.time_interval_month == 4)&(feature_data.time_interval_begin_hour == 6)&(feature_data.time_interval_minutes >= i),:]
    tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
            'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                ('mode_%d' % (i), mode_function), ('std_%d' % (i), np.std),('min_%d' % (i), np.min)]).reset_index()
    tmp['std_%d' % (i)] = tmp['std_%d' % (i)].fillna(0)
    train47 = pd.merge(train47,tmp,on=['link_ID','time_interval_day'],how='left')

train418 = feature_data.loc[(feature_data.time_interval_month == 4)&(feature_data.time_interval_begin_hour==18),: ]
for i in [58,48,38,28,18,8,0]:
    tmp = feature_data.loc[(feature_data.time_interval_month == 4)&(feature_data.time_interval_begin_hour == 17)&(feature_data.time_interval_minutes >= i),:]
    tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
            'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                ('mode_%d' % (i), mode_function), ('std_%d' % (i), np.std),('min_%d' % (i), np.min)]).reset_index()
    tmp['std_%d' % (i)] = tmp['std_%d' % (i)].fillna(0)
    train418 = pd.merge(train418,tmp,on=['link_ID','time_interval_day'],how='left')

train518 = feature_data.loc[(feature_data.time_interval_month == 5)&(feature_data.time_interval_begin_hour==18),: ]
for i in [58,48,38,28,18,8,0]:
    tmp = feature_data.loc[(feature_data.time_interval_month == 5)&(feature_data.time_interval_begin_hour == 17)&(feature_data.time_interval_minutes >= i),:]
    tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
            'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                ('mode_%d' % (i), mode_function), ('std_%d' % (i), np.std),('min_%d' % (i), np.min)]).reset_index()
    tmp['std_%d' % (i)] = tmp['std_%d' % (i)].fillna(0)
    train518 = pd.merge(train518,tmp,on=['link_ID','time_interval_day'],how='left')

train = pd.concat([train418,train518,train67,train57,train58,train47,train48,train66,train56],axis=0)

############################################################################################################################################################

train_history = feature_data.loc[(feature_data.time_interval_month == 4),: ]
train_history = train_history.groupby(['link_ID', 'time_interval_minutes'])[
            'travel_time'].agg([('mean_m', np.mean), ('median_m', np.median),
                                ('mode_m', mode_function), ('std_m', np.std), ('max_m', np.max),('min_m', np.min)]).reset_index()
# train_history['median_mode'] = 0.5 * train_history['mode_m'] + 0.5 * train_history['median_m']

train = pd.merge(train,train_history,on=['link_ID','time_interval_minutes'],how='left')

train_constacot = feature_data.loc[(feature_data.time_interval_month == 4),: ]
train_constacot = train_constacot.groupby(['link_ID'])[
            'travel_time'].agg([('constatic_m_1', add_constact)]).reset_index()
train = pd.merge(train,train_constacot,on=['link_ID'],how='left')

# train['speed_max'] = train['length']  / train['min_m']
# train['speed_min'] = train['length']  / train['max_m']
train['speed_mode'] = train['length']  / train['mode_m']
train['speed_median'] = train['length']  / train['median_m']

# train['120_speed'] = train['length']  / 120.0
train['mean_std'] = train['mean_m']  / train['std_m']
train['max_min_distance'] = train['max_m'] - train['min_m']

train_8 = feature_data.loc[(feature_data.time_interval_month == 4)&(feature_data.time_interval_begin_hour == 8),: ]
train_8 = train_8.groupby(['link_ID', 'time_interval_minutes'])[
            'travel_time'].agg([('median_8_', np.median)]).reset_index()

train = pd.merge(train,train_8,on=['link_ID','time_interval_minutes'],how='left')
train = train.fillna(-1)

train.drop(['link_ID','time_interval_begin_hour','time_interval_month','time_interval_begin','std_m','std_58','max_m','mode_m'],inplace=True,axis=1)
print train.shape

train_label = np.log1p(train.pop('travel_time'))
train_label = train_label.values
train = train.values


test = feature_data.loc[(feature_data.time_interval_month == 6)&(feature_data.time_interval_begin_hour==8),: ]
for i in [58,48,38,28,18,8,0]:
    tmp = feature_data.loc[(feature_data.time_interval_month == 6)&(feature_data.time_interval_begin_hour == 7)&(feature_data.time_interval_minutes >= i),:]
    tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
            'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                ('mode_%d' % (i), mode_function), ('std_%d' % (i), np.std),('min_%d' % (i), np.min)]).reset_index()
    tmp['std_%d' % (i)] = tmp['std_%d' % (i)].fillna(0)
    test = pd.merge(test,tmp,on=['link_ID','time_interval_day'],how='left')


test_history = feature_data.loc[(feature_data.time_interval_month == 5),: ]
test_history = test_history.groupby(['link_ID', 'time_interval_minutes'])[
            'travel_time'].agg([('mean_m', np.mean), ('median_m', np.median),
                                ('mode_m', mode_function), ('std_m', np.std), ('max_m', np.max),('min_m', np.min)]).reset_index()
# test_history['median_mode'] = 0.5 * test_history['mode_m'] + 0.5 * test_history['median_m']
test = pd.merge(test,test_history,on=['link_ID','time_interval_minutes'],how='left')

test_constacot = feature_data.loc[(feature_data.time_interval_month == 5),: ]
test_constacot = test_constacot.groupby(['link_ID'])[
            'travel_time'].agg([('constatic_m_1', add_constact)]).reset_index()
test = pd.merge(test,test_constacot,on=['link_ID'],how='left')
# test['speed_max'] = test['length']  / test['min_m']
# test['speed_min'] = test['length']  / test['max_m']
test['speed_mode'] = test['length']  / test['mode_m']
test['speed_median'] = test['length']  / test['median_m']

# test['120_speed'] = test['length']  / 120.0
test['mean_std'] = test['mean_m']  / test['std_m']
test['max_min_distance'] = test['max_m'] - test['min_m']

test_8 = feature_data.loc[(feature_data.time_interval_month == 5)&(feature_data.time_interval_begin_hour == 8),: ]
test_8 = test_8.groupby(['link_ID', 'time_interval_minutes'])[
            'travel_time'].agg([('median_8_', np.median)]).reset_index()

test = pd.merge(test,test_8,on=['link_ID','time_interval_minutes'],how='left')

print test.head()
# analy_data_org = test.copy()
# 缺失值的处理
test.drop(['link_ID','time_interval_begin_hour','time_interval_month','time_interval_begin','std_m','std_58','max_m','mode_m'],inplace=True,axis=1)
test = test.fillna(-1)
test_label = np.log1p(test.pop('travel_time'))

test_label = test_label.values
test = test.values


print('Start training...')
# train
lgb_train = lgb.Dataset(train, train_label)
lgb_eval = lgb.Dataset(test, test_label, reference=lgb_train)

params = {
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': 'rmse',
    'num_leaves': 128,
    'learning_rate': 0.0025,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': 0
}

gbm = lgb.train(params,
                lgb_train,
                num_boost_round=5000,
                # init_model=gbm,
                fobj=mape_object,
                feval=mape_ln,
                valid_sets=lgb_eval,
                early_stopping_rounds = 20)
                
print('Start predicting...')
# predict
sub = feature_data.loc[(feature_data.time_interval_month == 7)&(feature_data.time_interval_begin_hour==8),: ]
for i in [58,48,38,28,18,8,0]:
    tmp = feature_data.loc[(feature_data.time_interval_month == 7)&(feature_data.time_interval_begin_hour == 7)&(feature_data.time_interval_minutes >= i),:]
    tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
            'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                ('mode_%d' % (i), mode_function), ('std_%d' % (i), np.std),('min_%d' % (i), np.min)]).reset_index()
    tmp['std_%d' % (i)] = tmp['std_%d' % (i)].fillna(0)
    sub = pd.merge(sub,tmp,on=['link_ID','time_interval_day'],how='left')

sub_history = feature_data.loc[(feature_data.time_interval_month == 5),: ]
sub_history = sub_history.groupby(['link_ID', 'time_interval_minutes'])[
            'travel_time'].agg([('mean_m', np.mean), ('median_m', np.median),
                                ('mode_m', mode_function), ('std_m', np.std), ('max_m', np.max),('min_m', np.min)]).reset_index()
# sub_history['median_mode'] = 0.5 * sub_history['mode_m'] + 0.5 * sub_history['median_m']

sub = pd.merge(sub,sub_history,on=['link_ID','time_interval_minutes'],how='left')

sub_constacot = feature_data.loc[(feature_data.time_interval_month == 5),: ]
sub_constacot = sub_constacot.groupby(['link_ID'])[
            'travel_time'].agg([('constatic_m_1', add_constact)]).reset_index()
sub = pd.merge(sub,sub_constacot,on=['link_ID'],how='left')

# sub['speed_max'] = sub['length'] / sub['min_m']
# sub['speed_min'] = sub['length'] / sub['max_m']
sub['speed_mode'] = sub['length'] / sub['mode_m']
sub['speed_median'] = sub['length'] / sub['median_m']

# sub['120_speed'] = sub['length'] / 120.0

sub['mean_std'] = sub['mean_m']  / sub['std_m']
sub['max_min_distance'] = sub['max_m'] - sub['min_m']

sub_history_8 = feature_data.loc[(feature_data.time_interval_month == 6)&(feature_data.time_interval_begin_hour == 8),: ]
sub_history_8 = sub_history_8.groupby(['link_ID', 'time_interval_minutes'])[
            'travel_time'].agg([('median_8_', np.median)]).reset_index()

sub = pd.merge(sub,sub_history_8,on=['link_ID','time_interval_minutes'],how='left')

sub_label = np.log1p(sub.pop('travel_time'))

sub.drop(['link_ID','time_interval_begin_hour','time_interval_month','time_interval_begin','std_m','std_58','max_m','mode_m'],inplace=True,axis=1)
sub = sub.values

result = gbm.predict(sub, num_iteration=gbm.best_iteration)

travel_time = pd.DataFrame({'travel_time':list(result)})
sub_demo = pd.read_table(u'./semifinal_gy_cmp_testing_template_seg2.txt',header=None,sep=';')

sub_demo.columns = ['link_ID','date','time_interval','travel_time']
sub_demo = sub_demo.sort_values(['link_ID','time_interval']).reset_index()
del sub_demo['index']
del sub_demo['travel_time']
tt = pd.concat([sub_demo,travel_time],axis=1)
# tt = tt.fillna(0)
tt['travel_time'] = np.round(np.expm1(tt['travel_time']),6)
tt[['link_ID','date','time_interval','travel_time']].to_csv('./2017-09-16_08.txt',sep='#',index=False,header=False)
print tt[['link_ID','date','time_interval','travel_time']].shape
print tt[['link_ID','date','time_interval','travel_time']].isnull().sum()

###########################################################################################################################
# analy_data = gbm.predict(test, num_iteration=gbm.best_iteration)
# analy_data = pd.DataFrame({'pre_travel_time':list(analy_data)})
# analy_data_sub = pd.concat([analy_data,analy_data_org],axis=1)
# analy_data_sub['pre_travel_time'] = np.round(np.expm1(analy_data_sub['pre_travel_time']),6)
# analy_data_sub.to_csv('./analy_data_08.txt')
# print analy_data_sub.shape

# [901]   valid_0's rmse: 0.485679        valid_0's mape: 0.292658
# [937]   valid_0's rmse: 0.495004        valid_0's mape: 0.291705
# [942]   valid_0's rmse: 0.494127        valid_0's mape: 0.291573
# [1660]  valid_0's rmse: 0.49364           valid_0's mape: 0.291354


# 4 5 6 7
# [1879]  valid_0's rmse: 0.494375        valid_0's mape: 0.291137