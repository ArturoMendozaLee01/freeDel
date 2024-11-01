 # Paso 1

df = pd.read_excel('/content/drive/MyDrive/Tony&Arthur/RiskMatrix.xlsx', skiprows=1)

df.columns = df.columns.str.replace(' ', '_')
df['Significance_of_Excess'] = df.Significance_of_Excess.ffill()
df['Risk_Category'] = df.Risk_Category.ffill()
df
def get_crr_category(crr_value):
    crr_categories = {
        'CRR_1.1_to_2.2': 1.1 <= crr_value <= 2.2,
        'CRR_3.1_to_4.3': 3.1 <= crr_value <= 4.3,
        '>CRR_5.1': crr_value >= 5.1
    }

    # Return the category if it matches; otherwise, return None or a default value
    for category, condition in crr_categories.items():
        if condition:
            return category
    return "Out of range"



excess = {'Risk_Category': 'CAT-B', 'Products': 'Derivatives', 'CRR':3.3, 'Balance':6}

category = get_crr_category(excess['CRR'])
print(category)  # Output: 'CRR_3.1_to

#df.query('Risk_Category == @excess["Risk_Category"]')

# Paso 2

def clean_crr_columns(df, columns):
  for col in columns:
    df[col] = df[col].astype(str).str.replace('>$', '', regex=False)
    df[col] = df[col].astype(str).str.replace('min', '', regex=False)
  return df

columns_to_clean = ['>CRR_5.1', 'CRR_1.1_to_2.2', 'CRR_3.1_to_4.3']
df = clean_crr_columns(df, columns_to_clean)
df[['CRR_1.1_to_2.2','CRR_3.1_to_4.3','>CRR_5.1']].apply(process_crr_column)
df
# Paso 3

def process_crr_column(value):
    if isinstance(value, str) and value.endswith('k'):
        try:
            return float(value[:-1]) / 1000
        except ValueError:
            return value  # or handle the error as needed
    return value

# Apply the function to the specified columns
df['>CRR_5.1'] = df['>CRR_5.1'].apply(process_crr_column)


df.query('Products == ["Derivatives", "MMK / NI"]')[columns_to_clean].astype(float)

# Paso 4

excess = {'Risk_Category': 'CAT-B', 'Products': 'Derivatives', 'CRR': 3.3, 'Balance': 6}
exceso=df[(df['Risk_Category'] == excess["Risk_Category"]) & (df['Products'] == excess["Products"])][["Significance_of_Excess",category]]

exceso= pd.DataFrame(exceso)


exceso[category]= exceso[category].astype(float)

exceso.loc[exceso[category] < excess["Balance"]]
