"""
수학 계산 보고 라이브러리 모듈
실제 계산은 __math에서 하고, 보고를 중심으로 코드작성해라.

===== 출처 =====
수학용어 영문표기
https://www.myenglishteacher.eu/blog/math-terms-and-symbols/

===== 사용법 =====
import sys
sys.path.append('/Users/sambong/p/lib')
import __math as mth
"""
from __lib__ import *


# 오픈 라이브러리
import pandas as pd
import math



def 시리즈간_나누기_계산후_신규컬럼으로_추가(df, numerator_col, denominator_col, result_col):
    df1 = df[ df[denominator_col] != 0 ]
    s3 = df1[numerator_col].div( df1[denominator_col] )
    s3 = s3.rename(result_col)

    if (result_col in list(df.columns)) == True:
        df.update(s3)
    else:
        df[new_col_name] = 0
        print('컬럼 신규 추가')
    return df
"""
============================== 보고 ==============================
"""
def portion_ratio(n1, n2, portion명='구성비', ratio명='비율', 소수점자릿수=4, 퍼센트자릿수=1, dbgon=False):
    print('\n' + '='*60 + dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3]))
    inputs = dbg.inputs(inspect.currentframe(), dbgon=True)
    """
    두 수 간의 구성비, 비율을 보고한다. (비중은 중력값을 고려한 값이므로 사용하지 않는다.)
    portion : 구성비
    ratio : 비율
    p : 퍼센트
    portion_p = 구성비 * 100
    ratio_p = 비율 * 100
    """
    portion = n1 / (n1 + n2)
    ratio = n1 / n2

    rpt = {
        portion명:round(portion, 소수점자릿수),
        portion명+'p':str(round(portion *100, 퍼센트자릿수)) + '%',
        ratio명:round(ratio, 소수점자릿수),
        ratio명+'p':str(round(ratio *100, 퍼센트자릿수)) + '%',
    }
    if dbgon == True:
        pp.pprint({'결과보고':rpt})
    return rpt

def portion_in_pvt(pvt, set_col):
    print('\n' + '='*60 + dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3]))
    #inputs = dbg.inputs(inspect.currentframe(), dbgon=True)
    """
    set_col : 전체집합. 분모가 될 기준 값.
    """
    start_t = datetime.now()
    cols = list(pvt.columns)
    for col in cols:
        pvt[col] = pvt[col] / pvt[set_col]

    print('\n 구성비_계산시간 : {}'.format( (datetime.now()-start_t).total_seconds() ))
    print('\n pvt :\n\n{}'.format(pvt))
    return pvt

"""
============================== 미분 ==============================
"""
def growth_rate(a2=-4, a1=-1, test=False):
    print('\n' + '='*60 + dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3]))
    inputs = dbg.inputs(insp_currframe=inspect.currentframe(), dbgon=True)
    """
    ===== 개념 =====
    증가율 : growth_rate
    증감율 : change_rate
    r = (a2 - a1) / a1
    ===== 교훈 =====
    pd.pct_change()를 사용할 것.
    ===== 사용법 =====
    mth.growth_rate(a2=-4, a1=-1, test=True)
    ===== 용어정의 =====
    a1 : t1에서의 값
    a2 : t2에서의 값
    """
    c = (a2 - a1) / a1
    print('\n 증가율 : {}\n'.format(c))

    if test == True:
        c0 = (a2 - a1) / math.fabs(a1)
        print('\n 주식용_증가율 : {}\n'.format(c0))

    return c, c0


def diffcoff():
    print('\n' + '='*60 + dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3]))
    inputs = dbg.inputs(insp_currframe=inspect.currentframe(), dbgon=True)
    """
    diffcoff : differential coefficient

    ===== 개념 =====
    미분, derivative, 微分 또는 도함수, 導函數
    - 함숫값의 변화량과 독립 변숫값의 변화량의 비
    동사로서의 미분 : differentiation = 이러한 극한이나 도함수를 구하는 일 즉 미분법

    미분 또는 미분 계수, 微分係數, differential coefficient,
    또는
    순간변화율 瞬間變化率, instantaneous rate of change
    평균 변화율의 극한

    변곡(變曲)점 : Inflection point
    inflection point, flex, inflection, inflexion(British)
    2차 미분계수/도함수
    곡률, 曲率, curvature
    """

"""
============================== 산수 ==============================
"""
def divide(a2=-4, a1=-1, test=False):
    print('\n' + '='*60 + dbg.whoami(sys.modules[__name__].__file__, inspect.stack()[0][3]))
    inputs = dbg.inputs(insp_currframe=inspect.currentframe(), dbgon=True)
    from fractions import Fraction
    """나누기
    """
    c1 = Fraction(numerator=a2, denominator=a1)
    print('\n c1 : {}\n'.format(c1))

    c = a2 / a1
    print('\n c : {}\n'.format(c))
