true =  100
num = list(map(float, input("enter numbers seperated by a space: ").split()))
ave = sum(num) / len(num)
print("The average is:", ave)

error = ave - true
print("The error is:", error)

if(abs(error) < 0.003 ):
    print("The average is within the acceptable range.")
else:
    print("The average is outside the acceptable range.")