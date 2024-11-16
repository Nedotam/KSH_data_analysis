import pandas as pd

def read_csv_file(path, file, encode='latin-1', delimiter=';'):
    try:
            df = pd.read_csv(path + file, encoding=encode, delimiter=delimiter, index_col=False)
    except UnicodeDecodeError:
        print(f"Unicode error: The encoding '{encode}' doesn't work.")
        return None
    except FileNotFoundError:
        print(f"File not found in the specified path: {path}")
        return None
    else:
        print("File successfully loaded.")
        return df
    
def cleaning(df):
    df.iloc[:, 1:] = df.iloc[:, 1:].replace(",",".", regex=True)
    print(', have been swapped to .')
    df=df.rename(columns={'Megnevezés': 'Év'})
    print('Megnevezés -> Év')
    df=df.transpose()
    print('DataFrame got transposed')

def export_csv(df, encoding):   
    out_path = "../data/processed/"
    file_name = "clean.csv"
    file_out_path = out_path+file_name
    try:
        df.to_csv(file_out_path, index=False, header=False, encoding=encoding)
    except OSError:
        print("Nincs ilyen mappa")