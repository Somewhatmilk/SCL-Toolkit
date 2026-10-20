import pandas as pd

# Data
data = {
    'Size(Included cover)': ['190×190×130', '190×280×100', '190×280×130', '190×280×180', '190×380×130',
                             '190×380×180', '280×280×130', '280×340×130', '280×380×130', '280×380×180',
                             '280×560×130', '330×430×180', '380×560×180'],
    'W1xL1xH1(mm)': ['7.48×7.48×5.12', '7.48×11.02×3.94', '7.48×11.02×5.12', '7.48×11.02×7.09', '7.48×14.96×5.12',
                    '7.48×14.96×7.09', '11.02×11.02×5.12', '11.02×13.39×5.12', '11.02×14.96×5.12', '11.02×14.96×7.09',
                    '11.02×22.05×5.12', '12.99×16.93×7.09', '14.96×22.05×7.09'],
    'ABS Grey Cover': ['BC-AGS-191913', 'BC-AGS-192810', 'BC-AGS-192813', 'BC-AGS-192818', 'BC-AGS-193813',
                       'BC-AGS-193818', 'BC-AGS-282813', 'BC-AGS-283413', 'BC-AGS-283813', 'BC-AGS-283818',
                       'BC-AGS-285613', 'BC-AGS-334318', 'BC-AGS-385618'],
    'ABS Transparent Cover': ['BC-ATS-191913', 'BC-ATS-192810', 'BC-ATS-192813', 'BC-ATS-192818', 'BC-ATS-193813',
                              'BC-ATS-193818', 'BC-ATS-282813', 'BC-ATS-283413', 'BC-ATS-283813', 'BC-ATS-283818',
                              'BC-ATS-285613', 'BC-ATS-334318', 'BC-ATS-385618'],
    'PC Grey Cover': ['BC-CGS-191913', 'BC-CGS-192810', 'BC-CGS-192813', 'BC-CGS-192818', 'BC-CGS-193813',
                      'BC-CGS-193818', 'BC-CGS-282813', 'BC-CGS-283413', 'BC-CGS-283813', 'BC-CGS-283818',
                      'BC-CGS-285613', 'BC-CGS-334318', 'BC-CGS-385618'],
    'PC Transparent Cover': ['BC-CTS-191913', 'BC-CTS-192810', 'BC-CTS-192813', 'BC-CTS-192818', 'BC-CTS-193813',
                             'BC-CTS-193818', 'BC-CTS-282813', 'BC-CTS-283413', 'BC-CTS-283813', 'BC-CTS-283818',
                             'BC-CTS-285613', 'BC-CTS-334318', 'BC-CTS-385618'],
    'Plastic PG Type': ['N.A', '1928 PG', '1928 PG', '1928 PG', 'N.A', 'N.A', 'N.A', 'N.A', '2838 PG', '2838 PG', 'N.A', 'N.A', 'N.A'],
    'Plastic P type': ['1919 P', '1928 P', '1928 P', '1928 P', '1938 P', '1938 P', '2828 P', '2834 P', '2838 P', '2838 P', 'N.A', '3343 P', 'N.A'],
    'Steel S Type': ['1919 S', '1928 S', '1928 S', '1928 S', '1938 S', '1938 S', '2828 S', '2834 S', '2838 S', '2838 S', '2856 S', '3343 S', '3586 S']
}

# Create DataFrame
df = pd.DataFrame(data)

# Write to Excel file
excel_file_path = 'output_data.xlsx'
df.to_excel(excel_file_path, index=False)

print(f'Data has been exported to {excel_file_path}')
