import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter.font import Font

# Carregar os datasets
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Verificar se os DataFrames foram carregados corretamente
if movies.empty or ratings.empty:
    raise ValueError("Um dos DataFrames está vazio. Verifique os arquivos CSV.")

# Juntar os datasets para obter as notas dos filmes
movie_ratings = pd.merge(movies, ratings, on='movieId')

# Calcular a média das notas para cada filme
movie_avg_ratings = movie_ratings.groupby('title')['rating'].mean().reset_index()

# Obter todos os gêneros únicos
generos_unicos = set()
for generos in movies['genres'].str.split('|'):
    generos_unicos.update(generos)
generos_unicos = sorted(generos_unicos)  # Ordenar os gêneros

# Função para recomendar um filme aleatório de um gênero específico com boa nota
def recomendar_filme_por_genero(generos_escolhidos):
    # Filtrar filmes que contêm pelo menos um dos gêneros escolhidos
    mask = movies['genres'].apply(lambda x: any(genero in x for genero in generos_escolhidos))
    filmes_do_genero = movies[mask]
    
    if filmes_do_genero.empty:
        return f"Nenhum filme dos gêneros '{', '.join(generos_escolhidos)}' foi encontrado."
    
    # Juntar com as médias das notas
    filmes_com_notas = pd.merge(filmes_do_genero, movie_avg_ratings, on='title')
    
    # Filtrar filmes com nota acima de 4.0 (considerados "muito bons")
    filmes_muito_bons = filmes_com_notas[filmes_com_notas['rating'] > 4.0]
    
    if filmes_muito_bons.empty:
        return f"Nenhum filme dos gêneros '{', '.join(generos_escolhidos)}' com nota muito alta foi encontrado."
    
    # Escolher um filme aleatório
    filme_aleatorio = filmes_muito_bons.sample(1)
    
    titulo = filme_aleatorio['title'].values[0]
    nota = filme_aleatorio['rating'].values[0]
    
    return f"Recomendação: Assista '{titulo}' (Nota média: {nota:.2f})."

# Função para gerar a recomendação do dia
def gerar_recomendacao_do_dia():
    # Filtrar filmes com nota acima de 4.0
    filmes_muito_bons = movie_avg_ratings[movie_avg_ratings['rating'] > 4.0]
    
    if filmes_muito_bons.empty:
        return "Nenhum filme com nota muito alta foi encontrado."
    
    # Escolher um filme aleatório
    filme_aleatorio = filmes_muito_bons.sample(1)
    
    titulo = filme_aleatorio['title'].values[0]
    nota = filme_aleatorio['rating'].values[0]
    
    return f"Recomendação do Dia: '{titulo}' (Nota média: {nota:.2f})."

# Função para lidar com o clique do botão na interface gráfica
def obter_recomendacao():
    # Obter o gênero digitado pelo usuário
    genero_digitado = entry_genero.get().strip()
    
    if not genero_digitado:
        messagebox.showwarning("Aviso", "Por favor, digite um gênero.")
        return
    
    # Verificar se o gênero digitado existe no catálogo
    if genero_digitado not in generos_unicos:
        messagebox.showwarning("Aviso", f"Gênero '{genero_digitado}' não encontrado. Consulte a lista de gêneros disponíveis.")
        return
    
    # Obter a recomendação
    recomendacao = recomendar_filme_por_genero([genero_digitado])
    
    # Exibir a recomendação na caixa de texto
    text_recomendacao.config(state=tk.NORMAL)
    text_recomendacao.delete(1.0, tk.END)
    text_recomendacao.insert(tk.END, recomendacao)
    text_recomendacao.config(state=tk.DISABLED)

# Criar a interface gráfica
root = tk.Tk()
root.title("Sistema de Recomendação de Filmes")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Configurar fontes
fonte_titulo = Font(family="Helvetica", size=16, weight="bold")
fonte_texto = Font(family="Arial", size=12)
fonte_botao = Font(family="Arial", size=12, weight="bold")

# Título da interface
titulo = tk.Label(root, text="Sistema de Recomendação de Filmes", font=fonte_titulo, bg="#f0f0f0", fg="#333333")
titulo.pack(pady=20)

# Frame para a entrada de gênero
frame_entrada = tk.Frame(root, bg="#f0f0f0")
frame_entrada.pack(pady=10)

tk.Label(frame_entrada, text="Digite o gênero que deseja assistir:", font=fonte_texto, bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
entry_genero = ttk.Entry(frame_entrada, font=fonte_texto, width=20)
entry_genero.pack(side=tk.LEFT, padx=5)
botao_buscar = ttk.Button(frame_entrada, text="Buscar", command=obter_recomendacao, style="TButton")
botao_buscar.pack(side=tk.LEFT, padx=5)

# Frame para a lista de gêneros disponíveis
frame_generos = tk.Frame(root, bg="#f0f0f0")
frame_generos.pack(pady=10)

tk.Label(frame_generos, text="Gêneros disponíveis:", font=fonte_texto, bg="#f0f0f0").pack()
text_generos = scrolledtext.ScrolledText(frame_generos, width=50, height=10, font=fonte_texto, bg="white", fg="#333333")
text_generos.pack()
text_generos.insert(tk.END, "\n".join(generos_unicos))
text_generos.config(state=tk.DISABLED)  # Tornar a caixa de texto somente leitura

# Frame para a recomendação do dia
frame_recomendacao_dia = tk.Frame(root, bg="#f0f0f0")
frame_recomendacao_dia.pack(pady=20)

tk.Label(frame_recomendacao_dia, text="Recomendação do Dia:", font=fonte_texto, bg="#f0f0f0").pack()
recomendacao_dia = gerar_recomendacao_do_dia()
label_recomendacao_dia = tk.Label(frame_recomendacao_dia, text=recomendacao_dia, font=fonte_texto, bg="#f0f0f0", fg="#007acc")
label_recomendacao_dia.pack()

# Frame para a recomendação personalizada
frame_recomendacao = tk.Frame(root, bg="#f0f0f0")
frame_recomendacao.pack(pady=20)

tk.Label(frame_recomendacao, text="Recomendação Personalizada:", font=fonte_texto, bg="#f0f0f0").pack()
text_recomendacao = tk.Text(frame_recomendacao, width=60, height=3, font=fonte_texto, bg="white", fg="#333333")
text_recomendacao.pack()
text_recomendacao.config(state=tk.DISABLED)  # Tornar a caixa de texto somente leitura

# Estilo para o botão
style = ttk.Style()
style.configure("TButton", font=fonte_botao, background="#007acc", foreground="white")

# Iniciar a interface gráfica
root.mainloop()
