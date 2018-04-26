# This model is based on the kernel of  Pranav Pandya and andy harless.
#       https://www.kaggle.com/pranav84/single-lightgbm-in-r-with-75-mln-rows-lb-0-9690
#       https://www.kaggle.com/aharless/try-pranav-s-r-lgbm-in-python/code
# I modified code to make it easier for me
# The actual changed values are the parameters only. I focused on parameter tuning
# num_leaves :  7  ->  9
# max_depth  :  4  ->  5
# subsample  : 0.7 -> 0.9


# This is the first version and will be performing additional data sampling and parameter tuning.


import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split # for validation 
import lightgbm as lgb
import gc # memory 
from datetime import datetime # train time checking
import numpy as np
import zipfile


start = datetime.now()
VALIDATE = True
RANDOM_STATE = 50
VALID_SIZE = 0.3
MAX_ROUNDS = 1000
EARLY_STOP = 50
OPT_ROUNDS = 700
#skiprows = range(1,109903891)
skiprows = range(1,9308568)
#skiprows = range(1,184903890-4000000)
#nrows = 75000000
nrows = 45000000
output_filename = '/home/burke/song/v6/submission_v6_09.csv'
model_name = '/home/burke/song/v6/modelv6_9.txt'


dtypes = {
        'ip'            : 'uint32',
        'app'           : 'uint16',
        'device'        : 'uint16',
        'os'            : 'uint16',
        'channel'       : 'uint16',
        'is_attributed' : 'uint8',
        'click_id'      : 'uint32'
        }



train_cols = ['ip','app','device','os', 'channel', 'click_time', 'is_attributed']
with zipfile.ZipFile('/home/burke/song/s1.zip', 'r') as myzip:
    path = myzip.open('mnt/ssd/kaggle-talkingdata2/competition_files/train.csv')
df = pd.read_csv(path, iterator=True, chunksize=10000, dtype=dtypes, usecols=train_cols)
train_df = pd.concat([chunk[chunk['click_time'].str.contains("2017-11-09")] for chunk in df])
del df
del path
scale_num = round(train_df.is_attributed.value_counts().reset_index()['is_attributed'][0]/train_df.is_attributed.value_counts().reset_index()['is_attributed'][1], 3)
len_train = len(train_df)
gc.collect()

def click(df):
    new_feature = 'nextClick'
    D=2**26
    df['category'] = (df['ip'].astype(str) + "_" + df['app'].astype(str) + "_" + df['device'].astype(str) + "_" + df['os'].astype(str)).apply(hash) % D
    click_buffer= np.full(D, 3000000000, dtype=np.uint32)
    df['epochtime']= df['click_time'].astype(np.int64) // 10 ** 9
    next_clicks= []
    for category, t in zip(reversed(df['category'].values), reversed(df['epochtime'].values)):
        next_clicks.append(click_buffer[category]-t)
        click_buffer[category]= t
    del(click_buffer)
    QQ= list(reversed(next_clicks))
    df.drop(['epochtime','category','click_time'], axis=1, inplace=True)
    df[new_feature] = pd.Series(QQ).astype('float32')
    #df[new_feature+'_shift'] = df[new_feature].shift(+1).values
    #newname = [new_feature, new_feature+'_shift']
    newname = [new_feature, new_feature]
    return df, newname
def do_next_prev_Click( df,agg_suffix, agg_type='float32'):
    print('Extracting new features...')
    
    df['hour'] = pd.to_datetime(df.click_time).dt.hour.astype('int8')
    df['day'] = pd.to_datetime(df.click_time).dt.day.astype('int8')
    
    #### New added
    df['minute'] = pd.to_datetime(df.click_time).dt.minute.astype('int8')
    df['second'] = pd.to_datetime(df.click_time).dt.second.astype('int8')
    print("Extracting {0} time calculation features...".format(agg_suffix))
    
    GROUP_BY_NEXT_CLICKS = [
    {'groupby': ['ip', 'app', 'device', 'os', 'channel']},
    {'groupby': ['ip', 'os', 'device']},
    {'groupby': ['ip', 'app']},
    {'groupby': ['ip', 'channel']},
    {'groupby': ['ip', 'os', 'device', 'app']}
    ]
    add_p = []
    # Calculate the time to next click for each group
    for spec in GROUP_BY_NEXT_CLICKS:
    
       # Name of new feature
        new_feature = '{}_{}'.format('_'.join(spec['groupby']),agg_suffix)    
    
        # Unique list of features to select
        all_features = spec['groupby'] + ['click_time']

        # Run calculation
        print("Grouping by {0}, and saving time to {1} in: {2}".format(spec['groupby'], agg_suffix, new_feature))
        if agg_suffix=="nextClick":
            df[new_feature] = (df[all_features].groupby(spec[
            'groupby']).click_time.shift(-1) - df.click_time).dt.seconds.astype(agg_type)
        elif agg_suffix== "prevClick":
            df[new_feature] = (df.click_time - df[all_features].groupby(spec[
                'groupby']).click_time.shift(+1) ).dt.seconds.astype(agg_type)
        gc.collect()
        add_p.append(new_feature)
    df.drop(['hour', 'day', 'minute', 'second'], axis=1, inplace=True)
    return df, add_p
def group_by_click(lis_p, data):
    print('group by...')
    newname = '{}_click_time_gap'.format('_'.join(lis_p))
    all_p = lis_p[:]
    all_p.append('click_time')
    data[newname] = data[all_p].groupby(by=lis_p).click_time.transform(lambda x: x.diff().shift(-1)).dt.seconds
    data[newname] = data[newname].fillna(-1)
    print('merge...')
    return data, newname
def group_by(lis_p, select_p, data, fuc, agg_type='uint32', show_max=False):
    print('group by...')
    newname = '{}'.format('_'.join(lis_p))
    all_p = lis_p[:]
    all_p.append(select_p)
    if fuc == 'cumcount':
        newname = newname+"_cumcountBY_"+select_p
        gp = data[all_p].groupby(by=lis_p)
        gp = gp[select_p].cumcount()
        print('merge...')
        data[newname] = gp.values
        del gp
        if show_max:
            print( newname + " max value = ", data[newname].max() )
        data[newname] = data[newname].astype(agg_type)
        return data, newname
    elif fuc == 'count':
        newname = newname+"_countBY"
        gp = data[lis_p][lis_p].groupby(lis_p).size().rename(newname).to_frame().reset_index()
        print('merge...')
        data = data.merge(gp, on=lis_p, how='left')
        del gp
        if show_max:
            print( newname + " max value = ", data[newname].max() )
        data[newname] = data[newname].astype(agg_type)
        return data, newname
    elif fuc == 'countuniq':
        newname = newname+"_countuniqBY_"+select_p
        gp = data[all_p].groupby(by=lis_p)
        gp = gp[select_p].nunique().reset_index().rename(index=str, columns={select_p: newname})
        print('merge...')
        data = data.merge(gp, on=lis_p, how='left')
        del gp
        if show_max:
            print( newname + " max value = ", data[newname].max() )
        data[newname] = data[newname].astype(agg_type)
        return data, newname
    elif fuc == 'var':
        newname = newname+"_varBY_"+select_p
        gp = data[all_p].groupby(by=lis_p)
        gp = gp[select_p].var().reset_index().rename(index=str, columns={select_p: newname})
        print('merge...')
        data = data.merge(gp, on=lis_p, how='left')
        del gp
        if show_max:
            print( newname + " max value = ", data[newname].max() )
        data[newname] = data[newname].astype(agg_type)
        return data, newname
def prep_data( df ):
    print('data prep...')
    df['click_time'] = pd.to_datetime(df['click_time'])
    df, tmp1 = group_by_click(['ip', 'device', 'app'],df)
    gc.collect()
    df, tmp2 = group_by_click(['ip', 'channel'],df)
    gc.collect()
    df, lis_add_p1 = do_next_prev_Click(df, agg_suffix='nextClick', agg_type='float32')
    gc.collect()
    df, lis_add_p2 = do_next_prev_Click(df, agg_suffix='prevClick', agg_type='float32')
    gc.collect()
    print('data prep...')
    df['hour'] = df['click_time'].dt.hour.astype('uint8')
    df['minute'] = df['click_time'].dt.minute.astype('uint8')
    df['second'] = df['click_time'].dt.second.astype('uint8')
    gc.collect()
    df, tmp3 = group_by(['app','channel', 'hour','minute', 'second' ], 'device', df, 'count', agg_type = 'uint16', show_max=True)
    #df, tmp4 = group_by(['ip','device', 'hour', 'minute' ], 'app', df, 'count', agg_type = 'uint16', show_max=True)
    print('data drop...')
    #df.drop(['second'], axis=1, inplace=True)
    #df.drop(['minute'], axis=1, inplace=True)
    gc.collect()
    #group by
    df, tmp5 = group_by(['ip'], 'channel', df, 'countuniq', agg_type = 'uint8', show_max=True)
    gc.collect()
    df, tmp6 = group_by(['ip'], 'app', df, 'countuniq', agg_type = 'uint8', show_max=True)
    gc.collect()
    df, tmp7 = group_by(['ip','os','device'], 'app', df, 'countuniq', agg_type = 'uint8', show_max=True)
    gc.collect()
    df, tmp8 = group_by(['app'], 'channel', df, 'countuniq', agg_type = 'uint8', show_max=True)
    gc.collect()
    df, tmp9 = group_by(['ip'], 'os', df, 'cumcount', show_max=True)
    gc.collect()
    df, lis = click(df)
    gc.collect()
    df, tmp10 = group_by(['ip','app'], 'os', df, 'countuniq', agg_type = 'uint16', show_max=True)
    gc.collect()
    df, tmp11 = group_by(['ip', 'device', 'os'], 'app', df, 'cumcount', show_max=True)
    gc.collect()
    df, tmp12 = group_by(['ip', 'device', 'app'], 'os', df, 'count', show_max=True)
    gc.collect()
    df, tmp13 = group_by(['ip', 'hour'], 'os', df, 'count',  show_max=True)
    gc.collect()
    df, tmp14 = group_by(['ip', 'app'], 'os', df, 'count', show_max=True)
    gc.collect()
    df, tmp15 = group_by(['ip', 'os', 'app'], 'channel', df, 'count', show_max=True)
    gc.collect()
    df, tmp16 = group_by(['ip', 'hour', 'device'], 'channel', df, 'count', show_max=True)
    gc.collect()
    df, tmp17 = group_by(['ip', 'app', 'os'], 'hour', df, 'var', agg_type='float32', show_max=True)
    gc.collect()
    df, tmp18 = group_by(['ip', 'channel'], 'hour', df, 'var', agg_type='float32', show_max=True)
    gc.collect()
    df.drop( ['ip'], axis=1, inplace=True )
    gc.collect()
    add_p = [tmp1,tmp2,tmp3,tmp5,tmp6,tmp7,tmp8,tmp9,tmp10,tmp11,tmp12,tmp13,tmp14,tmp15,tmp16,tmp17,tmp18]
    for i in lis:
        add_p.append(i)
    for j in lis_add_p1:
        add_p.append(j)
    for j in lis_add_p2:
        add_p.append(j)
    return df, add_p

train_df, app_p = prep_data(train_df)
gc.collect()

params = {
          'boosting_type': 'gbdt',
          'objective': 'binary',
          'metric':'auc',
          'learning_rate': 0.1,
          'num_leaves': 7,  # we should let it be smaller than 2^(max_depth)
          'max_depth':3,#  -1 means no limit
          'min_child_samples': 100,  # Minimum number of data need in a child(min_data_in_leaf)
          'max_bin': 100,  # Number of bucketed bin for feature values
          'subsample': 0.7,  # Subsample ratio of the training instance.
          'subsample_freq': 1,  # frequence of subsample, <=0 means no enable
          'colsample_bytree': 0.9,  # Subsample ratio of columns when constructing each tree.
          'min_child_weight': 0,  # Minimum sum of instance weight(hessian) needed in a child(leaf)
          'min_split_gain': 0,  # lambda_l1, lambda_l2 and min_gain_to_split to regularization
          'subsample_for_bin': 200000,  # Number of samples for constructing bin
          'nthread': 8,
          'verbose': 0,
          'scale_pos_weight':scale_num, # because training data is extremely unbalanced 
         }

target = 'is_attributed'
categorical = ['app', 'device', 'os', 'channel', 'hour','minute','second']
app_p.extend(categorical)
predictors = app_p


if VALIDATE:

    train_df, val_df = train_test_split(train_df, test_size=VALID_SIZE, random_state=RANDOM_STATE, shuffle=True )
    dtrain = lgb.Dataset(train_df[predictors].values, 
                         label=train_df[target].values,
                         feature_name=predictors,
                         categorical_feature=categorical)
    del train_df
    gc.collect()

    dvalid = lgb.Dataset(val_df[predictors].values,
                         label=val_df[target].values,
                         feature_name=predictors,
                         categorical_feature=categorical)
    del val_df
    gc.collect()

    evals_results = {}

    model = lgb.train(params, 
                      dtrain, 
                      valid_sets=[dtrain, dvalid], 
                      valid_names=['train','valid'], 
                      evals_result=evals_results, 
                      num_boost_round=MAX_ROUNDS,
                      early_stopping_rounds=EARLY_STOP,
                      verbose_eval=50, 
                      feval=None)

    del dvalid

else:

    gc.collect()
    dtrain = lgb.Dataset(train_df[predictors].values, label=train_df[target].values,
                          feature_name=predictors,
                          categorical_feature=categorical
                          )
    del train_df
    gc.collect()

    evals_results = {}

    model = lgb.train(params, 
                      dtrain, 
                      valid_sets=[dtrain], 
                      valid_names=['train'], 
                      evals_result=evals_results, 
                      num_boost_round=OPT_ROUNDS,
                      verbose_eval=50,
                      feval=None)
    
del dtrain
gc.collect()
#import matplotlib.pyplot as plt
#f, ax = plt.subplots(figsize=[10,10])
#lgb.plot_importance(model, ax=ax, max_num_features=len(predictors))
#plt.title("Light GBM Feature Importance")
#plt.savefig('feature_import.png')

test_cols = ['ip','app','device','os', 'channel', 'click_time', 'click_id']
with zipfile.ZipFile('/home/burke/song/a1.zip', 'r') as myzip:
    path1 = myzip.open('test.csv')
test_df = pd.read_csv(path1, dtype=dtypes, usecols=test_cols)
test_df, app_p2 = prep_data(test_df)
del path1
gc.collect()
model.save_model(model_name)
sub = pd.DataFrame()
sub['click_id'] = test_df['click_id']
sub['is_attributed'] = model.predict(test_df[predictors])
sub.to_csv(output_filename, index=False, float_format='%.9f')

print('=='*35)
print('============================ Final Report ============================')
print('=='*35)
print(datetime.now(), '\n')
print('{:^17} : {:}'.format('train time', datetime.now()-start))
print('{:^17} : {:}'.format('output file', output_filename))
print('{:^17} : {:.5f}'.format('train auc', model.best_score['train']['auc']))
if VALIDATE:
    print('{:^17} : {:.5f}\n'.format('valid auc', model.best_score['valid']['auc']))
    print('{:^17} : {:}\n{:^17} : {}\n{:^17} : {}'.format('VALIDATE', VALIDATE, 'VALID_SIZE', VALID_SIZE, 'RANDOM_STATE', RANDOM_STATE))
print('{:^17} : {:}\n{:^17} : {}\n{:^17} : {}\n'.format('MAX_ROUNDS', MAX_ROUNDS, 'EARLY_STOP', EARLY_STOP, 'OPT_ROUNDS', model.best_iteration))
print('{:^17} : {:}\n{:^17} : {}\n'.format('skiprows', skiprows, 'nrows', nrows))
print('{:^17} : {:}\n{:^17} : {}\n'.format('variables', predictors, 'categorical', categorical))
print('{:^17} : {:}\n'.format('model params', params))
print('=='*35)