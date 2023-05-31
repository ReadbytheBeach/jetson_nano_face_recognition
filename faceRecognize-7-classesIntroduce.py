class Rectangle:
    # if a function in class, we call it method
    def __init__(self,color,w,l):
        # self means OBJECTS rect1, rect2,....
        self.width = w
        self.length = l
        self.color = color
    # every method should be recall to use
    def area(self): 
        self.area = self.width * self.length
        return self.area
    def per(self):
        self.perimeter = 2* self.width + 2* self.length
        return self.perimeter

c1 = 'red'
w1 = 3
l1 = 4

# following rect1= Rectangle(para1,para2,...) means: __init__ (self,para1,para2,...), self == rect1
rect1 = Rectangle(c1,w1,l1)

# call a method before 
areaRect1 = rect1.area()
print(areaRect1)

per1 = rect1.per()

print('per1', rect1.color, per1)