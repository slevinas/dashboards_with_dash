
import pandas as pd










datadorfeatures = {'ID': [1, 2, 3, 4, 5, 6,],
                   
                  
                  
                  }
            
df_features = pd.DataFrame(datadorfeatures)

print(df_features)

 'measureValue': [
73,
322,
56,
30/150,
39,
6.7
],  
'FeatureName':[
'N_Email_Sent', 
'Patient Follow-Up \(N_SMS_Sent\)', 
'N_medTeam_logins', 
'Staff-to-Patient Ratio', 
'Patient Follow-Up Rate', 
'Overall Patient Satisfaction'],
'Feat_Definiton': [
"""The total number of email that where sent on that date""", 
"""The total number of SMS sent on that date""", 
"""The number of CareTeam logins on that date """, 
"""Staff-to-Patient Ratio = Number of Staff : Number of Patients""", 
"""Patient Follow-Up Rate (%) = (Number of Follow-Ups / Total Number of Patients) *100", """,
"""Based on a Survye resposes:very-happy =10 happy = 5 indiferent = 4 not-happy = 1"""
],
'feature_Description': [
"""nan """, 
"""nan """, 
"""Measures the number of patients who receive a follow-up after their stay at the facility. This could be from a physician, nurse, or other staff member asking about the patient’s improvements. """ , 
"""The quality of care you receive in a healthcare facility is highly dependent on the amount of attention a patient receives. The easiest way to track this is by comparing the number of staff to the number of patients. This healthcare metric is so critical that the state of California has a legally enforced staff-to-patient ratio to ensure a minimum quality of care.""", 
"""Measures the number of patients who receive a follow-up after their stay at the facility. This could be from a physician, nurse, or other staff member asking about the patient’s improvements. This metric is used in conjunction with readmission rate; a higher follow-up rate will often lead to a lower readmission rate. """,
""" Overall Patient Satisfaction: This is a healthcare metric that calculates patient satisfaction. This can be a great marketing tool for your organization if satisfaction is high, but a low satisfaction level could signal a problem with the facility and its services."""],
'measureType': [
"""numeric""",
"""num of emails sent numeric""", 
"""numeric""",
"""ratio """, 
"""percetage """,
 """degrees of statisfections. as aggreggated avg' """
 ],
'measureValue': [
73,
322,
56,
30/150,
39,
 6.7,]

