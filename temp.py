def tempconvert(unit: str, temperature: int) -> str:
    options = ['c','C','f','F']

    if unit.lower().strip() == 'f': 
        celsius = (temperature - 32)/1.8 
        return (str(temperature)+ " degrees Fahrenheit is equal to %.2f degrees Celsius." %celsius) 

    elif unit.lower().strip() == 'c': 
        fahrenheit = (temperature * 1.8) + 32
        return (str(temperature)+ " degrees Celsius is equal to %.2f degrees Fahrenheit." %fahrenheit)     
    
    else: 
        return "Please enter 'F' or 'C for the scale'" 

# print(tempconvert(str(input('F for Fahrenheit or C for Celsius: ')), float(input("Enter temperature: "))))


# def tempconvert(temp_str):
#     # Check which scale is used ('F' or 'C') and split accordingly
    
#     if 'F' in temp_str:
#         temp, scale = temp_str.split('F')
#         temp = float(temp.strip())  # Convert the temperature to a float and strip any whitespace
#         # Convert Fahrenheit to Celsius
#         converted_temp = (temp - 32) * 5/9
#         return f'{converted_temp:.2f}C'
#     elif 'C' in temp_str:
#         temp, scale = temp_str.split('C')
#         temp = float(temp.strip())  # Convert the temperature to a float and strip any whitespace
#         # Convert Celsius to Fahrenheit
#         converted_temp = (temp * 9/5) + 32
#         return f'{converted_temp:.2f}F'
#     else:
#         return "Invalid input. Please enter a temperature followed by 'C' or 'F'."

# # Example usage
# input_str = input('Enter Temperature and Scale in this format: (100C) ')
# print(tempconvert(input_str))

# def tempconvert(temp_str):
#     temp_str = temp_str.upper()  # Convert to uppercase to handle both 'F' and 'C'
    
#     # Determine the scale and split accordingly
#     if 'F' in temp_str:
#         temp, scale = temp_str.split('F')
#     elif 'C' in temp_str:
#         temp, scale = temp_str.split('C')
#     else:
#         return "Invalid input. Please enter a temperature followed by 'C' or 'F'."
    
#     temp = temp.strip()  # Remove any surrounding whitespace
    
#     # Check if temp is empty after stripping whitespace
#     if not temp:
#         return "Invalid input. Please enter a valid temperature value."
    
#     # Convert temp to float
#     try:
#         temp = float(temp)
#     except ValueError:
#         return "Invalid input. Please enter a numeric temperature value."

#     # Convert the temperature based on the scale
#     if scale == 'F':
#         converted_temp = (temp - 32) * 5/9
#         return f'{converted_temp:.2f}C'
#     else:  # scale == 'C'
#         converted_temp = (temp * 9/5) + 32
#         return f'{converted_temp:.2f}F'

# # Example usage
# input_str = input('Enter Temperature and Scale: ')
# print(tempconvert(input_str))

#breaks if you input something like 100F100 or F100F

# if __name__ == "__main__":
#     main()