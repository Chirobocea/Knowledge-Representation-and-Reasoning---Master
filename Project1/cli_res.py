import janus_swi as janus

def run_prolog_test(test_name, mapping):
    print(f"Running test: {mapping[test_name]}...")
    try:
        janus.query_once(test_name)
    
    except Exception as e:
        print(f"Error running {test_name}: {e}")

def create_and_query_kb(test_name):
    try:
        query = input("Enter your query for the default KB: ")

        test_name += f"({query})"

        print("Querying your custom KB...")
        janus.query_once(test_name)

    except Exception as e:
        print(f"Error creating or querying custom KB: {e}")

def main():
    try:
        janus.consult("res.pl")
    except Exception as e:
        print(f"Error consulting Prolog file: {e}")
        return
    
    mapping = {
        "test1": "[[not(a), b], [c, d], [not(d), b], [not(c), b], [not(b)]]",
        "test2": "[[not(b), a], [not(a), b, e], [a, not(e)], [not(a)], [e]]",
        "test3": "[[not(a), b], [c, f], [not(c)], [not(f), b], [not(c), b]]",
        "test4": "[[a, b], [not(a), not(b)]]",
        "test_kb_default": "[happy(emma)]",
        "test_own_query": ""
    }

    tests = ["test1", "test2", "test3", "test4", "test_kb_default", "test_own_query"]

    print("Prolog Resolution Interface")
    print("============================")
    print("Available Tests:")
    for i, test in enumerate(tests, 1):
        print(f"{i}. {test} {mapping[test]}")

    while True:
        print("\nOptions:")
        print("1-5: Run a predefined test")
        print("6: Create and query your custom KB")
        print("q: Quit")

        choice = input("Enter the option number (or 'q' to quit): ").strip()

        if choice.lower() == 'q':
            break
        elif choice == '6':
            create_and_query_kb(tests[5])
        else:
            try:
                test_index = int(choice) - 1
                if 0 <= test_index < len(tests):
                    run_prolog_test(tests[test_index], mapping)
                else:
                    print("Invalid test number. Please try again.")
            except ValueError:
                print("Please enter a valid number or 'q' to quit.")

    print("Exiting...")

if __name__ == "__main__":
    main()
