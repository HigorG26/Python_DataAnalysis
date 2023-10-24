import tkinter as tk
import datetime as dt
import os

date = dt.datetime.today()

def ExcluirCSV():
    path = os.path.expanduser('~/Downloads')
    file = 'data.csv'
    fullPath = os.path.join(path, file)
    if (fullPath):
        os.remove(fullPath)
        label_file['text'] = 'Arquivo excluído da pasta Download!'
        label_file['fg'] = '#caeb10'
        button.destroy()
    else:
        label_file['text'] = 'Arquivo não encontrado na pasta Download!'
        label_file['bg'] = 'white'
        label_file['fg'] = 'red'

def GeraRelatorio():
    import pandas as pd

    pasta_downloads = os.path.expanduser('~/Downloads')
    nome_arquivo = 'data.csv'
    caminho_arquivo = os.path.join(pasta_downloads, nome_arquivo)
    busca_arquivo = os.path.exists(caminho_arquivo)
    if busca_arquivo:
        df = pd.read_csv(caminho_arquivo)
    else:
        label_file['text'] = 'Arquivo não encontrado na pasta Download!'
        label_file['bg'] = 'white'
        label_file['fg'] = 'red'

    analise = df[['PO Responsável', 'Demanda', 'Previsão entrega fase']]
    analise = analise.sort_values(by='PO Responsável')

    df['Previsão entrega fase'] = pd.to_datetime(df['Previsão entrega fase'], dayfirst=True)
    
    analise['Previsão entrega fase'] = df['Previsão entrega fase']

    informacoes = []

    for index, row in analise.iterrows():
        data_na_linha = row['Previsão entrega fase']
        
        if pd.notna(data_na_linha):
            if isinstance(data_na_linha, pd.Timestamp):
                if data_na_linha.to_pydatetime() < date:
                    data_formatada = data_na_linha.to_pydatetime().strftime('%d/%m/%Y')
                    informacoes.append("PO Responsável: " + str(row['PO Responsável']))
                    informacoes.append("Demanda: " + str(row['Demanda']))
                    informacoes.append("Previsão entrega fase: " + data_formatada)
                    informacoes.append("")
            else:
                informacoes.append("Conflito na data!")

    

    desktop_path = os.path.expanduser("~/Desktop")
    nome_arq_salvo = 'analise.txt'
    caminho_completo = os.path.join(desktop_path, nome_arq_salvo)
    with open(caminho_completo, 'w') as arquivo:
        arquivo.write('\n'.join(informacoes))
    
    label_file['text'] = 'Relatório gerado na sua área de trabalho!'
    label_file['fg'] = '#52e319'
    label_file['bg'] = 'gray'

    if label_file['text'] == 'Relatório gerado na sua área de trabalho!':
        ##button.destroy()
        button['text'] = 'Deseja excluir arquivo data.csv?'
        button['width'] = 25
        button['command'] = ExcluirCSV


window = tk.Tk()
window.title('Análise de Demandas') #titulo
window.geometry('350x200') #tamanho
window.config(background='blue')
window.resizable(width=False, height=False)

label_title = tk.Label(window, width=53, height=2, text='Lembre-se de salvar a tabela em .CSV', bg='lightblue', border=3)
label_title.grid(row=0, column=0, pady=10)

label_date = tk.Label(window, width=53, height=2, text='Data: '+ date.strftime('%d/%m/%Y'), bg='lightblue', border=3)
label_date.grid(row=1, column=0, pady=10)

label_file = tk.Label(window, width=53, height=2, text='Não há interações ainda.', bg='lightblue', border=3)
label_file.grid(row=2, column=0, pady=10)

button = tk.Button(window, command=GeraRelatorio, width=12, height=1, text='Gerar Relatório', relief='solid')
button.grid(row=3, column=0)

window.mainloop()

