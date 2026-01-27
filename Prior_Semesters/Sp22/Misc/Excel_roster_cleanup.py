import pandas as pd

# Load the Excel file
with pd.ExcelFile('Spring 2022 Class Rosterv3.xlsx') as xls:
    # Iterate over each sheet
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name)

        # Iterate over each cell in the dataframe excluding the first two rows
        for column in df.columns:
            df.loc[2:, column] = df.loc[2:, column].apply(lambda x: ' '.join([word.capitalize() for word in str(x).split()]) if pd.notnull(x) else x)

        # Save the modified dataframe back to the sheet
        df.to_excel('Spring 2022 Class Rosterv3.xlsx', sheet_name=sheet_name, index=False)
