def print_menu():
    print("\t\tGIN RUMMY\t\t")
    print("\t1. New Game")
    print("\t2. Rules")
    print("\t3. Quit")

def main():
    while True:
        print_menu()
        choice = input("> ").strip()
        if choice == "1":
            print("Starting game...")
        elif choice == "2":
            print("Print the rules here...")
        elif choice == "3":
            print("Quitting game...")
            break
        else:
            print("Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()