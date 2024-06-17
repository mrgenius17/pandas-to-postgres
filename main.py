import pandas as pd;

df = pd.read_excel('flow.xlsx', header=0, dtype={
'patientID': int,
'first name': str,
'last name': str,
'email': str,
'city': str,
'dob': object})

df['dob'] = pd.to_datetime(df['dob'], format='%m/%d/%y')
# print(df)

