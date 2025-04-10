import tkinter as tk
import threading
import random
import time
from tkinter import ttk  # Importar ttk para usar Progressbar
from matplotlib.figure import Figure  # Importar Figure para la gráfica
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Integrar matplotlib con tkinter

class Proceso:
    def __init__(self, id, prioridad, tiempo_ejecucion, ciclo_ejecucion):
        """
        Inicializa un proceso con sus características principales
        
        Args:
            id (int): Identificador único del proceso
            prioridad (int): Nivel de prioridad del proceso
            tiempo_ejecucion (int): Tiempo total de ejecución
            ciclo_ejecucion (int): Ciclo de ejecución del proceso
        """
        self.id = id
        self.prioridad = prioridad
        self.tiempo_ejecucion = tiempo_ejecucion
        self.ciclo_ejecucion = ciclo_ejecucion
        
        # Estados del proceso
        self.estados = {
            'Nuevo': False,
            'Listo': False,
            'Ejecutando': False,
            'Bloqueado': False,
            'Terminado': False
        }
        
        # Recursos asignados
        self.nucleo = None
        self.hilo = None
        self.memoria_asignada = 0
        
    def simular_proceso(self):
        """
        Simula el ciclo de vida completo del proceso
        """
        # Transición de estados
        self.estados['Nuevo'] = True
        time.sleep(random.uniform(0.5, 2))
        
        self.estados['Nuevo'] = False
        self.estados['Listo'] = True
        time.sleep(random.uniform(0.5, 2))
        
        self.estados['Listo'] = False
        self.estados['Ejecutando'] = True
        time.sleep(self.tiempo_ejecucion)
        
        self.estados['Ejecutando'] = False
        self.estados['Bloqueado'] = True
        time.sleep(random.uniform(0.5, 2))
        
        self.estados['Bloqueado'] = False
        self.estados['Terminado'] = True

class SimuladorProcesador:
    def __init__(self, num_procesos=3):
        """
        Inicializa el simulador con un número determinado de procesos
        
        Args:
            num_procesos (int): Número de procesos a simular
        """
        self.procesos = []
        self.crear_procesos(num_procesos)
        
        # Lock para controlar el acceso al estado "Ejecutando"
        self.lock_ejecucion = threading.Lock()
        
        # Configuración de la ventana principal
        self.root = tk.Tk()
        self.root.title("Simulador de Procesos de Procesador")
        
        # Frame para mostrar estados de procesos
        self.frame_estados = tk.Frame(self.root)
        self.frame_estados.pack(padx=10, pady=10)
        
        # Etiquetas y barras de progreso para mostrar estados
        self.labels_estados = []
        self.progress_bars = []
        self.info_labels = []  # Etiquetas adicionales para información del proceso
        
        # Crear la figura para la gráfica
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Tiempo de Ejecución de Procesos")
        self.ax.set_xlabel("ID del Proceso")
        self.ax.set_ylabel("Tiempo de Ejecución (s)")
        
        # Canvas para mostrar la gráfica en la ventana de tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(pady=10)
        
        # Botón para iniciar la simulación
        self.boton_iniciar = tk.Button(
            self.root, 
            text="Iniciar Simulación", 
            command=self.iniciar_simulacion
        )
        self.boton_iniciar.pack(pady=10)
    
    def crear_procesos(self, num_procesos):
        """
        Genera procesos con características aleatorias y prioridades únicas
        
        Args:
            num_procesos (int): Número de procesos a crear
        """
        prioridades = list(range(1, num_procesos + 1))  # Generar prioridades únicas
        random.shuffle(prioridades)  # Mezclar las prioridades para asignarlas aleatoriamente

        for i in range(num_procesos):
            proceso = Proceso(
                id=i + 1,
                prioridad=prioridades[i],  # Asignar prioridad única
                tiempo_ejecucion=random.uniform(1, 5),
                ciclo_ejecucion=random.randint(1, 10)
            )
            proceso.nucleo = random.randint(1, 4)  # Núcleo aleatorio (1-4)
            proceso.hilo = random.randint(1, 8)  # Hilo aleatorio (1-8)
            proceso.memoria_asignada = random.randint(100, 1000)  # Memoria aleatoria (100-1000 MB)
            self.procesos.append(proceso)

    def iniciar_simulacion(self):
        """
        Inicia la simulación de procesos en hilos separados
        """
        # Vacía todas las listas de control para reiniciar la simulación desde cero
        self.procesos = []
        # Elimina todas las referencias a las etiquetas que muestran el estado de los procesos
        self.labels_estados = []
        # Elimina todas las referencias a las barras de progreso
        self.progress_bars = []
        # Elimina todas las referencias a las etiquetas que muestran información adicional
        self.info_labels = []
        # Destruye el frame que contiene todos los elementos visuales de los procesos anteriores
        self.frame_estados.destroy()
        # Crea un nuevo frame vacío para albergar los nuevos elementos visuales
        self.frame_estados = tk.Frame(self.root)
        # Coloca el nuevo frame en la ventana con un margen interno de 10 píxeles
        self.frame_estados.pack(padx=10, pady=10)

        # Crea nuevos procesos, usando la cantidad anterior o 3 por defecto si no había ninguno
        self.crear_procesos(len(self.procesos) or 3)

        # Ordena los procesos según su prioridad, donde valores menores indican mayor prioridad
        # La función lambda extrae el atributo "prioridad" de cada proceso para la comparación
        self.procesos.sort(key=lambda p: p.prioridad)

        # Itera sobre cada proceso para crear su representación visual en la interfaz
        for proceso in self.procesos:
            # Crea una etiqueta que muestra el ID del proceso y su estado inicial
            label = tk.Label(self.frame_estados, text=f"Proceso {proceso.id}: Estado Inicial")
            # Coloca la etiqueta en el frame
            label.pack()
            # Almacena la referencia a la etiqueta para actualizarla después
            self.labels_estados.append(label)

            # Crea una barra de progreso para visualizar el avance del proceso
            # length=200: ancho de 200 píxeles
            # mode='determinate': la barra se llena gradualmente
            # maximum=5: valor máximo que representa los 5 estados posibles
            progress = ttk.Progressbar(self.frame_estados, length=200, mode='determinate', maximum=5)
            # Coloca la barra de progreso con un espacio vertical de 5 píxeles
            progress.pack(pady=5)
            # Almacena la referencia a la barra para actualizarla después
            self.progress_bars.append(progress)

            # Crea una etiqueta que muestra información detallada del proceso:
            # - Prioridad asignada al proceso
            # - Cantidad de memoria asignada en megabytes
            # - Número de hilo asignado
            # - Número de núcleo asignado
            info_label = tk.Label(
                self.frame_estados,
                text=f"Prioridad: {proceso.prioridad} | Memoria: {proceso.memoria_asignada} MB | "
                     f"Hilo: {proceso.hilo} | Núcleo: {proceso.nucleo}"
            )
            # Coloca la etiqueta de información en el frame
            info_label.pack()
            # Almacena la referencia a la etiqueta de información para actualizarla después
            self.info_labels.append(info_label)

        # Iniciar la simulación
        for i, proceso in enumerate(self.procesos):
            thread = threading.Thread(
                target=self.simular_proceso_con_actualizacion,
                args=(proceso, i)
            )
            thread.start()

    def actualizar_grafica(self):
        """
        Actualiza la gráfica con los tiempos de ejecución de los procesos en tiempo real
        Mostrando tanto tiempos estimados como tiempos reales acumulados
        """
        # Limpiar la gráfica anterior
        self.ax.clear()
        self.ax.set_title("Progreso de Ejecución de Procesos")
        self.ax.set_xlabel("ID del Proceso")
        self.ax.set_ylabel("Tiempo (s)")
        
        ids = [proceso.id for proceso in self.procesos]
        tiempos_estimados = [proceso.tiempo_ejecucion for proceso in self.procesos]
        
        # Recopilar tiempos reales (usar 0 si aún no hay tiempo acumulado)
        tiempos_reales = []
        for proceso in self.procesos:
            if hasattr(proceso, 'tiempo_ejecucion_real'):
                tiempos_reales.append(proceso.tiempo_ejecucion_real)
            else:
                tiempos_reales.append(0)  # Si aún no tiene tiempo acumulado
        
        # Dibujar barras para los tiempos estimados (en azul claro)
        self.ax.bar(ids, tiempos_estimados, alpha=0.4, color='lightblue', label='Tiempo Estimado')
        
        # Dibujar barras para los tiempos reales (en azul oscuro)
        self.ax.bar(ids, tiempos_reales, alpha=0.7, color='blue', label='Tiempo Ejecutado')
        
        # Añadir valores encima de las barras
        for i, (est, real) in enumerate(zip(tiempos_estimados, tiempos_reales)):
            # Mostrar tiempo estimado
            self.ax.text(ids[i], est + 0.1, f"{est:.2f}s", ha='center', va='bottom', fontsize=8)
            
            # Mostrar tiempo real si es > 0
            if real > 0:
                self.ax.text(ids[i], real/2, f"{real:.2f}s", ha='center', va='center', 
                             fontsize=8, color='white', fontweight='bold')
                
                # Mostrar porcentaje completado
                porcentaje = (real / est) * 100
                if porcentaje > 10:  # Solo mostrar si hay espacio suficiente
                    self.ax.text(ids[i], 0.1, f"{porcentaje:.1f}%", ha='center', 
                                va='bottom', fontsize=7, color='black')
        
        # Ajustar el rango del eje y para mostrar claramente todos los valores
        max_tiempo = max(max(tiempos_estimados), max(tiempos_reales) if tiempos_reales else 0) * 1.2
        self.ax.set_ylim(0, max_tiempo)
        
        # Establecer ticks específicos para el eje x (solo los IDs de procesos)
        self.ax.set_xticks(ids)
        
        # Añadir leyenda
        self.ax.legend(loc='upper right')
        
        # Añadir cuadrícula para mejor legibilidad
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Actualizar el canvas
        self.canvas.draw()
    
    def simular_proceso_con_actualizacion(self, proceso, index):
        """
        Simula el proceso y actualiza la interfaz gráfica
        Con ciclos alternados entre Ejecutando y Bloqueado
        
        Args:
            proceso (Proceso): Proceso a simular
            index (int): Índice del proceso para actualizar etiqueta
        """
        # Inicializar tiempo acumulado de ejecución
        tiempo_final_acumulado = 0
        tiempo_estimado_total = proceso.tiempo_ejecucion
        
        # Establecer el proceso como Nuevo
        for key in proceso.estados:
            proceso.estados[key] = False
        proceso.estados['Nuevo'] = True
        
        # Actualizar la interfaz para el estado Nuevo
        self.labels_estados[index].config(text=f"Proceso {proceso.id}: Nuevo")
        self.progress_bars[index]['value'] = 1
        self.info_labels[index].config(
            text=f"Prioridad: {proceso.prioridad} | Memoria: {proceso.memoria_asignada} MB | "
                 f"Hilo: {proceso.hilo} | Núcleo: {proceso.nucleo} | "
                 f"Tiempo estimado: {tiempo_estimado_total:.2f} s"
        )
        self.root.update_idletasks()
        time.sleep(random.uniform(0.5, 1))
        
        # Cambiar a estado Listo
        for key in proceso.estados:
            proceso.estados[key] = False
        proceso.estados['Listo'] = True
        
        # Actualizar la interfaz para el estado Listo
        self.labels_estados[index].config(text=f"Proceso {proceso.id}: Listo")
        self.progress_bars[index]['value'] = 2
        self.root.update_idletasks()
        time.sleep(random.uniform(0.5, 1))
        
        # Determinar cuántos ciclos de ejecución-bloqueo habrá (entre 2 y 4)
        num_ciclos = random.randint(2, 4)
        
        # Calcular el tiempo por ciclo dividiendo el tiempo total estimado
        tiempo_por_ciclo = tiempo_estimado_total / num_ciclos
        
        # Realizar ciclos alternados de Ejecutando y Bloqueado
        for ciclo in range(num_ciclos):
            # Estado Ejecutando
            for key in proceso.estados:
                proceso.estados[key] = False
            proceso.estados['Ejecutando'] = True
            
            # Actualizar la interfaz para el estado Ejecutando
            self.labels_estados[index].config(
                text=f"Proceso {proceso.id}: Ejecutando (Ciclo {ciclo+1}/{num_ciclos})"
            )
            self.progress_bars[index]['value'] = 3
            self.info_labels[index].config(
                text=f"Prioridad: {proceso.prioridad} | Memoria: {proceso.memoria_asignada} MB | "
                     f"Hilo: {proceso.hilo} | Núcleo: {proceso.nucleo} | "
                     f"Tiempo estimado: {tiempo_estimado_total:.2f} s | "
                     f"Progreso: {(tiempo_final_acumulado/tiempo_estimado_total)*100:.1f}%"
            )
            self.root.update_idletasks()
            
            # Ajustar el tiempo de ejecución según la prioridad
            tiempo_actual = tiempo_por_ciclo / proceso.prioridad
            start_time = time.time()
            time.sleep(tiempo_actual)
            tiempo_ciclo = time.time() - start_time
            tiempo_final_acumulado += tiempo_ciclo
            
            # Si es el último ciclo, no entrar a estado bloqueado
            if ciclo < num_ciclos - 1:
                # Estado Bloqueado
                for key in proceso.estados:
                    proceso.estados[key] = False
                proceso.estados['Bloqueado'] = True
                
                # Actualizar la interfaz para el estado Bloqueado
                self.labels_estados[index].config(
                    text=f"Proceso {proceso.id}: Bloqueado (Después del ciclo {ciclo+1})"
                )
                self.progress_bars[index]['value'] = 4
                self.info_labels[index].config(
                    text=f"Prioridad: {proceso.prioridad} | Memoria: {proceso.memoria_asignada} MB | "
                         f"Hilo: {proceso.hilo} | Núcleo: {proceso.nucleo} | "
                         f"Tiempo estimado: {tiempo_estimado_total:.2f} s | "
                         f"Progreso: {(tiempo_final_acumulado/tiempo_estimado_total)*100:.1f}%"
                )
                self.root.update_idletasks()
                
                # Bloqueo por un tiempo aleatorio corto
                time.sleep(random.uniform(0.3, 1))
                
                # Volver al estado Listo antes del siguiente ciclo de ejecución
                for key in proceso.estados:
                    proceso.estados[key] = False
                proceso.estados['Listo'] = True
                
                # Actualizar la interfaz para el estado Listo intermedio
                self.labels_estados[index].config(
                    text=f"Proceso {proceso.id}: Listo (Para ciclo {ciclo+2})"
                )
                self.progress_bars[index]['value'] = 2
                self.root.update_idletasks()
                time.sleep(random.uniform(0.2, 0.5))
        
        # Estado Terminado
        for key in proceso.estados:
            proceso.estados[key] = False
        proceso.estados['Terminado'] = True
        
        # Actualizar la interfaz para el estado Terminado
        self.labels_estados[index].config(text=f"Proceso {proceso.id}: Terminado")
        self.progress_bars[index]['value'] = 5
        self.info_labels[index].config(
            text=f"Prioridad: {proceso.prioridad} | Memoria: {proceso.memoria_asignada} MB | "
                 f"Hilo: {proceso.hilo} | Núcleo: {proceso.nucleo} | "
                 f"Tiempo estimado: {tiempo_estimado_total:.2f} s | "
                 f"Tiempo real: {tiempo_final_acumulado:.2f} s"
        )
        
        # Almacenar el tiempo real de ejecución para la gráfica
        proceso.tiempo_ejecucion_real = tiempo_final_acumulado
        
        # Actualizar la gráfica con los tiempos reales
        self.actualizar_grafica()

# Ejecutar la simulación
if __name__ == "__main__":
    simulador = SimuladorProcesador(num_procesos=3)
    simulador.root.mainloop()