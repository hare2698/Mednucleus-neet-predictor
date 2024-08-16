import re
original_value = input('whatever value coming from db should be assigned to this temp variable')
cleaned_value = re.sub(r'\D', '', original_value) #cleaned_value variable should be actual_var_name
