import janus_swi as janus
import tkinter as tk
from tkinter import ttk
import sys
import io

class RedirectText(io.StringIO):
    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)

    def flush(self):
        pass

def run_prolog_test(test_name, mode, mapping, result_text):
    result_text.delete(1.0, tk.END) 
    query = f"{test_name}_{mode}"
    result_text.insert(tk.END, f"Running {query}...\n")
    try:
        janus.query_once(query)
        
    except Exception as e:
        print(f"Error running {query}: {e}\n")

    finally:
        sys.stdout = sys.__stdout__

def main():
    try:
        janus.consult("sat.pl")
    except Exception as e:
        print(f"Error consulting Prolog file: {e}")
        return

    mapping = {
        "test1": "[[toddler], [not(toddler), child], [not(child), not(male), boy], [not(infant), child], [not(child), not(female), girl], [female], [girl]]",
        "test2": "[[toddler], [not(toddler), child], [not(child), not(male), boy], [not(infant), child], [not(child), not(female), girl], [female], [not(girl)]]",
        "test3": "[[not(a), b], [c, d], [not(d), b], [not(c), b], [not(b)], [e], [a, b, not(f), f]]",
        "test4": "[[not(b), a], [not(a), b, e], [e], [a, not(e)], [not(a)]]",
        "test5": "[[not(a), not(e), b], [not(d), e, not(b)], [not(e), f, not(b)], [f, not(a), e], [e, f, not(b)]]",
        "test6": "[[a, b], [not(a), not(b)], [not(a), b], [a, not(b)]]"
    }

    tests = ["test1", "test2", "test3", "test4", "test5", "test6"]
    modes = ["mostbalanced", "mostfrequent"]


    root = tk.Tk()
    root.title("Prolog SAT Solver Interface")
    root.geometry("600x400")
    

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Select a Test Case:").grid(row=0, column=0, padx=5, pady=5)

    selected_test = tk.StringVar()
    test_combobox = ttk.Combobox(frame, textvariable=selected_test, values=tests, state="readonly")
    test_combobox.grid(row=0, column=1, padx=5, pady=5)
    test_combobox.current(0)

    ttk.Label(frame, text="Select a Mode:").grid(row=1, column=0, padx=5, pady=5)

    selected_mode = tk.StringVar()
    mode_combobox = ttk.Combobox(frame, textvariable=selected_mode, values=modes, state="readonly")
    mode_combobox.grid(row=1, column=1, padx=5, pady=5)
    mode_combobox.current(0)

    run_button = ttk.Button(frame, text="Run Test", command=lambda: run_prolog_test(selected_test.get(), selected_mode.get(), mapping, result_text))
    run_button.grid(row=2, column=0, columnspan=2, pady=10)

    result_text = tk.Text(root, wrap="word", height=15, width=70)
    result_text.grid(row=1, column=0, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()