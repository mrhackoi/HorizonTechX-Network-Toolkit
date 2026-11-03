
def main():

    while True:
        print("\n" + "=" * 45)
        print(" HORIZON TECHX - NETWORK TOOLKIT")
        print("=" * 45)

        print("1. CLI Mode")
        print("2. GUI Mode")
        print("3. Exit")

        choice = input("\nSelect mode: ").strip()

        if choice == "1":
            try:
                from cli import show_cli
                show_cli()

            except ImportError as error:
                print(f"CLI import error: {error}")

        elif choice == "2":
            try:
                from gui import launch_gui
                launch_gui()

            except ImportError as error:
                print(f"GUI is not ready: {error}")

        elif choice == "3":
            print("\nExiting Horizon TechX Network Toolkit.")
            break

        else:
            print("\nInvalid choice. Please select 1-3.")


if __name__ == "__main__":
    main()
