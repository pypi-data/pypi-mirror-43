class Calculations(object):
    def __init__(self,_num1=0,_num2=0):
        self.num1 = _num1
        self.num2 = _num2

    def Add(self):
        result = self.num1+self.num2
        print ('the final result for {} and {} is {}'.format(self.num1,self.num2,result))
        return 'the final result for {} and {} is {}'.format(self.num1,self.num2,result)

    def Sub(self):
        result = self.num1-self.num2    
        print('the final result for {} and {} is {}'.format(self.num1,self.num2,result))
        return 'the final result for {} and {} is {}'.format(self.num1,self.num2,result)
c = Calculations(1,3)
# c.Add()
# c.Sub()