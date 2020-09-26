
def randPortf(cnt):
    """
    Генерация случайного портфеля
    
    Аргументы:
    cnt - размер портфеля (кол-во инструментов)
    
    Вовращяет массив numpy с долями от единицы (от 0. до 1.). Сумма элементов даст единицу.
    
    Пример:
    randPortf(10)
    """
    import numpy as np
    res = np.exp(np.random.randn(cnt))
    res = res / res.sum()
    return res

# ------------------------------------------------------

def dohPortf(r,doh):
    """
    Доходность портфеля
    
    Аргументы:
    r - массив долей инструментов в портфеле
    doh - массив доходностей каждого инструмента в портфеле
    
    Возвращает число (суммарную доходность портфеля)
    
    Пример:
    dohPortf(r=[0.1,0.5,0.4],doh=[-0.3,0.4,0.1])
    """
    import numpy as np
    return np.matmul(doh,r)

# ------------------------------------------------------

def riskPortf(r,cov):
    """
    Риск портфеля
    
    Аргументы:
    r - массив долей инструментов в портфеле
    cov - ковариационная матрица инструментов в портфеле
    
    Возвращает число
    
    Пример:
    riskPortf(r=[0.1,0.5,0.4],cov=np.cov(X))
    """
    import numpy as np
    return np.sqrt(np.matmul(np.matmul(r,cov),r))

# ------------------------------------------------------

def koefSharp(weights,Doh,Cov):
	"""
	Расчет коэффициента Шарпа
	
	Аргументы:
	weights - веса каждого инструмента в портфеле
	Doh - массив доходностей каждого инструмента в портфеле
	Cov - ковариационная матрица инструментов в портфеле
	
	Возвращает число.
	
	"""
	import numpy as np
	return np.matmul(weights,Doh)/np.sqrt(np.matmul(np.matmul(np.transpose(weights),Cov),weights))

# ------------------------------------------------------

def portfSharpOptim(doh,cov):
    """
    Поиск оптимизированного портфеля
    (на основе https://www.mlq.ai/python-for-finance-portfolio-optimization/)
    
    Аргументы:
    doh - массив доходностей каждого инструмента в портфеле
    cov - ковариационная матрица инструментов в портфеле
    
    Возвращает массив весов портфеля
    
    Пример:
    portfSharpOptim(dohMean.values,cov.values)
    >>> array([4.07396945e-01, 2.64008207e-01, 2.39608680e-17, 2.03830008e-17,
       8.89045781e-18, 3.28594848e-01])
    """
    import numpy as np
    from scipy.optimize import minimize

    l = cov.shape[1]

    # проверка сумм долей портфеля на соотвестветствие 1-це
    def check_sum(weights): 
	    return np.sum(weights) - 1

    # отрицательный коэффицицент Шарпа
    def kSharpe(weights): 
	    return -dohPortf(weights,doh)/riskPortf(weights,cov)

    # накладываем условия
    constr = ({'type':'eq','fun':check_sum})

    # границы 
    bounds = [(0,1)] * l
    #print(bounds)

    # начальные значения
    w0 = [1.0/l] * l

    # оптимизируем
    res = minimize(kSharpe, w0, method='SLSQP', bounds=bounds, constraints=constr)

    return res.x
