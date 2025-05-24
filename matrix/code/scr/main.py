import os

class SparseMatrix:
    def __init__(self, file_path=None, num_rows=None, num_cols=None):
        if file_path:
            self.load_from_file(file_path)
        else:
            self.num_rows = num_rows
            self.num_cols = num_cols
            self.elements = {}

    def load_from_file(self, file_path):
        self.elements = {}
        with open(file_path, 'r') as f:
            lines = f.readlines()
        self.num_rows = 0
        self.num_cols = 0
        for line in lines[2:]:
            if line.strip() == "":
                continue
            try:
                row, col, value = self.parse_line(line.strip())
                self.num_rows = max(self.num_rows, row + 1)
                self.num_cols = max(self.num_cols, col + 1)
                self.elements[(row, col)] = value
            except ValueError as e:
                raise ValueError(f"Input file has wrong format: {e}")

    def parse_line(self, line):
        if not (line.startswith('(') and line.endswith(')')):
            raise ValueError("Line must start with '(' and end with ')'")
        line = line[1:-1]
        parts = line.split(',')
        if len(parts) != 3:
            raise ValueError("Line must contain exactly three comma-separated values")
        return int(parts[0]), int(parts[1]), int(parts[2])

    def get_element(self, row, col):
        return self.elements.get((row, col), 0)

    def set_element(self, row, col, value):
        if row >= self.num_rows or col >= self.num_cols:
            raise IndexError("Index out of bounds")
        self.elements[(row, col)] = value

    def __add__(self, other):
        result = SparseMatrix(num_rows=max(self.num_rows, other.num_rows),
                                num_cols=max(self.num_cols, other.num_cols))
        for key, value in self.elements.items():
            result.set_element(*key, value)
        for key, value in other.elements.items():
            result.set_element(*key, result.get_element(*key) + value)
        return result

    def __sub__(self, other):
        result = SparseMatrix(num_rows=max(self.num_rows, other.num_rows),
                                num_cols=max(self.num_cols, other.num_cols))
        for key, value in self.elements.items():
            result.set_element(*key, value)
        for key, value in other.elements.items():
            result.set_element(*key, result.get_element(*key) - value)
        return result

    def __mul__(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError("For multiplication, the number of columns in the first matrix must equal the number of rows in the second")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)
        for i in range(self.num_rows):
            for j in range(other.num_cols):
                sum_value = 0
                for k in range(self.num_cols):
                    sum_value += self.get_element(i, k) * other.get_element(k, j)
                if sum_value:
                    result.set_element(i, j, sum_value)
        return result

    def __repr__(self):
        s = f"SparseMatrix(num_rows={self.num_rows}, num_cols={self.num_cols})\n"
        for (row, col), value in self.elements.items():
            s += f"({row}, {col}, {value})\n"
        return s

    def add(self, other):
        return self.__add__(other)

    def subtract(self, other):
        return self.__sub__(other)

    def multiply(self, other):
        return self.__mul__(other)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.abspath(os.path.join(base_dir, '..', '..', 'sample_inputs'))
    output_dir = os.path.abspath(os.path.join(base_dir, '..', '..', 'sample_results'))

    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output directory does not exist: {output_dir}")

    print(f"Base directory: {base_dir}")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")

    matrix1_file = os.path.join(input_dir, 'matrix1.txt')
    matrix2_file = os.path.join(input_dir, 'matrix2.txt')

    try:
        matrix1 = SparseMatrix(file_path=matrix1_file)
        matrix2 = SparseMatrix(file_path=matrix2_file)
    except ValueError as e:
        print(f"Error loading matrices: {e}")
        return

    while True:
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Exit")
        choice = input("Enter choice (1/2/3/4): ").strip()
        if choice == '1':
            result = matrix1.add(matrix2)
            operation = "addition"
        elif choice == '2':
            result = matrix1.subtract(matrix2)
            operation = "subtraction"
        elif choice == '3':
            result = matrix1.multiply(matrix2)
            operation = "multiplication"
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice! Please select a valid option.")
            continue

        print(f"\nResult of {operation}:")
        print(result)
        output_file = os.path.join(output_dir, f"{operation}_result.txt")
        with open(output_file, 'w') as f:
            f.write(f"rows={result.num_rows}\n")
            f.write(f"cols={result.num_cols}\n")
            for (row, col), value in result.elements.items():
                f.write(f"({row}, {col}, {value})\n")
        print(f"Result saved to {output_file}")

if __name__ == '__main__':
    main()
