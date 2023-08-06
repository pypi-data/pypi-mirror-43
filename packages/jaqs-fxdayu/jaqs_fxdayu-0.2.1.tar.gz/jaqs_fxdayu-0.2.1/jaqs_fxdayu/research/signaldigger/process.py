# encoding=utf-8
# 数据处理

import jaqs.util as jutil
import pandas as pd
import numpy as np


def _mask_df(df, mask):
    mask = mask.astype(bool)
    df[mask] = np.nan
    return df


def _mask_non_index_member(df, index_member=None):
    if index_member is not None:
        index_member = index_member.astype(bool)
        return _mask_df(df, ~index_member)
    return df


# 横截面标准化 - 对Dataframe数据
def standardize(factor_df, index_member=None):
    """
    对因子值做z-score标准化-算样本方差选择自由度为n-1
    :param index_member:
    :param factor_df: 因子值 (pandas.Dataframe类型),index为datetime, colunms为股票代码。
                      形如:
                                  　AAPL	　　　     BA	　　　CMG	　　   DAL	      LULU	　　
                        date
                        2016-06-24	0.165260	0.002198	0.085632	-0.078074	0.173832
                        2016-06-27	0.165537	0.003583	0.063299	-0.048674	0.180890
                        2016-06-28	0.135215	0.010403	0.059038	-0.034879	0.111691
                        2016-06-29	0.068774	0.019848	0.058476	-0.049971	0.042805
                        2016-06-30	0.039431	0.012271	0.037432	-0.027272	0.010902
    :return:z-score标准化后的因子值(pandas.Dataframe类型),index为datetime, colunms为股票代码。
    """

    factor_df = jutil.fillinf(factor_df)
    factor_df = _mask_non_index_member(factor_df, index_member)
    return factor_df.sub(factor_df.mean(axis=1), axis=0).div(factor_df.std(axis=1), axis=0)


# 横截面去极值 - 对Dataframe数据
def winsorize(factor_df, alpha=0.05, index_member=None):
    """
    对因子值做去极值操作
    :param index_member:
    :param alpha: 极值范围
    :param factor_df: 因子值 (pandas.Dataframe类型),index为datetime, colunms为股票代码。
                      形如:
                                  　AAPL	　　　     BA	　　　CMG	　　   DAL	      LULU	　　
                        date
                        2016-06-24	0.165260	0.002198	0.085632	-0.078074	0.173832
                        2016-06-27	0.165537	0.003583	0.063299	-0.048674	0.180890
                        2016-06-28	0.135215	0.010403	0.059038	-0.034879	0.111691
                        2016-06-29	0.068774	0.019848	0.058476	-0.049971	0.042805
                        2016-06-30	0.039431	0.012271	0.037432	-0.027272	0.010902
    :return:去极值后的因子值(pandas.Dataframe类型),index为datetime, colunms为股票代码。
    """

    def winsorize_series(se):
        q = se.quantile([alpha / 2, 1 - alpha / 2])
        se[se < q.iloc[0]] = q.iloc[0]
        se[se > q.iloc[1]] = q.iloc[1]
        return se

    factor_df = jutil.fillinf(factor_df)
    factor_df = _mask_non_index_member(factor_df, index_member)
    return factor_df.apply(lambda x: winsorize_series(x), axis=1)


# 横截面去极值 - 对Dataframe数据
def mad(factor_df, index_member=None):
    """
    对因子值做去极值操作
    :param index_member:
    :param factor_df: 因子值 (pandas.Dataframe类型),index为datetime, colunms为股票代码。
                      形如:
                                  　AAPL	　　　     BA	　　　CMG	　　   DAL	      LULU	　　
                        date
                        2016-06-24	0.165260	0.002198	0.085632	-0.078074	0.173832
                        2016-06-27	0.165537	0.003583	0.063299	-0.048674	0.180890
                        2016-06-28	0.135215	0.010403	0.059038	-0.034879	0.111691
                        2016-06-29	0.068774	0.019848	0.058476	-0.049971	0.042805
                        2016-06-30	0.039431	0.012271	0.037432	-0.027272	0.010902
    :return:去极值后的因子值(pandas.Dataframe类型),index为datetime, colunms为股票代码。
    """

    def _mad(series):
        if series.dropna().size==0:
            return series
        median = series.median()
        tmp = (series - median).abs().median()
        return series.clip(median - 5 * tmp, median + 5 * tmp)

    factor_df = jutil.fillinf(factor_df)
    factor_df = _mask_non_index_member(factor_df, index_member)
    return factor_df.apply(lambda x: _mad(x), axis=1)


# 横截面排序并归一化
def rank_standardize(factor_df, index_member=None):
    """
    输入因子值, 将因子用排序分值重构，并处理到0-1之间(默认为升序——因子越大 排序分值越大(越好)
        :param index_member:
        :param factor_df: 因子值 (pandas.Dataframe类型),index为datetime, colunms为股票代码。
                      形如:
                                  　AAPL	　　　     BA	　　　CMG	　　   DAL	      LULU	　　
                        date
                        2016-06-24	0.165260	0.002198	0.085632	-0.078074	0.173832
                        2016-06-27	0.165537	0.003583	0.063299	-0.048674	0.180890
                        2016-06-28	0.135215	0.010403	0.059038	-0.034879	0.111691
                        2016-06-29	0.068774	0.019848	0.058476	-0.049971	0.042805
                        2016-06-30	0.039431	0.012271	0.037432	-0.027272	0.010902

    :return: 排序重构后的因子值。 取值范围在0-1之间
    """
    factor_df = jutil.fillinf(factor_df)
    factor_df = _mask_non_index_member(factor_df, index_member)
    return jutil.rank_with_mask(factor_df, axis=1, normalize=True)


# 将因子值加一个极小的扰动项,用于对quantile做区分
def get_disturbed_factor(factor_df):
    """
    将因子值加一个极小的扰动项,用于对quantile区分
    :param factor_df: 因子值 (pandas.Dataframe类型),index为datetime, colunms为股票代码。
                      形如:
                                  　AAPL	　　　     BA	　　　CMG	　　   DAL	      LULU	　　
                        date
                        2016-06-24	0.165260	0.002198	0.085632	-0.078074	0.173832
                        2016-06-27	0.165537	0.003583	0.063299	-0.048674	0.180890
                        2016-06-28	0.135215	0.010403	0.059038	-0.034879	0.111691
                        2016-06-29	0.068774	0.019848	0.058476	-0.049971	0.042805
                        2016-06-30	0.039431	0.012271	0.037432	-0.027272	0.010902

    :return: 重构后的因子值,每个值加了一个极小的扰动项。
    """
    return factor_df + np.random.random(factor_df.shape) / 1000000000


# 行业、市值中性化 - 对Dataframe数据
def neutralize(factor_df,
               group,
               float_mv=None,
               index_member=None):
    """
    对因子做行业、市值中性化
    :param index_member:
    :param group:　行业分类(pandas.Dataframe类型),index为datetime, colunms为股票代码
    :param factor_df: 因子值 (pandas.Dataframe类型),index为datetime, colunms为股票代码。
                      形如:
                                  　AAPL	　　　     BA	　　　CMG	　　   DAL	      LULU	　　
                        date
                        2016-06-24	0.165260	0.002198	0.085632	-0.078074	0.173832
                        2016-06-27	0.165537	0.003583	0.063299	-0.048674	0.180890
                        2016-06-28	0.135215	0.010403	0.059038	-0.034879	0.111691
                        2016-06-29	0.068774	0.019848	0.058476	-0.049971	0.042805
                        2016-06-30	0.039431	0.012271	0.037432	-0.027272	0.010902
    :param float_mv: 流通市值因子(pandas.Dataframe类型),index为datetime, colunms为股票代码．为空则不进行市值中性化
    :return: 中性化后的因子值(pandas.Dataframe类型),index为datetime, colunms为股票代码。
    """
    def drop_nan(s):
        return s[s != "nan"]

    def _ols_by_numpy(x, y):
        m = np.linalg.lstsq(x, y)[0]
        resid = y - (x@m)
        return resid

    def _generate_cross_sectional_residual(data):
        for _, X in data.groupby(level=0):
            signal = X.pop("signal")
            X = pd.concat([X, pd.get_dummies(X.pop("industry"))], axis=1)
            signal = pd.Series(_ols_by_numpy(X.values, signal), index=signal.index, name=signal.name)
            yield signal

    data = []

    # 用于恢复原先的索引和列
    origin_factor_columns = factor_df.columns
    origin_factor_index = factor_df.index

    factor_df = jutil.fillinf(factor_df)  # 调整非法值
    factor_df = _mask_non_index_member(factor_df, index_member)  # 剔除非指数成份股
    factor_df = factor_df.dropna(how="all").stack().rename("signal")  # 删除全为空的截面
    data.append(factor_df)

    # 获取对数流动市值，并去极值、标准化。市值类因子不需进行这一步
    if float_mv is not None:
        float_mv = standardize(mad(np.log(float_mv), index_member=index_member), index_member).stack().rename("style")
        data.append(float_mv)

    # 行业
    industry_standard = drop_nan(group.stack()).rename("industry")
    data.append(industry_standard)

    data = pd.concat(data,axis=1).dropna()
    residuals = pd.concat(_generate_cross_sectional_residual(data)).unstack()

    # 恢复在中性化过程中剔除的行和列
    residuals.reindex(index=origin_factor_index,columns=origin_factor_columns)
    return residuals.reindex(index=origin_factor_index,columns=origin_factor_columns)
