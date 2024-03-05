import sys
import random
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QMessageBox, QTabWidget, QTextEdit, QLineEdit, QInputDialog, QHBoxLayout
from PyQt5.QtGui import QClipboard

class LotteryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lottery App")
        self.setGeometry(100, 100, 600, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        
        self.tab_choose = QWidget()
        self.tab_widget.addTab(self.tab_choose, "Escolher Jogo")
        
        self.tab_saved = QWidget()
        self.tab_widget.addTab(self.tab_saved, "Jogos Salvos")
        
        self.layout_choose = QVBoxLayout()
        self.tab_choose.setLayout(self.layout_choose)
        
        self.layout_saved = QVBoxLayout()
        self.tab_saved.setLayout(self.layout_saved)
        
        self.label_choose = QLabel("Escolha seu jogo:")
        self.layout_choose.addWidget(self.label_choose)
        
        self.combo_box = QComboBox()
        self.combo_box.addItem("Mega-Sena")
        self.combo_box.addItem("Lotofácil")
        self.combo_box.addItem("Quina")
        self.combo_box.addItem("Lotomania")
        self.combo_box.addItem("Timemania")
        self.combo_box.addItem("Dupla Sena")
        self.combo_box.addItem("Loteca")
        self.combo_box.addItem("Dia de Sorte")
        self.layout_choose.addWidget(self.combo_box)
        
        self.button = QPushButton("Escolher")
        self.button.clicked.connect(self.choose_game)
        self.layout_choose.addWidget(self.button)
        
        self.label_saved = QLabel("Escolha o jogo salvo:")
        self.layout_saved.addWidget(self.label_saved)
        
        self.refresh_button = QPushButton("Atualizar")
        self.refresh_button.clicked.connect(self.load_saved_games)
        self.layout_saved.addWidget(self.refresh_button)
        
        self.combo_box_saved = QComboBox()
        self.combo_box_saved.addItem("Mega-Sena")
        self.combo_box_saved.addItem("Lotofácil")
        self.combo_box_saved.addItem("Quina")
        self.combo_box_saved.addItem("Lotomania")
        self.combo_box_saved.addItem("Timemania")
        self.combo_box_saved.addItem("Dupla Sena")
        self.combo_box_saved.addItem("Loteca")
        self.combo_box_saved.addItem("Dia de Sorte")
        self.layout_saved.addWidget(self.combo_box_saved)
        
        self.saved_games_container = QWidget()
        self.saved_games_layout = QVBoxLayout()
        self.saved_games_container.setLayout(self.saved_games_layout)
        self.layout_saved.addWidget(self.saved_games_container)
        
        self.load_saved_games()
        
    def choose_game(self):
        game = self.combo_box.currentText()
        if game == "Mega-Sena":
            numbers = self.generate_mega_sena()
            self.save_numbers_csv(game, numbers)
        elif game == "Lotofácil":
            num_choices = self.get_lotofacil_choices()
            if num_choices is not None:
                numbers = self.generate_lotofacil(num_choices)
                self.save_numbers_csv(game, numbers)
            else:
                return
        elif game == "Quina":
            numbers = self.generate_quina()
            self.save_numbers_csv(game, numbers)
        elif game == "Lotomania":
            numbers = self.generate_lotomania()
            self.save_numbers_csv(game, numbers)
        elif game == "Timemania":
            numbers, team = self.get_timemania_numbers_and_team()
            self.save_team(team, game)
            self.save_numbers_csv(game, numbers)
        elif game == "Dupla Sena":
            numbers = self.generate_dupla_sena()
            self.save_numbers_csv(game, numbers)
        elif game == "Loteca":
            results = self.generate_loteca()
            self.save_results_csv(results, game)
        elif game == "Dia de Sorte":
            numbers, month = self.generate_dia_de_sorte()
            self.save_month(month, game)
            self.save_numbers_csv(game, numbers)
        
        self.display_success_message(numbers)
    
    def generate_mega_sena(self):
        return sorted(random.sample(range(1, 61), 6))
    
    def get_lotofacil_choices(self):
        choices, ok = QInputDialog.getInt(self, "Escolha", "Quantos números você deseja escolher? (entre 15 e 20)")
        if ok:
            if choices >= 15 and choices <= 20:
                return choices
            else:
                QMessageBox.warning(self, "Aviso", "Escolha um número entre 15 e 20.")
        return None
    
    def generate_lotofacil(self, num_choices):
        return sorted(random.sample(range(1, 26), num_choices))
    
    def generate_quina(self):
        return sorted(random.sample(range(1, 81), 5))
    
    def generate_lotomania(self):
        return sorted(random.sample(range(1, 101), 50))
    
    def get_timemania_numbers_and_team(self):
        states = {
            "MG": ["América Futebol Clube", "Atlético Mineiro Futebol Clube"],
            "GO": ["Atlético Clube Goianiense", "Goiás Esporte Clube"],
            "SC": ["Avaí Futebol Clube", "Associação Chapecoense de Futebol"],
            "RJ": ["Botafogo de Futebol e Regatas", "Clube de Regatas Flamengo", "Fluminense Football Club"],
            "CE": ["Ceará Sporting Clube", "Fortaleza Esporte Clube"],
            "SP": ["Clube Atlético Bragantino", "Santos Futebol Clube", "São Paulo Futebol Clube", "Sport Club Corinthians Paulista", "Sociedade Esportiva Palmeiras"],
            "PR": ["Coritiba Foot Ball Club", "Clube Atlético Paranaense"],
            "MT": ["Cuiabá Esporte Clube"],
            "RS": ["Esporte Clube Juventude", "Grêmio Foot-Ball Porto Alegrense", "Sport Club Internacional", "Grêmio Esportivo Brasil (Brasil de Pelotas)", "Sociedade Esportiva e Recreativa Caxias do Sul", "Ypiranga Futebol Clube"],
            "PE": ["Clube Náutico Capibaribe", "Sport Club do Recife"],
            "AL": ["CRB Clube de Regatas Brasil", "CSA Centro Sportivo Alagoano"],
            "BA": ["Esporte Clube Bahia", "Esporte Clube Vitória"],
            "PA": ["Clube do Remo", "Paysandu Sport Club"],
            "MA": ["Sampaio Corrêa Futebol Clube", "Sociedade Imperatriz de Desportos"],
            "RN": ["ABC Futebol Clube"],
            "PI": ["Associação Atlética de Altos"],
            "PB": ["Botafogo Futebol Clube", "Campinense Clube", "Treze Futebol Clube"],
            "AM": ["Manaus Futebol Clube"],
            "DF": ["Brasiliense Futebol Clube"],
            "MS": ["Operário Futebol Clube"],
            "RO": ["Real Ariquemes Esporte Clube"],
            "TO": ["Palmas Futebol e Regatas"],
            "AC": ["Atlético Acreano"],
            "AP": ["Ypiranga Clube"],
        }
        states = {key: value for key, value in states.items() if key not in ["RR", "MA"]}  # Remove duplicatas
        state, ok = QInputDialog.getItem(self, "Escolha o estado", "Escolha o estado:", sorted(states.keys()))
        if ok:
            team, ok = QInputDialog.getItem(self, "Escolha o time", "Escolha o time:", states[state])
            if ok:
                numbers = sorted(random.sample(range(1, 81), 10))
                return numbers, team
        return None, None
    
    def generate_dupla_sena(self):
        return sorted(random.sample(range(1, 51), 6))
    
    def generate_loteca(self):
        results = []
        for i in range(14):
            result = random.choice(["1", "2", "X"])
            results.append(result)
        return results
    
    def generate_dia_de_sorte(self):
        numbers = sorted(random.sample(range(1, 32), 7))
        month = random.choice(["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
        return numbers, month
    
    def save_numbers_csv(self, game, numbers):
        with open("lottery_numbers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([game] + numbers)
                
    def save_team(self, team, game):
        with open("lottery_numbers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([game] + [team])
            
    def save_results_csv(self, results, game):
        with open("lottery_numbers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([game] + results)
    
    def save_month(self, month, game):
        with open("lottery_numbers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([game] + [month])

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(", ".join(map(str, text)))

    def display_success_message(self, numbers):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Números gerados com sucesso!")
        msg_box.setInformativeText(f"Números gerados: {numbers}")
        msg_box.addButton("Ok", QMessageBox.AcceptRole)
        copy_button = msg_box.addButton("Copiar para a área de transferência", QMessageBox.ActionRole)
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(numbers))
        msg_box.exec_()
        
    def load_saved_games(self):
        try:
            for i in reversed(range(self.saved_games_layout.count())):
                widget = self.saved_games_layout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)
            
            selected_game = self.combo_box_saved.currentText()
            with open("lottery_numbers.csv", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0].startswith(selected_game):
                        game = row[0]
                        data = ", ".join(row[1:])
                        if game == "Timemania":
                            team = data.split(',')[0]
                            numbers = ", ".join(data.split(',')[1:])
                            game_widget = QWidget()
                            game_layout = QHBoxLayout()
                            game_widget.setLayout(game_layout)
                            label = QLabel(f"{game}: {team} - {numbers}")
                            copy_button = QPushButton("Copiar")
                            copy_button.clicked.connect(lambda _, team=team, numbers=numbers: self.copy_to_clipboard(f"{team} - {numbers}"))
                            game_layout.addWidget(label)
                            game_layout.addWidget(copy_button)
                            self.saved_games_layout.addWidget(game_widget)
                        else:
                            game_widget = QWidget()
                            game_layout = QHBoxLayout()
                            game_widget.setLayout(game_layout)
                            label = QLabel(f"{game}: {data}")
                            copy_button = QPushButton("Copiar")
                            copy_button.clicked.connect(lambda _, numbers=data.split(','): self.copy_to_clipboard(numbers))
                            game_layout.addWidget(label)
                            game_layout.addWidget(copy_button)
                            self.saved_games_layout.addWidget(game_widget)
        except (FileNotFoundError, PermissionError, csv.Error) as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar jogos salvos: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LotteryApp()
    window.show()
    sys.exit(app.exec_())
