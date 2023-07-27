
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QFileDialog
import matplotlib.pyplot as plt


# Dados das disciplinas
disciplinas = ['Atualidades', 'Constitucional', 'Direito Administrativo', 'Direito Penal',
               'Direito Processual Civil', 'Direito Processual Penal', 'Informática',
               'Matemática', 'Normas da Corregedoria', 'Português', 'Raciocínio Lógico']

# Valores pré-carregados dos acertos e erros. Pode ser modificado posteriormente
prova1 = "São Paulo"
prova2 = "São Bernardo"
acertos1 = [5, 7, 8, 5, 4, 7, 14, 5, 5, 19, 6]
erros1 = [1, 0, 0, 1, 3, 0, 0, 1, 1, 5, 4]
acertos2 = [6, 4, 6, 3, 6, 7, 13, 5, 5, 22, 9]
erros2 = [1, 0, 1, 3, 1, 0, 1, 1, 1, 2, 1]
nota_corte1 = 76
nota_corte2 = 80

# Classe principal da janela

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Estado inicial
        self.state = 0

        # Configurações iniciais da janela
        self.setWindowTitle("Concurso TJ-SP")
        self.setFixedSize(1024, 840)

        # Criar um widget central para a janela
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Criar um layout vertical para o widget central
        layout = QVBoxLayout(central_widget)

        # Adicionar a label de totais
        self.total_label = QLabel(self)
        self.total_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # Adicionar o total_label ao layout principal como primeiro widget
        layout.addWidget(self.total_label)

        # Criar o layout de grade para as caixas de entrada de dados
        grid_layout = QGridLayout()

        # Lista de caixas de entrada de dados para cada prova
        self.acertos_inputs = []
        self.erros_inputs = []

        # Adicionar as caixas de entrada de dados ao layout de grade
        for i, disciplina in enumerate(disciplinas):
            # Labels
            label_disciplina = QLabel(disciplina)
            label_acertos = QLabel("Acertos:")
            label_erros = QLabel("Erros:")

            # Caixas de entrada de dados
            acertos_input = QLineEdit(self)
            erros_input = QLineEdit(self)

            # Adicionar as caixas de entrada de dados ao layout de grade
            grid_layout.addWidget(label_disciplina, i, 0)
            grid_layout.addWidget(label_acertos, i, 1)
            grid_layout.addWidget(acertos_input, i, 2)
            grid_layout.addWidget(label_erros, i, 3)
            grid_layout.addWidget(erros_input, i, 4)

            # Adicionar as caixas de entrada de dados à lista
            self.acertos_inputs.append(acertos_input)
            self.erros_inputs.append(erros_input)

        # Campo para entrada da nota de corte
        self.nota_corte_input = QLineEdit(self)
        grid_layout.addWidget(QLabel("Nota de Corte:"), len(disciplinas), 1)
        grid_layout.addWidget(self.nota_corte_input, len(disciplinas), 2)

        # Adicionar o layout de grade ao layout vertical
        layout.addLayout(grid_layout)

        # Adicionar o gráfico
        self.figure_widget = plt.figure(figsize=(12, 6))
        self.figure_widget.subplots_adjust(left=0.2)
        layout.addWidget(self.figure_widget.canvas)

        # Criar o botão "Gerar Gráfico"
        button = QPushButton("Gerar Gráfico", self)
        button.clicked.connect(lambda: self.gerar_grafico(
            self.acertos_inputs, self.erros_inputs, self.nota_corte_input))

        # Adicionar o botão ao layout vertical
        layout.addWidget(button)
        
        # Criar o botão "Salvar Gráfico"
        save_button = QPushButton("Salvar Gráfico", self)
        save_button.clicked.connect(self.save_plot)

        # Adicionar o botão ao layout vertical
        layout.addWidget(save_button)

        # Criar o botão para alternar entre os dados das provas
        toggleButton = QPushButton("Alternar Prova", self)
        toggleButton.clicked.connect(self.toggle_data)

        # Adicionar o botão ao layout vertical
        layout.addWidget(toggleButton)

        # Preencher as caixas de entrada de dados com os valores iniciais
        self.update_inputs()

    def update_inputs(self):
        acertos = acertos1 if self.state == 0 else acertos2
        erros = erros1 if self.state == 0 else erros2
        nota_corte = nota_corte1 if self.state == 0 else nota_corte2
        prova = prova1 if self.state == 0 else prova2

        for i, (acertos_input, erros_input) in enumerate(zip(self.acertos_inputs, self.erros_inputs)):
            acertos_input.setText(str(acertos[i]))
            erros_input.setText(str(erros[i]))

        self.nota_corte_input.setText(str(nota_corte))
        self.total_label.setText(f'Prova: {prova:<16} Acertos: {sum(acertos)}/{sum(acertos) + sum(erros)} Nota: {(sum(acertos) * 100) / (sum(acertos) + sum(erros)):.2f}')    
        
    def toggle_data(self):
        # Alterna entre 0 e 1
        self.state = 1 - self.state

        # Atualizar as caixas de entrada de dados
        self.update_inputs()
        # Gerar o gráfico novamente
        self.gerar_grafico(self.acertos_inputs,
                           self.erros_inputs, self.nota_corte_input)


    def gerar_grafico(self, acertos_inputs, erros_inputs, nota_corte_input):
            # Obter os valores digitados nas caixas de entrada de dados
        acertos = [int(acertos_input.text())
                   for acertos_input in acertos_inputs]
        erros = [int(erros_input.text()) for erros_input in erros_inputs]
        nota_corte = int(nota_corte_input.text())

        # Calcular as notas e diferenças
        notas = [(acertos[i] * 100) / (acertos[i] + erros[i])
                 for i in range(len(acertos))]
        diferenca = [100 - nota for nota in notas]

        # Calcular total de acertos, total de questões e nota total
        total_acertos = sum(acertos)
        total_questoes = total_acertos + sum(erros)
        nota_total = (total_acertos * 100) / total_questoes

        # Atualizar o label de totais
        self.total_label.setText(
            f"Acertos: {total_acertos}/{total_questoes}, Nota: {nota_total:.2f}")

        # Configurar o gráfico de barras
        self.figure_widget.clear()  # Limpar o gráfico anterior
        ax = self.figure_widget.add_subplot(111)
        bar_width = 0.4
        index = range(len(disciplinas))

        ax.barh(index, notas, color='green', label='Nota', height=bar_width)
        ax.barh(index, diferenca, color='orange',
                label='Diferença', left=notas, height=bar_width)
        ax.axvline(x=nota_corte, color='red', linestyle='--')
        ax.text(nota_corte - 1, -0.15,
                f'Corte: {nota_corte}', color='white', ha='right')

        for i, (nota, diff) in enumerate(zip(notas, diferenca)):
            ax.annotate(f'{nota:.2f}', (nota + 1, i),
                        color='black', ha='left', va='center', fontsize=9)
            ax.text(40, i, f'{acertos[i]}/{acertos[i] + erros[i]}',
                    color='white', ha='center', va='center', fontsize=9)

        # Configurar os eixos
        ax.set_xlim([0, 105])
        ax.set_yticks(index)
        ax.set_yticklabels(disciplinas)
        ax.set_xlabel('Nota')
        ax.set_title('Gráfico de Notas por Disciplina')
        #ax.legend()
        
        # Atualizar a label de totais
        self.update_inputs()

        # Atualizar o gráfico
        self.figure_widget.canvas.draw()
        
    def save_plot(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getSaveFileName(
            self, 'Salvar Gráfico', '', 'Images (*.jpg)')
        if filename:
            self.figure_widget.savefig(filename)

# Executar a aplicação
if __name__ == "__main__":
    app = QApplication([])
    main = MainWindow()
    main.show()
    app.exec()

