import tkinter as tk
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_DIR = "pso_scientific_results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

USE_RASTRIGIN = True

def funcao_esfera(posicao_no_dominio):
    x, y = posicao_no_dominio
    return x**2 + y**2

def funcao_rastrigin(posicao_no_dominio):
    x, y = posicao_no_dominio
    return (x**2 - 10 * np.cos(2 * np.pi * x)) + \
           (y**2 - 10 * np.cos(2 * np.pi * y)) + 20

FUNCAO_OBJETIVO = funcao_rastrigin if USE_RASTRIGIN else funcao_esfera

NUM_PARTICULAS = 8
NUM_DIMENSOES = 2

CANVAS_MIN = 0
CANVAS_MAX = 600
CANVAS_SIZE = CANVAS_MAX - CANVAS_MIN

DOMAIN_MIN = -5.12
DOMAIN_MAX = 5.12
DOMAIN_SIZE = DOMAIN_MAX - DOMAIN_MIN

SCALE_CANVAS_TO_DOMAIN = DOMAIN_SIZE / CANVAS_SIZE
SCALE_DOMAIN_TO_CANVAS = CANVAS_SIZE / DOMAIN_SIZE

# PARÂMETRO AJUSTADO: Velocidade Máxima das Partículas no Canvas.
# Mantido para o Cenário 1, mas ajustado no Cenário 2 dentro de run_batch_experiments.
MAX_VELOCIDADE_CANVAS = 5

# PARÂMETRO AJUSTADO: Peso de Inércia Inicial para incentivar explotação mais cedo.
W_INICIAL = 0.8
W_FINAL = 0.4

# PARÂMETROS AJUSTADOS: Componentes Cognitiva e Social para acelerar a convergência.
C1_INICIAL = 2.2
C2_INICIAL = 2.2

MAX_ITERATIONS = 1000
CONVERGENCE_THRESHOLD = 0.05

STAGNATION_CHECK_INTERVAL = 50
STAGNATION_ITERATIONS_THRESHOLD = 100
STAGNATION_DIVERSITY_THRESHOLD = 20
STAGNATION_RESET_COUNT = 4

# PARAMETERS AJUSTED for Scenario 1 within run_batch_experiments
OBSTACLE_REPULSION_FORCE = 50.0 # Placeholder, adjusted per scenario
COLLISION_BOUNCE_FACTOR = 0.7 # Placeholder, adjusted per scenario
CONTOUR_STEERING_FORCE = 40.0 # Placeholder, adjusted per scenario
SENSING_RADIUS = 150 # Placeholder, adjusted per scenario
SENSING_REPULSION_DECAY = 0.1 # Placeholder, adjusted per scenario

# Obstacle coordinates adjusted to ensure more fluid passages.
# Larger openings in corners and increased spacing for central blocks.
OBSTACULOS = [
    # Horizontal walls (x1, y1, x2, y2) - Even larger openings in corners
    {"coords": [0, 155, 60, 185], "id": None},   # Top-Left (shorter)
    {"coords": [540, 155, 600, 185], "id": None}, # Top-Right (shorter)
    {"coords": [0, 415, 60, 445], "id": None},   # Bottom-Left (shorter)
    {"coords": [540, 415, 600, 445], "id": None}, # Bottom-Right (shorter)

    # Vertical walls (x1, y1, x2, y2) - Even larger openings in corners
    {"coords": [155, 0, 185, 60], "id": None},   # Left-Top (shorter)
    {"coords": [155, 540, 185, 600], "id": None}, # Left-Bottom (shorter)
    {"coords": [415, 0, 445, 60], "id": None},   # Right-Top (shorter)
    {"coords": [415, 540, 445, 600], "id": None}, # Right-Bottom (shorter)

    {"coords": [290, 290, 310, 310], "id": None}, # Central block (maintained)

    # Rectangular obstacles around the central block, with even greater spacing and reduced length.
    # Length of 80px, thickness of 30px. Further away for clearer passages.
    {"coords": [285, 160, 315, 240], "id": None}, # Block above center (80px length)
    {"coords": [285, 360, 315, 440], "id": None}, # Block below center (80px length)
    {"coords": [160, 285, 240, 315], "id": None}, # Block to the left of center (80px length)
    {"coords": [360, 285, 440, 315], "id": None}, # Block to the right of center (80px length)
]

def canvas_to_domain(posicao_canvas):
    return (posicao_canvas - CANVAS_MIN) * SCALE_CANVAS_TO_DOMAIN + DOMAIN_MIN

def domain_to_canvas(posicao_domain):
    return (posicao_domain - DOMAIN_MIN) * SCALE_DOMAIN_TO_CANVAS + CANVAS_MIN

class Particula:
    def __init__(self, canvas_ref, raio=5):
        self.canvas = canvas_ref
        self.raio = raio
        
        self.posicao = np.random.uniform(CANVAS_MIN + self.raio, CANVAS_MAX - self.raio, NUM_DIMENSOES)
        
        self.velocidade = np.random.uniform(-MAX_VELOCIDADE_CANVAS, MAX_VELOCIDADE_CANVAS, NUM_DIMENSOES)
        
        self.pbest_posicao = np.copy(self.posicao)
        self.pbest_valor = self._calcular_fitness(self.posicao)

        self.collisions_count = 0

        self.id_grafico = None
        self.pbest_id_grafico = None
        self.trail_id = None
        self.trail_points = []
        
        if self.canvas:
            self.id_grafico = self.canvas.create_oval(
                self.posicao[0] - self.raio, self.posicao[1] - self.raio,
                self.posicao[0] + self.raio, self.posicao[1] + self.raio,
                fill="blue", outline="darkblue"
            )
            self.pbest_id_grafico = self.canvas.create_oval(
                self.pbest_posicao[0] - 2, self.pbest_posicao[1] - 2,
                self.pbest_posicao[0] + 2, self.pbest_posicao[1] + 2,
                fill="green", outline="darkgreen"
            )

    def _calcular_fitness(self, posicao_canvas):
        posicao_dominio = canvas_to_domain(posicao_canvas)
        return FUNCAO_OBJETIVO(posicao_dominio)

    def atualizar_posicao_grafico(self):
        if not self.canvas:
            return
        
        x, y = self.posicao
        self.canvas.coords(
            self.id_grafico,
            x - self.raio, y - self.raio,
            x + self.raio, y + self.raio
        )
        
        px, py = self.pbest_posicao
        self.canvas.coords(
            self.pbest_id_grafico,
            px - 2, py - 2,
            px + 2, py + 2
        )
        
        self.trail_points.append(tuple(self.posicao))
        if len(self.trail_points) > 20:
            self.trail_points.pop(0)

        if self.trail_id:
            self.canvas.coords(self.trail_id, *[coord for point in self.trail_points for coord in point])
        elif len(self.trail_points) > 1:
            self.trail_id = self.canvas.create_line(
                *[coord for point in self.trail_points for coord in point],
                fill="lightblue", width=1.5
            )

    def _detectar_e_desviar_obstaculos(self, obstaculos, gbest_posicao_canvas):
        for obs in obstaculos:
            ox1, oy1, ox2, oy2 = obs["coords"]
            
            closest_x = max(ox1, min(self.posicao[0], ox2))
            closest_y = max(oy1, min(self.posicao[1], oy2))

            distance_vector = self.posicao - np.array([closest_x, closest_y])
            distance = np.linalg.norm(distance_vector)

            if distance < self.raio + SENSING_RADIUS:
                normal = distance_vector / (distance + 1e-6)
                
                if distance < self.raio:
                    self.collisions_count += 1
                    
                    overlap = self.raio - distance
                    self.posicao += normal * (overlap + 1.0)
                    self.velocidade *= COLLISION_BOUNCE_FACTOR
                    
                    if self.canvas:
                        self.canvas.itemconfig(self.id_grafico, fill="red")
                        self.canvas.after(100, lambda: self.canvas.itemconfig(self.id_grafico, fill="blue"))
                
                repulsion_magnitude = OBSTACLE_REPULSION_FORCE * np.exp(-distance * SENSING_REPULSION_DECAY)
                self.velocidade += repulsion_magnitude * normal

                tangent_left = np.array([-normal[1], normal[0]])
                tangent_right = np.array([normal[1], -normal[0]])

                to_gbest = gbest_posicao_canvas - self.posicao
                if np.linalg.norm(to_gbest) > 1e-6:
                    to_gbest = to_gbest / np.linalg.norm(to_gbest)

                dot_left = np.dot(to_gbest, tangent_left)
                dot_right = np.dot(to_gbest, tangent_right)

                if dot_left > dot_right:
                    contour_direction = tangent_left
                else:
                    contour_direction = tangent_right
                
                self.velocidade += CONTOUR_STEERING_FORCE * contour_direction

        self.velocidade = np.clip(self.velocidade, -MAX_VELOCIDADE_CANVAS, MAX_VELOCIDADE_CANVAS)

    def atualizar(self, gbest_posicao_canvas, W_val, C1_val, C2_val, obstaculos):
        r1 = np.random.rand(NUM_DIMENSOES)
        r2 = np.random.rand(NUM_DIMENSOES)

        termo_inercia = W_val * self.velocidade
        termo_cognitivo = C1_val * r1 * (self.pbest_posicao - self.posicao)
        termo_social = C2_val * r2 * (gbest_posicao_canvas - self.posicao)
        
        self.velocidade = termo_inercia + termo_cognitivo + termo_social
        
        self.velocidade = np.clip(self.velocidade, -MAX_VELOCIDADE_CANVAS, MAX_VELOCIDADE_CANVAS)

        self.posicao += self.velocidade
        
        self.posicao = np.clip(self.posicao, CANVAS_MIN + self.raio, CANVAS_MAX - self.raio)
        
        self._detectar_e_desviar_obstaculos(obstaculos, gbest_posicao_canvas)

        valor_atual = self._calcular_fitness(self.posicao)
        if valor_atual < self.pbest_valor:
            self.pbest_valor = valor_atual
            self.pbest_posicao = np.copy(self.posicao)

        self.atualizar_posicao_grafico()


class PSOSimulation:
    def __init__(self, master=None, is_gui_mode=True):
        self.master = master
        self.is_gui_mode = is_gui_mode
        self.running = False
        self.particulas = []
        self.current_iteration = 0
        self.last_gbest_improvement_iteration = 0

        self.gbest_fitness_log = []
        self.distance_to_target_log = []
        self.swarm_diversity_log = []
        self.total_collisions_current_run = 0

        self.gbest_posicao = np.random.uniform(CANVAS_MIN + 50, CANVAS_MAX - 50, NUM_DIMENSOES)
        self.gbest_velocity = np.random.uniform(-1.0, 1.0, NUM_DIMENSOES) * 0.75
        
        self.gbest_valor = float('inf')

        if self.is_gui_mode:
            self.master.title("Simulação PSO Científica Completa com Tkinter")

            self.canvas = tk.Canvas(master, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="lightgray")
            self.canvas.pack(pady=10)

            self.gbest_graphic_id = self.canvas.create_oval(0,0,0,0, fill="yellow", outline="orange")
            
            self.gbest_label = tk.Label(master, text="Melhor Global (gbest): Valor: Inf, Pos: (0.00, 0.00) | Iteração: 0 | Diversidade: N/A | Status: Parado")
            self.gbest_label.pack(pady=5)

            self._desenhar_obstaculos()
            
            self.frame_params = tk.LabelFrame(master, text="Parâmetros PSO")
            self.frame_params.pack(pady=5, padx=10, fill=tk.X)

            self.w_var = tk.DoubleVar(value=W_INICIAL)
            tk.Label(self.frame_params, text="W (Inércia):").pack(side=tk.LEFT, padx=5)
            tk.Scale(self.frame_params, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL,
                     variable=self.w_var, command=self._update_gbest_display).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
            
            self.c1_var = tk.DoubleVar(value=C1_INICIAL)
            tk.Label(self.frame_params, text="C1 (Cognitivo):").pack(side=tk.LEFT, padx=5)
            tk.Scale(self.frame_params, from_=0.0, to=4.0, resolution=0.01, orient=tk.HORIZONTAL,
                     variable=self.c1_var, command=self._update_gbest_display).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

            self.c2_var = tk.DoubleVar(value=C2_INICIAL)
            tk.Label(self.frame_params, text="C2 (Social):").pack(side=tk.LEFT, padx=5)
            tk.Scale(self.frame_params, from_=0.0, to=4.0, resolution=0.01, orient=tk.HORIZONTAL,
                     variable=self.c2_var, command=self._update_gbest_display).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
            
            self.sim_speed_var = tk.IntVar(value=30)
            tk.Label(self.frame_params, text="Velocidade Simulação (ms):").pack(side=tk.LEFT, padx=5)
            tk.Scale(self.frame_params, from_=10, to=200, resolution=10, orient=tk.HORIZONTAL,
                     variable=self.sim_speed_var).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

            self.frame_botoes = tk.Frame(master)
            self.frame_botoes.pack(pady=5)

            self.btn_iniciar = tk.Button(self.frame_botoes, text="Iniciar Simulação", command=self.iniciar_simulacao)
            self.btn_iniciar.pack(side=tk.LEFT, padx=5)

            self.btn_pausar = tk.Button(self.frame_botoes, text="Pausar Simulação", command=self.pausar_simulacao, state=tk.DISABLED)
            self.btn_pausar.pack(side=tk.LEFT, padx=5)

            self.btn_reset = tk.Button(self.frame_botoes, text="Resetar Simulação", command=self.resetar_simulacao)
            self.btn_reset.pack(side=tk.LEFT, padx=5)
        
        self._inicializar_particulas()

    def _reset_metrics(self):
        self.gbest_fitness_log = []
        self.distance_to_target_log = []
        self.swarm_diversity_log = []
        self.total_collisions_current_run = 0
        for p in self.particulas:
            p.collisions_count = 0

    def _print_run_summary(self):
        if not self.current_iteration > 0:
            return

        print("\n--- Resumo da Última Execução da Simulação ---")
        print(f"Função Objetivo: {'Rastrigin' if USE_RASTRIGIN else 'Esfera'}")
        print(f"Iterações Totais: {self.current_iteration}")
        print(f"Fitness Final do Gbest: {self.gbest_valor:.4f}")
        
        total_collisions_this_run = sum(p.collisions_count for p in self.particulas)
        print(f"Colisões Totais Registradas: {total_collisions_this_run}")
        
        if self.swarm_diversity_log:
            avg_diversity = np.mean(self.swarm_diversity_log)
            print(f"Diversidade Média do Enxame: {avg_diversity:.2f}")
        
        if self.distance_to_target_log:
            avg_distance_to_target = np.mean(self.distance_to_target_log)
            print(f"Distância Média ao Alvo em Movimento: {avg_distance_to_target:.2f} pixels")
        print("-------------------------------------------\n")

    def _desenhar_obstaculos(self):
        if not self.canvas:
            return
        for obs in OBSTACULOS:
            obs["id"] = self.canvas.create_rectangle(
                obs["coords"][0], obs["coords"][1], obs["coords"][2], obs["coords"][3],
                fill="gray", outline="black"
            )

    def _inicializar_particulas(self):
        if self.current_iteration > 0 or not self.is_gui_mode:
            self._print_run_summary()
        
        if self.is_gui_mode:
            for p in self.particulas:
                self.canvas.delete(p.id_grafico)
                self.canvas.delete(p.pbest_id_grafico)
                if p.trail_id:
                    self.canvas.delete(p.trail_id)
        self.particulas = []
        
        self.current_iteration = 0
        self.last_gbest_improvement_iteration = 0
        self.gbest_valor = float('inf')

        for _ in range(NUM_PARTICULAS):
            self.particulas.append(Particula(self.canvas if self.is_gui_mode else None))
        
        self._reset_metrics()
        
        if len(self.particulas) > 0:
            self.gbest_posicao = np.array([CANVAS_SIZE / 2, CANVAS_SIZE / 2])
            self.gbest_velocity = np.random.uniform(-1.0, 1.0, NUM_DIMENSOES) * 0.75

        if self.is_gui_mode:
            self._update_gbest_display("Status: Pronto para Iniciar")
            self._update_gbest_graphic()

    def iniciar_simulacao(self):
        if not self.running and self.is_gui_mode:
            self.running = True
            self.btn_iniciar.config(state=tk.DISABLED)
            self.btn_pausar.config(state=tk.NORMAL)
            self._update_gbest_display("Status: Rodando")
            self._loop_simulacao()

    def pausar_simulacao(self):
        if self.running and self.is_gui_mode:
            self.running = False
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_pausar.config(state=tk.DISABLED)
            self._update_gbest_display("Status: Pausado")
            self._print_run_summary()

    def resetar_simulacao(self):
        if self.is_gui_mode:
            self.pausar_simulacao()
            self._inicializar_particulas()
            self._update_gbest_display("Status: Resetado")

    def _calculate_swarm_diversity(self):
        if not self.particulas:
            return 0.0
        
        positions = np.array([p.posicao for p in self.particulas])
        centroid = np.mean(positions, axis=0)
        
        distances = [np.linalg.norm(p.posicao - centroid) for p in self.particulas]
        
        return np.mean(distances) if distances else 0.0

    def _reset_stagnant_particles(self):
        indices_to_reset = np.random.choice(NUM_PARTICULAS, STAGNATION_RESET_COUNT, replace=False)

        for i in indices_to_reset:
            p = self.particulas[i]
            p.posicao = np.random.uniform(CANVAS_MIN + p.raio, CANVAS_MAX - p.raio, NUM_DIMENSOES)
            p.velocidade = np.random.uniform(-MAX_VELOCIDADE_CANVAS, MAX_VELOCIDADE_CANVAS, NUM_DIMENSOES)
            p.pbest_posicao = np.copy(p.posicao)
            p.pbest_valor = p._calcular_fitness(p.posicao)
            if self.is_gui_mode:
                p.atualizar_posicao_grafico()

    def _update_gbest_display(self, status_message=None): 
        if not self.is_gui_mode:
            return

        gbest_pos_domain = canvas_to_domain(self.gbest_posicao)
        current_diversity = self._calculate_swarm_diversity()
        
        display_text = (
            f"Melhor Global (gbest): Valor: {self.gbest_valor:.4f}, "
            f"Pos: ({gbest_pos_domain[0]:.2f}, {gbest_pos_domain[1]:.2f}) | "
            f"Iteração: {self.current_iteration} | "
            f"Diversidade: {current_diversity:.2f}"
        )
        if status_message:
            display_text += f" | Status: {status_message}"
        else:
            display_text += f" | Status: {'Rodando' if self.running else 'Pausado'}"

        self.gbest_label.config(text=display_text)
        self._update_gbest_graphic()

    def _update_gbest_graphic(self):
        if not self.is_gui_mode:
            return

        gx, gy = self.gbest_posicao
        self.canvas.coords(
            self.gbest_graphic_id,
            gx - 6, gy - 6,
            gx + 6, gy + 6
        )
        self.canvas.lift(self.gbest_graphic_id)

    def _perform_one_iteration_step(self):
        self.current_iteration += 1

        current_W = W_INICIAL - (self.current_iteration / MAX_ITERATIONS) * (W_INICIAL - W_FINAL)
        current_W = max(W_FINAL, current_W)
        if self.is_gui_mode: self.w_var.set(current_W)

        current_C1 = self.c1_var.get() if self.is_gui_mode else C1_INICIAL
        current_C2 = self.c2_var.get() if self.is_gui_mode else C2_INICIAL

        self.gbest_posicao += self.gbest_velocity
        
        if self.gbest_posicao[0] <= CANVAS_MIN or self.gbest_posicao[0] >= CANVAS_MAX:
            self.gbest_velocity[0] *= -1
            self.gbest_posicao[0] = np.clip(self.gbest_posicao[0], CANVAS_MIN, CANVAS_MAX)
        if self.gbest_posicao[1] <= CANVAS_MIN or self.gbest_posicao[1] >= CANVAS_MAX:
            self.gbest_velocity[1] *= -1
            self.gbest_posicao[1] = np.clip(self.gbest_posicao[1], CANVAS_MIN, CANVAS_MAX)

        current_swarm_gbest_value = float('inf')
        current_swarm_gbest_pos_canvas = np.array([0.0, 0.0])

        for p in self.particulas:
            if p.pbest_valor < current_swarm_gbest_value:
                current_swarm_gbest_value = p.pbest_valor
                current_swarm_gbest_pos_canvas = np.copy(p.pbest_posicao)
        
        if current_swarm_gbest_value < self.gbest_valor:
            self.gbest_valor = current_swarm_gbest_value
            self.last_gbest_improvement_iteration = self.current_iteration
        
        if self.is_gui_mode: self._update_gbest_display()

        for p in self.particulas:
            p.atualizar(self.gbest_posicao, current_W, current_C1, current_C2, OBSTACULOS)
            self.total_collisions_current_run = sum(pt.collisions_count for pt in self.particulas)

        self.gbest_fitness_log.append(self.gbest_valor)
        
        distance_to_moving_target = np.linalg.norm(current_swarm_gbest_pos_canvas - self.gbest_posicao)
        self.distance_to_target_log.append(distance_to_moving_target)
        
        self.swarm_diversity_log.append(self._calculate_swarm_diversity())
        
        if self.current_iteration >= MAX_ITERATIONS:
            print(f"Simulação (Iter {self.current_iteration}): Máx. Iterações Atingido!")
            return "max_iterations"

        if self.gbest_valor < CONVERGENCE_THRESHOLD:
            print(f"Simulação (Iter {self.current_iteration}): Enxame Convergido (fitness < {CONVERGENCE_THRESHOLD})!")
            return "converged_fitness"

        if distance_to_moving_target < 10.0:
            print(f"Simulação (Iter {self.current_iteration}): Alvo Atingido (distância < 10.0px)!")
            return "target_found"

        if (self.current_iteration - self.last_gbest_improvement_iteration) > STAGNATION_ITERATIONS_THRESHOLD:
            current_diversity = self._calculate_swarm_diversity()
            if current_diversity < STAGNATION_DIVERSITY_THRESHOLD:
                print(f"Alerta (Iter {self.current_iteration}): Estagnação detectada (gbest não melhorou por {STAGNATION_ITERATIONS_THRESHOLD} iterações e baixa diversidade {current_diversity:.2f}). Reiniciando partículas.")
                self._reset_stagnant_particles()
                self.last_gbest_improvement_iteration = self.current_iteration
            
        return "running"

    def _loop_simulacao(self):
        if self.running:
            status = self._perform_one_iteration_step()
            
            if status != "running":
                self.pausar_simulacao()
                if status == "max_iterations": self._update_gbest_display("Status: Máx. Iterações Atingido!")
                elif status == "converged_fitness": self._update_gbest_display("Status: Convergido!")
                elif status == "target_found": self._update_gbest_display("Status: Alvo Atingido!")
                return

            self.master.after(self.sim_speed_var.get(), self._loop_simulacao)

    def run_headless_simulation(self):
        self.running = True
        self._inicializar_particulas()

        status = "running"
        while status == "running" and self.current_iteration < MAX_ITERATIONS:
            status = self._perform_one_iteration_step()

        final_gbest_fitness = self.gbest_valor
        total_iterations = self.current_iteration
        total_collisions = self.total_collisions_current_run
        avg_diversity = np.mean(self.swarm_diversity_log) if self.swarm_diversity_log else 0.0
        avg_distance_to_target = np.mean(self.distance_to_target_log) if self.distance_to_target_log else 0.0

        print(f"Rodada Headless Completa: Fitness={final_gbest_fitness:.4f}, Iter={total_iterations}, Colisões={total_collisions}")

        return {
            "final_gbest_fitness": final_gbest_fitness,
            "total_iterations": total_iterations,
            "total_collisions": total_collisions,
            "avg_swarm_diversity": avg_diversity,
            "avg_distance_to_target": avg_distance_to_target,
            "convergence_status": status,
            "gbest_fitness_log": self.gbest_fitness_log,
            "swarm_diversity_log": self.swarm_diversity_log,
            "distance_to_target_log": self.distance_to_target_log,
        }

NUM_RUNS_PER_SCENARIO = 30

def run_batch_experiments():
    print("\n--- INICIANDO EXPERIMENTOS EM LOTE PARA ARTIGO CIENTÍFICO ---")
    all_experiment_results = []

    experiment_scenarios = [
        {"name": "Cenário 1: PSO Padrão com LDIW e Desvio (Otimizado)",
         "W_init": 0.8, "C1_val": 2.2, "C2_val": 2.2,
         "obstacle_repulsion": 99.0, "contour_steering": 80.0, "sensing_radius": 200, "max_velocity_canvas": 10, "sensing_repulsion_decay": 0.2, "collision_bounce_factor": 0.5},
        
        {"name": "Cenário 2: PSO Padrão SEM Desvio",
         "W_init": 0.7, "C1_val": 2.0, "C2_val": 2.0,
         "obstacle_repulsion": 0.0, "contour_steering": 0.0, "sensing_radius": 0, "max_velocity_canvas": 6, "sensing_repulsion_decay": 0.0, "collision_bounce_factor": 0.7}, 

        {"name": "Cenário 3: C1 Mais Forte (foco no pbest)",
         "W_init": 0.8, "C1_val": 2.2, "C2_val": 1.9,
         "obstacle_repulsion": 90.0, "contour_steering": 70.0, "sensing_radius": 200, "max_velocity_canvas": 10, "sensing_repulsion_decay": 0.2, "collision_bounce_factor": 0.5},
        
        {"name": "Cenário 4: C2 Mais Forte (foco no gbest)",
         "W_init": 0.8, "C1_val": 1.9, "C2_val": 2.2,
         "obstacle_repulsion": 90.0, "contour_steering": 70.0, "sensing_radius": 200, "max_velocity_canvas": 10, "sensing_repulsion_decay": 0.2, "collision_bounce_factor": 0.5},
    ]

    global W_INICIAL, C1_INICIAL, C2_INICIAL, OBSTACLE_REPULSION_FORCE, CONTOUR_STEERING_FORCE, SENSING_RADIUS, MAX_VELOCIDADE_CANVAS, SENSING_REPULSION_DECAY, COLLISION_BOUNCE_FACTOR


    for scenario_idx, scenario in enumerate(experiment_scenarios):
        print(f"\nEXECUTANDO CENÁRIO: {scenario['name']} ({scenario_idx + 1}/{len(experiment_scenarios)})")
        
        # Store original global parameters before overriding for scenario
        W_INICIAL_ORIG = W_INICIAL 
        C1_INICIAL_ORIG = C1_INICIAL
        C2_INICIAL_ORIG = C2_INICIAL
        OBSTACLE_REPULSION_FORCE_ORIG = OBSTACLE_REPULSION_FORCE
        CONTOUR_STEERING_FORCE_ORIG = CONTOUR_STEERING_FORCE
        SENSING_RADIUS_ORIG = SENSING_RADIUS
        MAX_VELOCIDADE_CANVAS_ORIG = MAX_VELOCIDADE_CANVAS
        SENSING_REPULSION_DECAY_ORIG = SENSING_REPULSION_DECAY
        COLLISION_BOUNCE_FACTOR_ORIG = COLLISION_BOUNCE_FACTOR

        # Apply scenario-specific parameters
        W_INICIAL = scenario["W_init"]
        C1_INICIAL = scenario["C1_val"]
        C2_INICIAL = scenario["C2_val"]
        OBSTACLE_REPULSION_FORCE = scenario["obstacle_repulsion"]
        CONTOUR_STEERING_FORCE = scenario["contour_steering"]
        SENSING_RADIUS = scenario["sensing_radius"]
        MAX_VELOCIDADE_CANVAS = scenario["max_velocity_canvas"]
        SENSING_REPULSION_DECAY = scenario["sensing_repulsion_decay"]
        COLLISION_BOUNCE_FACTOR = scenario["collision_bounce_factor"]

        scenario_gbest_fitness_logs = []
        scenario_swarm_diversity_logs = []
        scenario_distance_to_target_logs = []

        for run_num in range(NUM_RUNS_PER_SCENARIO):
            print(f"  Rodada {run_num + 1}/{NUM_RUNS_PER_SCENARIO} para o Cenário '{scenario['name']}'...")
            np.random.seed(run_num)

            sim = PSOSimulation(is_gui_mode=False)
            run_results = sim.run_headless_simulation()

            all_experiment_results.append({
                "scenario_name": scenario["name"],
                "run_number": run_num + 1,
                **run_results
            })

            max_log_len = MAX_ITERATIONS
            scenario_gbest_fitness_logs.append(
                run_results["gbest_fitness_log"] + [np.nan] * (max_log_len - len(run_results["gbest_fitness_log"]))
            )
            scenario_swarm_diversity_logs.append(
                run_results["swarm_diversity_log"] + [np.nan] * (max_log_len - len(run_results["swarm_diversity_log"]))
            )
            scenario_distance_to_target_logs.append(
                run_results["distance_to_target_log"] + [np.nan] * (max_log_len - len(run_results["distance_to_target_log"]))
            )
        
        avg_gbest_fitness = np.nanmean(scenario_gbest_fitness_logs, axis=0)
        std_gbest_fitness = np.nanstd(scenario_gbest_fitness_logs, axis=0)

        avg_swarm_diversity = np.nanmean(scenario_swarm_diversity_logs, axis=0)
        std_swarm_diversity = np.nanstd(scenario_swarm_diversity_logs, axis=0)

        avg_distance_to_target = np.nanmean(scenario_distance_to_target_logs, axis=0)
        std_distance_to_target = np.nanstd(scenario_distance_to_target_logs, axis=0)

        all_experiment_results.append({
            "scenario_name": scenario["name"],
            "run_number": "AVERAGE",
            "scenario_type": "average_log",
            "gbest_fitness_log": avg_gbest_fitness.tolist(),
            "std_gbest_fitness_log": std_gbest_fitness.tolist(),
            "swarm_diversity_log": avg_swarm_diversity.tolist(),
            "std_swarm_diversity_log": std_swarm_diversity.tolist(),
            "distance_to_target_log": avg_distance_to_target.tolist(),
            "std_distance_to_target_log": std_distance_to_target.tolist(),
            "final_gbest_fitness": avg_gbest_fitness[-1] if len(avg_gbest_fitness) > 0 else np.nan,
            "total_iterations": MAX_ITERATIONS,
            "total_collisions": np.nan, # Collisions for average log are not directly meaningful here
            "avg_swarm_diversity": np.nanmean(avg_swarm_diversity),
            "avg_distance_to_target": np.nanmean(avg_distance_to_target)
        })
        
        # Restore original global parameters
        W_INICIAL = W_INICIAL_ORIG
        C1_INICIAL = C1_INICIAL_ORIG
        C2_INICIAL = C2_INICIAL_ORIG
        OBSTACLE_REPULSION_FORCE = OBSTACLE_REPULSION_FORCE_ORIG
        CONTOUR_STEERING_FORCE = CONTOUR_STEERING_FORCE_ORIG
        SENSING_RADIUS = SENSING_RADIUS_ORIG
        MAX_VELOCIDADE_CANVAS = MAX_VELOCIDADE_CANVAS_ORIG
        SENSING_REPULSION_DECAY = SENSING_REPULSION_DECAY_ORIG
        COLLISION_BOUNCE_FACTOR = COLLISION_BOUNCE_FACTOR_ORIG


    print("\n--- INICIANDO ANÁLISE DE DADOS E GERAÇÃO DE GRÁFICOS ---")
    df_results = pd.DataFrame(all_experiment_results)
    
    df_results.to_csv(os.path.join(RESULTS_DIR, "scientific_pso_results.csv"), index=False)
    print(f"Todos os resultados detalhados (brutos e médios) salvos em: {os.path.join(RESULTS_DIR, 'scientific_pso_results.csv')}")

    summary_results = df_results[df_results['scenario_type'] != 'average_log'].groupby("scenario_name").agg({
        "final_gbest_fitness": ["mean", "std"],
        "total_iterations": ["mean", "std"],
        "total_collisions": ["mean", "std"],
        "avg_swarm_diversity": ["mean", "std"],
        "avg_distance_to_target": ["mean", "std"]
    })
    print("\n--- Resumo Estatístico por Cenário ---")
    print(summary_results)

    plot_convergence_curves(df_results, "gbest_fitness_log", "Gbest Fitness (Média)", "Curva de Convergência do Gbest")
    plot_convergence_curves(df_results, "swarm_diversity_log", "Diversidade do Enxame (Média)", "Diversidade do Enxame ao Longo das Iterações")
    plot_convergence_curves(df_results, "distance_to_target_log", "Distância ao Alvo (Média)", "Capacidade de Rastreamento do Alvo Dinâmico")
    plot_collision_bar_chart(df_results)
    
    print(f"\nResultados e gráficos salvos no diretório: {RESULTS_DIR}")
    print("--- EXPERIMENTOS CONCLUÍDOS ---")


def plot_convergence_curves(df, log_column_name, y_label, title):
    plt.figure(figsize=(10, 6))
    
    avg_logs_df = df[df['scenario_type'] == 'average_log']

    for index, row in avg_logs_df.iterrows():
        scenario_name = row["scenario_name"]
        
        avg_data = np.array(row[log_column_name])
        if log_column_name == "gbest_fitness_log":
            std_data = np.array(row["std_gbest_fitness_log"])
        elif log_column_name == "swarm_diversity_log":
            std_data = np.array(row["std_swarm_diversity_log"])
        elif log_column_name == "distance_to_target_log":
            std_data = np.array(row["std_distance_to_target_log"])
        else:
            std_data = np.zeros_like(avg_data) 

        valid_indices = ~np.isnan(avg_data)
        avg_data = avg_data[valid_indices]
        std_data = std_data[valid_indices]
        iterations = np.arange(1, len(avg_data) + 1)

        plt.plot(iterations, avg_data, label=scenario_name)
        plt.fill_between(iterations, avg_data - std_data, avg_data + std_data, alpha=0.2)

    plt.xlabel("Iteração")
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, f"{title.replace(' ', '_').replace(':', '')}.png"))
    plt.close()

def plot_collision_bar_chart(df):
    collision_summary = df[df['scenario_type'] != 'average_log'].groupby("scenario_name")["total_collisions"].agg(["mean", "std"]).reset_index()

    plt.figure(figsize=(10, 6))
    plt.bar(collision_summary["scenario_name"], collision_summary["mean"],
            yerr=collision_summary["std"], capsize=5, label="Colisões Médias")
    
    plt.xlabel("Cenário de Experimento")
    plt.ylabel("Número Médio de Colisões")
    plt.title("Comparação do Número Médio de Colisões por Cenário")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "Comparacao_Colisoes.png"))
    plt.close()


if __name__ == "__main__":
    print("Selecione o modo de execução da Simulação PSO:")
    print("1. Modo GUI (Visualização Interativa)")
    print("2. Modo de Experimentos em Lote (Coleta de Dados e Análise Científica)")
    
    choice = input("Digite 1 ou 2: ")

    if choice == '1':
        root = tk.Tk()
        sim = PSOSimulation(root, is_gui_mode=True)
        root.mainloop()
    elif choice == '2':
        run_batch_experiments()
    else:
        print("Escolha inválida. Por favor, digite 1 ou 2.")
