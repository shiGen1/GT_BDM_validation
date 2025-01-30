import os
import pandas as pd
import glob
import numpy as np

# Specify the location of that brand and the retailers in subfolders
base_folder = r'C:\Users\G704790\OneDrive - General Mills\Desktop\NV_old'          
subfolders = ['Amazon', 'Kroger']
# -----------------------------------------------------------------------------------
def vif_process_csv(csv_path):

    # this function will return a dataframe with 
    # columns containing count of variables who cross their threshold i:e [vif > 20 or t-score <-1 or > 1]
    try:
        input_variable = pd.read_csv(csv_path)
        vif = (input_variable['VIF'] > 20).sum()
        tscore = ((input_variable['T-Value'] > 1) | (input_variable['T-Value'] < -1)).sum()
        vif_t_count = pd.DataFrame({'VIF': [vif], 'T_score': [tscore]})  
        return vif_t_count
    except Exception as e:
        print(f"Error processing VIF for {csv_path}: {e}")
    return None


def contribution_g_process_csv(csv_path):

    # This function tells us the number of variables under each contribution group.

    try:
        df = pd.read_csv(csv_path)
        contribution_count = df.groupby('Contribution Group').size().reset_index(name='Number of Variables')
        total = pd.DataFrame({'Contribution Group': ['Total'], 'Number of Variables': [contribution_count['Number of Variables'].sum()]})
        contribution_result = pd.concat([contribution_count, total], ignore_index=True)
    # the table gives us contribution table's count
        return contribution_result
    except Exception as e:
        print(f"Error processing contribution-group for {csv_path}: {e}")
    return None

def prior_process_csv(csv_path):
    
    # This will return a dataframe on the count of variables whose priors lie in their bounds or not
    # Here the bounded-interval is taken 90% of the provided interval so as to avoid the danger of outlier
    
    try:
        prior = pd.read_csv(csv_path,header=1)
        prior['5th-percent'] = prior['Lower'] + 0.05 * (prior['Upper'] - prior['Lower'])
        prior['95th-percent'] = prior['Lower'] + 0.95 * (prior['Upper'] - prior['Lower'])
    
        prior['Lies_within_range'] = prior.apply(lambda row: pd.NA if pd.isna(row['5th-percent']) or pd.isna(row['95th-percent'])
                              else ('yes' if row['5th-percent'] <= row['Prior Coeff'] <= row['95th-percent'] else 'no'), axis=1)
    
        prior_result = prior[['Variable Name','Prior Coeff', 'Lower', 'Upper','5th-percent', '95th-percent', 'Lies_within_range']]
    
        unique_value = prior_result['Lies_within_range'].value_counts(dropna=False)
        total = len(prior_result['Lies_within_range'])
        prior_unique_values = pd.DataFrame({
            "Value": unique_value.index,  # Unique values
            "Count": unique_value.values  # Corresponding counts
        })
    
        # table that tells us if prior lies in bound or not as there are "no" so all-right.
        prior_unique_values = pd.concat([pd.DataFrame({"Prior-Value": ["Total"], "Count": [total]}), prior_unique_values], ignore_index=True)
        return prior_unique_values
    except Exception as e:
        print(f"Error processing prior-bounded for {csv_path}: {e}")
    return None

def r2_mape_extract(csv_path):
    # this will simply extract the r-square and MAPE values from a file
    try:
        df = pd.read_csv(csv_path)
        r2=df.loc[0,"R bar^2"]*100
        mape = df.loc[0,"MAPE"]*100
        r2_and_MAPE = pd.DataFrame({'R2': [r2], 'MAPE': [mape]})
        return r2_and_MAPE
    except Exception as e:
        print("No r-square or/and MAPE found")
        return None
              
        

def data_influence(csv_path):
    # It will give a count of variable allocated to a specific bin.
    # Write a flag that tells which variable are becoming outliers and their values
    try:
        df = pd.read_csv(csv_path,header=1)
        bins = [0, 0.25,0.50,1,1.25, 1.50,1.75,2, 5,float('inf')]
        df = df.copy()
        df.loc[:, 'binned'] = pd.cut(df['Data Influence'], bins)
        bin_counts = df['binned'].value_counts()
        print(bin_counts.sort_index())
        outlr_bin = df['binned'].cat.categories[-1]
        outlr_bin_values = df[df['binned'] == outlr_bin]
        print(f"The outlier are : \n{outlr_bin_values["Variable Name"].reset_index(drop=True)}")
    except Exception as e:
        print(f"Error processing Data Influence for {csv_path}: {e}")
        return None
#########################
#def model_tranform(csv_path):
#-------------"To be decided"---------------    
########################3

# This is more of structural/process defining function which will basically read csv's and allocate appropriate function based on their names

def read_and_process_folders(base_folder, subfolders):
    for subfolder in subfolders:
        print("**************************************************************************************************")
        print(f"Processing subfolder: {subfolder}")
        current_folder = os.path.join(base_folder, subfolder)
        csv_files = glob.glob(os.path.join(current_folder, "*.csv"))
        csv_file_names = [os.path.basename(file) for file in csv_files]#extracting the names of csv files
        print(f"Found CSV files in: {csv_file_names}")
        
 
        for csv_file in csv_files:
            
            if 'var_in' in csv_file:
                vif_t_count = vif_process_csv(csv_file)
                if vif_t_count is not None:
                    print(vif_t_count)
                contribution_result = contribution_g_process_csv(csv_file)
                if contribution_result is not None:
                    print(contribution_result)
            elif 'prior' in csv_file:
                prior_unique_values = prior_process_csv(csv_file)
                if prior_unique_values is not None:
                    print(prior_unique_values)
            elif 'r2_mape' in csv_file:
                r2_and_mape = r2_mape_extract(csv_file)
                if r2_and_mape is not None:
                    print(r2_and_mape)        
            elif 'summary' in csv_file:
                bin_counts = data_influence(csv_file)
                if bin_counts is not None:
                    print(bin_counts)
# ------------------------------------------------------------------------------------------
# Run the function to process the folders
read_and_process_folders(base_folder, subfolders)