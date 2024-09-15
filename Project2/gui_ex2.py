import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


def equipment_cheap(x):
    return np.interp(x, [200, 3000], [1, 0])

def equipment_mid_range(x):
    return np.interp(x, [600, 3000, 5000], [0, 1, 0])

def equipment_expensive(x):
    return np.interp(x, [3000, 5000, 7000, 8000], [0, 0.6, 0.9, 1])

def people_not_dancing(x):
    return np.interp(x, [0, 40], [1, 0])

def people_dancing(x):
    return np.interp(x, [30, 80, 100], [0, 0.5, 1])

def photos_bad(x):
    return np.interp(x, [0, 3, 5], [1, 0.7, 0])

def photos_ok(x):
    return np.interp(x, [3, 5, 7], [0, 1, 0])

def photos_good(x):
    return np.interp(x, [6, 8, 10], [0, 0.8, 1])


def rule1(equipment, dancing):
    return min(equipment_cheap(equipment), people_not_dancing(dancing))

def rule2(equipment, dancing):
    return equipment_mid_range(equipment)

def rule3(equipment, dancing):
    return min(equipment_expensive(equipment), people_dancing(dancing))


def aggregated_shape(x, equipment, dancing):
    return max(
        min(rule1(equipment, dancing), photos_bad(x)),
        min(rule2(equipment, dancing), photos_ok(x)),
        min(rule3(equipment, dancing), photos_good(x))
    )

def defuzzify(equipment, dancing):
    def x_times_shape(x):
        return x * aggregated_shape(x, equipment, dancing)
    
    numerator, _ = quad(x_times_shape, 0, 10, limit=1000)
    denominator, _ = quad(lambda x: aggregated_shape(x, equipment, dancing), 0, 10, limit=1000)
    
    epsilon = 1e-10
    if denominator < epsilon:
        return 0
    return numerator / denominator


def plot_results(equipment, dancing):
    plt.figure(figsize=(12, 8))
    x_equipment = np.linspace(200, 8000, 1000)
    x_dancing = np.linspace(0, 100, 1000)
    x_photos = np.linspace(0, 10, 1000)

    plt.subplot(2, 2, 1)
    plt.plot(x_equipment, [equipment_cheap(x) for x in x_equipment], label='Cheap')
    plt.plot(x_equipment, [equipment_mid_range(x) for x in x_equipment], label='Mid-range')
    plt.plot(x_equipment, [equipment_expensive(x) for x in x_equipment], label='Expensive')
    plt.title('Equipment Cost Membership')
    plt.xlabel('Cost (Euro)')
    plt.ylabel('Membership Degree')
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(x_dancing, [people_not_dancing(x) for x in x_dancing], label='Not Dancing')
    plt.plot(x_dancing, [people_dancing(x) for x in x_dancing], label='Dancing')
    plt.title('Dancing People Membership')
    plt.xlabel('Percentage of People Dancing')
    plt.ylabel('Membership Degree')
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(x_photos, [photos_bad(x) for x in x_photos], label='Bad')
    plt.plot(x_photos, [photos_ok(x) for x in x_photos], label='OK')
    plt.plot(x_photos, [photos_good(x) for x in x_photos], label='Good')
    plt.title('Photo Quality Membership')
    plt.xlabel('Photo Quality')
    plt.ylabel('Membership Degree')
    plt.legend()

    plt.subplot(2, 2, 4)
    x = np.linspace(0, 10, 1000)
    y = [aggregated_shape(xi, equipment, dancing) for xi in x]
    plt.plot(x, y)
    plt.title(f"Aggregated Fuzzy Set\n(Equipment: €{equipment}, Dancing: {dancing}%)")
    plt.xlabel("Photo Quality")
    plt.ylabel("Membership Degree")
    defuzzified_value = defuzzify(equipment, dancing)
    plt.axvline(x=defuzzified_value, color='r', linestyle='--', label=f'Defuzzified Value: {defuzzified_value:.2f}')
    plt.legend()

    plt.tight_layout()
    return plt


class FuzzyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fuzzy Logic Photo Quality Prediction")
        self.geometry("1000x800")

        self.label1 = tk.Label(self, text="Equipment Cost (200-8000 Euro)")
        self.label1.pack()

        self.slider_equipment = tk.Scale(self, from_=200, to=8000, orient=tk.HORIZONTAL, resolution=100)
        self.slider_equipment.pack()

        self.label2 = tk.Label(self, text="Percentage of People Dancing (0-100%)")
        self.label2.pack()

        self.slider_dancing = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, resolution=1)
        self.slider_dancing.pack()

        self.button = tk.Button(self, text="Predict and Plot", command=self.predict_and_plot)
        self.button.pack()

        self.canvas = None

    def predict_and_plot(self):
        equipment = self.slider_equipment.get()
        dancing = self.slider_dancing.get()
        result = defuzzify(equipment, dancing)
        self.display_result(result)
        self.plot_figure(equipment, dancing)

    def display_result(self, result):
        result_text = f"Predicted photo quality: {result:.2f}/10"
        if hasattr(self, 'result_label'):
            self.result_label.config(text=result_text)
        else:
            self.result_label = tk.Label(self, text=result_text)
            self.result_label.pack()

    def plot_figure(self, equipment, dancing):
        plt = plot_results(equipment, dancing)

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

if __name__ == "__main__":
    app = FuzzyApp()
    app.mainloop()
