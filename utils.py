def get_product_name():
    while True:
        name = input("Enter product name: ").strip()

        if name:
            return name

        print("Product name cannot be empty.")


def get_number(number_type, prompt, minimum=0):
    while True:
        try:
            if number_type == int:
                value = int(input(prompt))
            elif number_type == float:
                value = float(input(prompt))
            else:
                print("Unsupported number type.")
                return None

            if value < minimum:
                print(f"Value must be at least {minimum}.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")