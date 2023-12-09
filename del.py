def generate_latex_table_from_file(file_path):
    try:
        # Lendo os dados do arquivo
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Iniciando a construção da tabela em LaTeX
        latex_table = [
            "\\begin{table}[ht]",
            "\\centering",
            "\\begin{tabular}{|c|c|c|c|c|c|}",
            "\\hline",
            "\\textbf{Instância} & \\textbf{Algoritmo} & \\textbf{Resultado} & \\textbf{Tempo (s)} & \\textbf{Memória (MB)} & \\textbf{Qualidade} \\\\",
            "\\hline"
        ]

        # Processando cada linha do arquivo e adicionando à tabela
        for line in lines[1:]:  # Pulando a linha do cabeçalho
            # Removendo espaços extras e quebras de linha
            data = line.strip().split(',')
            # Verificar se a linha tem a quantidade correta de colunas
            if len(data) == 6:
                # Arredondando a qualidade para duas casas decimais
                # Removendo o símbolo de porcentagem antes de converter para float
                data[5] = f"{float(data[5].strip('%')):.2f}\\%"
                # Adicionando a linha formatada à tabela
                latex_table.append(" & ".join(data) + " \\\\")
            else:
                print(f"Linha inválida ou com dados insuficientes: {line}")

        # Finalizando a tabela
        latex_table.extend([
            "\\hline",
            "\\end{tabular}",
            "\\caption{Comparação dos Algoritmos TATT e Christofides}",
            "\\label{tab:algorithms_comparison}",
            "\\end{table}"
        ])

        return "\n".join(latex_table)

    except FileNotFoundError:
        return "Arquivo não encontrado."

# Caminho do arquivo de dados
file_path = "results_tsp.txt"  # Substitua pelo caminho correto do seu arquivo

# Gerar a tabela em LaTeX
latex_table_content = generate_latex_table_from_file(file_path)
print(latex_table_content)
