# Data Quality Assessment Scripting
# Alejandro Malagon

def exec_data_quality(dataFrame, max_unique_values = 20, neg_numeric_test = 0, no_num_test = []):
    # Arguments
    # dataFrame accepts a pandas DataFrame for which to perform the data quality assessment
    
    # max_unique_values accepts an integer representing how many unique values to show for columns
    # if the number of unique values exceeds this value, ... is replaced rather than outputting every
    # value

    # neg_numeric_test accepts an integer (0, 1)
    # 0 - do not fail a numeric field if it contains negative numbers
    # 1 - fail a numeric field if it contains negative numbers

    # TODO: No numbers test (alphanumeric only)
    # TODO: No letter test (numeric only)
    # TODO: Pair population test (if A is populated, B is populated)
    # TODO: Pair population test (at least one of A, B, ... is populated)
    # TODO: Country validity test

    # Import statement for return table
    import pandas as pd

    # Initialize return dataframe
    df_dqa = pd.DataFrame(columns = 
        ['Column Name', 
         'Data Type', 
         'Num. Populated Values', 
         'Num. Null Records', 
         'Completeness %',
         'Range Minimum',
         'Range Maximum',
         'Negative Values Test',
         'Minimum String Length',
         'Maximum String Length',
         'Num. Distinct Values',
         'Categorical Values'])

    # Identify columns in DataFrame
    col_list = list(dataFrame.columns.values)

    for col in col_list:
        # Get data type
        if 'int' in str(dataFrame[col].dtypes):
            data_type = 'integer'
        elif 'float' in str(dataFrame[col].dtypes):
            data_type = 'decimal'
        elif 'datetime' in str(dataFrame[col].dtypes):
            data_type = 'datetime'
        elif 'date' in str(dataFrame[col].dtypes):
            data_type = 'date'
        else:
            data_type = 'string'

        # Count # of populated records
        non_null_cnt = dataFrame[col].count()

        # Count # of NaN records
        null_cnt = dataFrame[col].isnull().sum()

        # Determine % completeness
        cmplt_pct = "{:.2%}".format(non_null_cnt / (non_null_cnt + null_cnt))

        # Get minimum for numeric values
        if data_type in ['integer', 'decimal', 'date', 'datetime']:
            numeric_min = dataFrame[col].min()
        else:
            numeric_min = 'N/A'

        # Get maximum for numeric values
        if data_type in ['integer', 'decimal', 'date', 'datetime']:
            numeric_max = dataFrame[col].max()
        else:
            numeric_max = 'N/A'

        # Numeric Positive / Negative Test
        if data_type in ['integer', 'decimal'] and neg_numeric_test == 0 :
            neg_test_rslt = 'Not Tested'
        elif data_type in ['integer', 'decimal'] and neg_numeric_test == 1 :
            if dataFrame[col][dataFrame[col] < 0].count() == 0 :
                neg_test_rslt = 'Passed'
            else:
                neg_test_rslt = 'Failed - ' + str(dataFrame[col][dataFrame[col] < 0].count()) + ' neg. values found.'
        else:
            neg_test_rslt = 'N/A'

        # Get minimum string length for string values
        if data_type == 'string':
            min_str_length = dataFrame[col].str.len().min()
        else:
            min_str_length = 'N/A'

        # Get maximum string length for string values
        if data_type == 'string':
            max_str_length = dataFrame[col].str.len().max()
        else:
            max_str_length = 'N/A'

        # Get number of unique values
        num_unique_vals = len(list(dataFrame[col].unique()))

        # Generate list of unique values if less than or equal to max_unique_values arg.
        # Otherwise, input '...' string.
        if len(list(dataFrame[col].unique())) <= max_unique_values:
            list_unique_vals = str(list(dataFrame[col].unique()))
        else:
            list_unique_vals = '...'

        # Create a DataFrame containing the row
        df_row = pd.DataFrame(
            [[col, data_type, non_null_cnt, null_cnt, cmplt_pct, numeric_min, numeric_max, neg_test_rslt, min_str_length, max_str_length, num_unique_vals, list_unique_vals]], 
            columns = list(df_dqa.columns.values))
        df_dqa = df_dqa.append(df_row, ignore_index = True)

    return df_dqa  