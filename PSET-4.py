
import pandas as pd
import numpy as np
from scipy import stats

def feedback_analysis(df_feedback):
    #used paired t test
    ios = df_feedback['product'] == 'iOS'
    andriod = df_feedback['product'] == 'Android'
    condition_ios = df_feedback.loc[ios, 'feedback_score'].to_numpy()
    condition_andriod = df_feedback.loc[andriod, 'feedback_score'].to_numpy()
    np_array = np.array([condition_ios, condition_andriod])
    t_statistic, p_value = stats.ttest_rel(np_array[0], np_array[1])
    if p_value > 0.05:
        difference = 'NO'
    else : difference = 'YES'
    return difference, p_value

def sales_analysis(df_sales):
    #use one-tailed t test
    before = df_sales['date'] < '2023-03-01'
    after = df_sales['date'] > '2023-03-31'
    condition_before = df_sales.loc[before, 'sales'].to_numpy()
    condition_after = df_sales.loc[after, 'sales'].to_numpy()
    t_statistic, p_value = stats.ttest_ind(condition_before, condition_after, equal_var = False)
    if t_statistic > 0:
        p_value /= 2
    if p_value > 0.05:
        difference = 'NO'
    else : difference = 'YES'
    return difference, p_value

def seasonal_analysis(df_sales):
    #two-tailed t test
    summer = [6, 7, 8]
    winter = [12,1,2]
    summer_sales = df_sales['date'].dt.month.isin(summer)
    winter_sales = df_sales['date'].dt.month.isin(winter)

    condition_winter = df_sales.loc[winter_sales, 'sales'].to_numpy()
    condition_summer = df_sales.loc[summer_sales, 'sales'].to_numpy()
    t_statistic, p_value = stats.ttest_ind(condition_winter, condition_summer, equal_var = False)
    if p_value > 0.05:
        difference = 'NO'
    else : difference = 'YES'
    return difference, p_value

def consistency_analysis(df_feedback):
    #Use 1-way anova
    jan = df_feedback.date.dt.month == 1
    may = df_feedback.date.dt.month == 5
    sept = df_feedback.date.dt.month == 9
    dec = df_feedback.date.dt.month == 12

    f_stat, p_value = stats.f_oneway(jan, may, sept, dec)
    if p_value > 0.05:
        consistency = 'YES'
    else : consistency = 'NO'
    return consistency, p_value

def corr_analysis(df_feedback, df_sales):
    #use one-way t test
    df = pd.merge(left = df_feedback, right = df_sales, on = ['date', 'product'])
    grouped_ = [df[df.date.dt.month == month] for month in [1,2,3,4,5,6,7,8,9,10,11,12]]
    grouped_ = df.groupby(df.date.dt.month)['feedback_score'].agg(list)
    grouped_ = df.groupby(df.date.dt.month)['feedback_score'].mean().sort_values()

    low_scores = grouped_[0:6]
    low_scores = low_scores.index
    high_scores = grouped_[6:12]
    high_scores = high_scores.index
    
    high_scores_df = df['date'].dt.month.isin(high_scores)
    low_scores_df = df['date'].dt.month.isin(low_scores)

    condition_high = df.loc[high_scores_df, 'sales'].to_numpy()
    condition_low = df.loc[low_scores_df, 'sales'].to_numpy()
    t_statistic, p_value = stats.ttest_ind(condition_high, condition_low, equal_var = False)
    if t_statistic > 0:
        p_value /= 2
    if p_value > 0.05:
        corr = 'NO'
    else : corr = 'YES'
    return corr, p_value

df_cf = pd.read_csv("customer_feedback.csv")
df_sd = pd.read_csv("sales_data.csv")
df_sd.date= pd.to_datetime(df_sd.date)
df_cf.date= pd.to_datetime(df_cf.date)

difference, p_value = feedback_analysis(df_cf)
difference, p_value = sales_analysis(df_sd)
difference, p_value = seasonal_analysis(df_sd)
consistency, p_value = consistency_analysis(df_cf)
corr, p_value = corr_analysis(df_cf, df_sd)


