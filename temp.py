def tempconvert(degrees):
    options = ['c','C','f','F']

    if degrees == 'f' or degrees == 'F':
        fahrenheit = float(input("Enter temperature in Fahrenheit: "))
        celsius = (fahrenheit - 32)/1.8 
        return (str(fahrenheit)+ " degrees Fahrenheit is equal to %.2f degrees Celsius." %celsius) 

    elif degrees == 'c' or degrees == 'C':
        celsius = float(input("Enter temperature in Celsius: "))
        fahrenheit = (celsius * 1.8) + 32
        return (str(celsius)+ " degrees Celsius is equal to %.2f degrees Fahrenheit."%fahrenheit)     
    
    else: 
        return "Please enter 'F' or 'C'" 

print(tempconvert(str(input('F for Fahrenheit or C for Celsius: '))))