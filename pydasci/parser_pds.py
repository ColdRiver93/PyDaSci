from rply import ParserGenerator
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.api import ExponentialSmoothing
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.mixture import GaussianMixture


SOL = {}
class Parser():
 def __init__(self):
    self.pg = ParserGenerator(['ADD','COLON','PREDICTION','CLUSTERING','FLOAT','STATS',
    'PLOT','C_PLOT', 'SENTENCE','PRINT', 'FORECAST', 'VAR', 'EQUAL', 'INT', 'OPEN_BRA',
    'CLOSE_BRA' ,'OPEN_PAREN', 'CLOSE_PAREN','SEMI_COLON', 'COMA' ,'METHOD', 'BOOLEAN',
    'TYPE_A'])
 def parse(self):
    @self.pg.production('main : main assignment')
    @self.pg.production('main : assignment')
    def main_p(p):
        return SOL
    
    @self.pg.production('assignment : STATS VAR SEMI_COLON')
    def statistics(p):
        print("\nVariable's '", p[1].getstr(), "' Statistics: ")
        ts = SOL[p[1].getstr()]
        print(stats.describe(ts))
        print('')
        return 'PRINTED ' + p[1].getstr() + ' STATISTICS'
    
    @self.pg.production('assignment : PLOT ts SENTENCE SEMI_COLON')
    def plot_ts(p):
        plt.figure(figsize=(12,6), dpi=100)
        plt.plot(range(1,len(p[1])+1), p[1], color = 'blue', label = 'Time Serie')
        plt.legend(fontsize = 20)
        plt.title(p[2].getstr()[1:-1], fontsize = 28)
        plt.xlabel('Sample',fontsize = 24)
        plt.ylabel('Value',fontsize = 24)
        plt.tick_params(labelsize=20)
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.show()
    @self.pg.production('assignment : PLOT VAR SENTENCE SEMI_COLON')
    def plot_var(p):
        plt.figure(figsize=(12,6), dpi=100)
        plt.plot(range(1,len(SOL[p[1].getstr()])+1), SOL[p[1].getstr()], color = 'blue', label = 'Time Serie')
        plt.legend(fontsize = 20)
        plt.title(p[2].getstr()[1:-1], fontsize = 28)
        plt.xlabel('Sample',fontsize = 24)
        plt.ylabel('Value',fontsize = 24)
        plt.tick_params(labelsize=20)
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.show()
    @self.pg.production('assignment : C_PLOT plot_args SENTENCE SEMI_COLON')
    def plot_c(p):
        p_mat = [i[1] for i in p[1]]
        p_name = [i[0] for i in p[1]]

        plt.figure(figsize=(12,6), dpi=100)
        for i in range(len(p_mat)):
            plt.plot(range(1,len(p_mat[i])+1), p_mat[i], label = p_name[i])
        plt.legend(fontsize = 20)
        plt.title(p[2].getstr()[1:-1], fontsize = 28)
        plt.xlabel('Sample',fontsize = 24)
        plt.ylabel('Value',fontsize = 24)
        plt.tick_params(labelsize=20)
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()
        plt.show()
    @self.pg.production('plot_args : plot_args VAR')
    @self.pg.production('plot_args : VAR')
    def p_args(p):
        if len(p) == 1:
            return [[p[0].getstr(), SOL[p[0].getstr()].tolist()]]
        elif len(p) == 2:
            return p[0] + [[p[1].getstr(),SOL[p[1].getstr()].tolist()]]
    @self.pg.production('assignment : PRINT SENTENCE SEMI_COLON')
    @self.pg.production('assignment : PRINT VAR SEMI_COLON')
    def print_s(p):
        if p[1].gettokentype() == 'VAR':
            print(SOL[p[1].getstr()])
        if p[1].gettokentype() == 'SENTENCE':
            print(p[1].getstr()[1:-1])
        return 'PRINT: DONE'
        
    @self.pg.production('assignment : VAR EQUAL program')
    @self.pg.production('assignment : VAR EQUAL ts SEMI_COLON')
    @self.pg.production('assignment : VAR EQUAL matrix SEMI_COLON')
    @self.pg.production('assignment : VAR EQUAL partition SEMI_COLON')
    @self.pg.production('assignment : VAR EQUAL extension SEMI_COLON')
    def assignment(p):
        x= p[0].getstr()
        SOL[p[0].getstr()] = p[2]
        a = p[0].getstr() + '=' 'ASSIGNED'
        return a
    @self.pg.production('program : FORECAST VAR INT SEMI_COLON')
    def forecasting(p):
        return SOL[p[1].getstr()].forecast(int(p[2].getstr()))

        
    @self.pg.production('program : METHOD OPEN_PAREN VAR args CLOSE_PAREN SEMI_COLON')
    def program(p):
        if p[0].getstr() == 'SARIMA':
            return SARIMA(SOL[p[2].getstr()], p[3]).eval()
        elif p[0].getstr() == 'EXPSM':
            return EXPSM(SOL[p[2].getstr()], p[3]).eval()
        else:
            print(p, 'NO METHOD')    
            
            
    @self.pg.production('program : CLUSTERING OPEN_PAREN VAR number CLOSE_PAREN SEMI_COLON')
    def program(p):
        if p[0].getstr() == 'KMEANS':
            km_model = KMeans(n_clusters=p[3])
            km_model.fit(SOL[p[2].getstr()])
            return km_model
        elif p[0].getstr() == 'GAUSSIAN':
            g_model = GaussianMixture(n_components=p[3], reg_covar = 1e-3)
            g_model.fit(SOL[p[2].getstr()])
            return g_model
        else:
            print(p, 'NO METHOD')  
    
    @self.pg.production('program : CLUSTERING OPEN_PAREN number CLOSE_PAREN SEMI_COLON')
    def program(p):
        if p[0].getstr() == 'AGGLOMERATIVE':
            ag_model = AgglomerativeClustering(n_clusters=p[2])
            return ag_model
        elif p[0].getstr() == 'SPECTRAL':
            sp_model = SpectralClustering(n_clusters=p[2])
            return sp_model
        else:
            print(p, 'NO METHOD')
    
    @self.pg.production('program : PREDICTION VAR VAR SEMI_COLON')
    def prediction(p):
        if p[0].getstr() == 'PREDICT':
            return SOL[p[1].getstr()].predict(SOL[p[2].getstr()])
        elif p[0].getstr() == 'PREDICT2':    
            return SOL[p[1].getstr()].fit_predict(SOL[p[2].getstr()])
    
        
    
    @self.pg.production('args : pdq spdq')
    def args(p):
        if p != []:
            return [p[0], p[1]]
        else:
            return None
            
    @self.pg.production('args : trend damped seasonal s_periods')
    def args(p):
        if p != []:
            return [p[0], p[1], p[2], p[3]]
        else:
            return None
            
    @self.pg.production('pdq : OPEN_PAREN INT COMA INT COMA INT CLOSE_PAREN')  
    def pdq(p):
        v_pdq = (int(p[1].getstr()), int(p[3].getstr()), int(p[5].getstr()))
        return v_pdq
        
    @self.pg.production('spdq : OPEN_PAREN INT COMA INT COMA INT COMA INT CLOSE_PAREN')
    def spdq(p):
        v_spdq = (int(p[1].getstr()), int(p[3].getstr()), int(p[5].getstr()), int(p[3].getstr()))
        return v_spdq
    
    @self.pg.production('number : INT')
    @self.pg.production('number : FLOAT')
    def number(p):
        if p[0].gettokentype() == 'INT':
            return int(p[0].getstr())
        elif p[0].gettokentype() == 'FLOAT':
            return float(p[0].getstr())
    
    @self.pg.production('cn : ')
    @self.pg.production('cn : COMA number cn')
    def cn(p):
        if p != []:
            b = [p[1]] + p[2]
            return b
        else:
            return []
    @self.pg.production('ts : OPEN_BRA number cn CLOSE_BRA')
    def ts(p):
        if p != []:
            list = [p[1]] + p[2]
            return list
            
            
    @self.pg.production('ts_c : ')
    @self.pg.production('ts_c : COMA ts ts_c')
    def ts_c(p):
        if p != []:
            b = [p[1]] + p[2]
            return b
        else:
            return []
    
    @self.pg.production('matrix : OPEN_BRA ts ts_c CLOSE_BRA')
    def matrix(p):
        if p != []:
            mat = [p[1]]+ p[2]
            return mat       
    @self.pg.production('partition : VAR OPEN_BRA number CLOSE_BRA')
    def partition(p):
        return SOL[p[0].getstr()][p[2]]
        
    @self.pg.production('partition : VAR OPEN_BRA number COLON number CLOSE_BRA')
    def partition(p):
        return SOL[p[0].getstr()][p[2]:p[4]]
        
    @self.pg.production('partition : VAR OPEN_BRA number COLON number CLOSE_BRA OPEN_BRA number COLON number CLOSE_BRA')
    def partition(p):
        part = [i[p[7]:p[9]] for i in SOL[p[0].getstr()][p[2]:p[4]]]
        return part
        
    @self.pg.production('partition :  VAR OPEN_BRA number CLOSE_BRA OPEN_BRA number COLON number CLOSE_BRA')
    def partition(p):
        part = SOL[p[0].getstr()][p[2]][p[5]:p[7]]
        return part
        
    @self.pg.production('extension :  VAR ADD VAR')
    def extension(p):
        ext = SOL[p[0].getstr()] + SOL[p[2].getstr()]
        return ext
                
    @self.pg.production('damped : BOOLEAN')
    def damped(p):
        if p[0].getstr()=='False':
            return False
        elif p[0].getstr()== 'True':
            return True
    
    @self.pg.production('trend : TYPE_A')
    def trend(p):
        if p[0].getstr()=='add':
            return 'add'
        elif p[0].getstr()== 'mul':
            return 'mul'
        elif p[0].getstr()=='additive':
            return 'additive'
        elif p[0].getstr()=='multiplicative':
            return 'multiplicative'
            
    @self.pg.production('seasonal : TYPE_A')
    def seasonal(p):
        if p[0].getstr()=='add':
            return 'add'
        elif p[0].getstr()== 'mul':
            return 'mul'
        elif p[0].getstr()=='additive':
            return 'additive'
        elif p[0].getstr()=='multiplicative':
            return 'multiplicative'
            
    @self.pg.production('s_periods : INT')
    def s_periods(p):
        return int(p[0].getstr())
        
        
    def error_handle(token):
        print('ERROR')
        raise ValueError(token)
 
 def get_parser(self):
     return self.pg.build()


            

class Method():
    def __init__(self, ts, args):
        self.ts = ts
        self.args = args
        
class SARIMA(Method):
    def eval(self):
        return SARIMAX(self.ts,order=self.args[0], seasonal_order=self.args[1]).fit(disp=0)
        
class EXPSM(Method):
    def eval(self):
        return ExponentialSmoothing(self.ts, trend=self.args[0], damped = self.args[1], seasonal=self.args[2], seasonal_periods=self.args[3]).fit()
