import pandas as pd
import numpy as np
import scipy
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="centered")

st.session_state.clear()
st.session_state.app_started = False

if st.button("Tisztitas/EDA"):
    st.session_state.app_started = True

if st.session_state.app_started:
    st.write("KSH adat elemzese")

    path="data/raw/"
    file="raw_data.csv"
    encoding='latin-1'
    skiprows=1
    st.write("#A file elso sora folosleges, encoding hibat ad ki a program utf-8 encodolasra, es a csv ';'-el van elvalasztva.")
    try:
        
        df=pd.read_csv(path+file, encoding=encoding, delimiter=';', skiprows=skiprows )
        
    except UnicodeDecodeError:
        print("Unicode error")
    except FileNotFoundError:
        print("A file nem talalhato a "+path+" mappaban")
    else:
        st.table(df)
        
    st.write("#Elso oszlopot, es sort kihagyva minden ,-t .-ra cserelek")
    df.iloc[:, 1:] = df.iloc[:, 1:].replace(",",".", regex=True).apply(pd.to_numeric, errors='coerce')


    st.write("#Amit nem tudok float-ta alakitani azt NaN-re valtom")
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')


    st.write("#A megnevezes oszlopnevet Ev-re cserelem")
    df=df.rename(columns={'Megnevezés': 'Év'})
    df=df.transpose()
    df.reset_index(inplace=True)
    st.table(df)
    st.write("Kimentem a megtisztitott adatot")
    out_path = "data/processed/"
    file_name = "clean_data.csv"
    file_out_path = out_path+file_name
    try:
        df.to_csv(file_out_path, index=False, header=False, encoding=encoding)
    except OSError:
        print("Nincs ilyen mappa")
        
    path='data/processed/'
    file='clean_data.csv'
    encode='latin-1'

    try:
        df=pd.read_csv(path+file, encoding=encode, delimiter=',')
        
    except UnicodeDecodeError:
        print("Unicode error: "+encode+" nem mukodik")
    except FileNotFoundError:
        print("A file nem talalhato a "+path+" mappaban")
    else:
        print(df)




    st.write("#az osszehasonlitast kezdem az elso oszloppal, es azt osszehasonlitom az osszes tobbi oszloppal")
    for outer in range(1, df.shape[1]):
        #onmagaval nem hasonlitom ossze, ezert a sorszam+1 tol inditom a belso ciklust // df.shape[1] megadja az oszlopok szamossagat
        for inner in range(outer+1, df.shape[1]):
            #valtozoba teszem az osszehasonlitast
            relation=df.iloc[1:,outer].corr(df.iloc[1:,inner])
            #print(f)-el ki tudok valtozokat iratni
            print(f'A {df.columns[outer]} es {df.columns[inner]} osszefuggesi erossege: {relation}')
            

    st.write("#Legeneralom a linechartokat, majd kesobb kivalasztjuk hogy melyik relevans. Ez resze az EDA-nek (Exploratory Data Analysis). Lenyegeben megnezunk mindent, es probaljuk eszrevenni az osszefuggeseket.")
    for outer in range(1, df.shape[1]):  
        
        column_outer = df.iloc[:, [0, outer]]  # 'Év' es egy oszlop
        
        for inner in range(outer + 1, df.shape[1]):
            
            column_inner = df.iloc[:, [0, inner]]  # 'Év' es egy masik oszlop
            plt.figure(figsize=(8, 5))
            # elso oszlop plot
            sns.lineplot(x='Év', y=column_outer.columns[1], data=column_outer, label=df.columns[outer])
            
            # masodik oszlop plot
            sns.lineplot(x='Év', y=column_inner.columns[1], data=column_inner, label=df.columns[inner])

            plt.title(f"{df.columns[outer]} vs {df.columns[inner]}")
            plt.xlabel("Év")
            plt.ylabel("%")
            plt.legend()
            st.pyplot(plt)
            plt.clf()
            
    st.write("#az utolso evet eltavolitom, mert a NaN ertekek zavarjak a linearis regressziot")
    st.write("#feltoltottem a hianyzo adatot a kovetkezo evi adatbol")
    st.write("Elotte:")
    st.table(df)
    linear_df=df.drop(axis=0, index=df.shape[0]-1)


    linear_df.bfill(inplace=True)

    st.write("Utana:")
    st.table(linear_df)
    linear_df.info()


    st.write("Most keresek linearis regressziot az adatok kozt.")
    for i in range(1, linear_df.shape[1]):
        res = stats.linregress(linear_df['Év'], linear_df.iloc[:, i])
        st.write(f"{linear_df.columns[i]} R^2: {res.rvalue**2:.6f}")



    st.write("# Nem linearis a valtozas, erre lehetett is szamitani, mivel sok komponense lehet a piac alakulasanak.")
else:
    st.write("Az inditashoz nyomd meg a gombot.")
st.write("....")
st.write("...")
st.write("..")
st.write(".")
if st.button("Script ujrainditas"):
    st.session_state.app_started = False
    st.session_state.clear()