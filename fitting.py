import numpy as np

class Fitting:  
    
    def __init__(self,X,Y):  
        self.x = np.array(X)  
        self.y = np.array(Y)  
        
    def fitting(self,n):  
        self.z = np.polyfit(self.x,self.y,n)  
        self.p = np.poly1d(self.z)  
        self.val = np.polyval(self.p,self.x)
        self.error = np.abs(self.y - self.val)
        self.ER2 = np.sum(np.power(self.error,2))/len(self.x)
        return self.z,self.p  
    
    def geterror(self):  
        return self.error,self.ER2
    
