import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
import os


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



def plot_results(equipment, dancing, iteration):
    if not os.path.exists('plots'):
        os.makedirs('plots')

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
    plt.savefig(f'plots/fuzzy_result_{iteration}.png')
    plt.close()



def get_valid_equipment_cost():
    while True:
        try:
            cost = float(input("Enter the cost of photography equipment (200-8000 Euro): "))
            if 200 <= cost <= 8000:
                return cost
            else:
                print("Invalid input. Please enter a value between 200 and 8000.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_valid_dancing_percentage():
    while True:
        try:
            percentage = float(input("Enter the percentage of people dancing (0-100%): "))
            if 0 <= percentage <= 100:
                return percentage
            else:
                print("Invalid input. Please enter a value between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")



def main():
    iteration = 1
    while True:
        equipment = get_valid_equipment_cost()
        dancing = get_valid_dancing_percentage()
        
        try:
            result = defuzzify(equipment, dancing)
            print(f"\nPredicted photo quality: {result:.2f}/10")
            
            plot_results(equipment, dancing, iteration)
            print(f"Plot saved as 'plots/fuzzy_result_{iteration}.png'")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Unable to calculate the result or generate the plot.")
        
        iteration += 1
        
        if input("Enter 'q' to quit, or any other key to continue: ").lower() == 'q':
            break

if __name__ == "__main__":
    main()