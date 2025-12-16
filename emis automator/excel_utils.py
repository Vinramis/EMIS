
import pandas as pd

def next_col(col):
    """Increments Excel column letter (A -> B, Z -> AA)."""
    result = list(col)
    i = len(result) - 1
    while i >= 0:
        if result[i] != 'Z':
            result[i] = chr(ord(result[i]) + 1)
            return ''.join(result)
        else:
            result[i] = 'A'
            i -= 1
    return 'A' + ''.join(result)

def get_cell_value(data: pd.DataFrame, cell_ref: str):
    """Gets cell value from DataFrame by reference (e.g., 'A1')."""
    col = ''.join(filter(str.isalpha, cell_ref)).upper()
    # Excel rows are 1-indexed, pandas .iat is 0-indexed
    try:
        row_digits = ''.join(filter(str.isdigit, cell_ref))
        if not row_digits:
            return None
        row = int(row_digits) - 1
    except ValueError:
        return None

    col_index = 0
    for c in col:
        col_index = col_index * 26 + (ord(c) - ord('A') + 1)
    col_index -= 1

    if 0 <= row < len(data) and 0 <= col_index < len(data.columns):
        return data.iat[row, col_index]
    return None

def generate_sequence(data: pd.DataFrame, start_cell: str, mode: str) -> list:
    """Generates a sequence of non-empty cell references from DataFrame."""
    sequence = []
    empty_cell_counter = 0
    MAX_EMPTY_CELLS_IN_A_ROW = 5

    current_col = ''.join(filter(str.isalpha, start_cell)).upper()
    try:
        current_row = int(''.join(filter(str.isdigit, start_cell)))
    except ValueError:
        return []

    while empty_cell_counter < MAX_EMPTY_CELLS_IN_A_ROW:
        cell_ref = f"{current_col}{current_row}"
        cell_value = get_cell_value(data, cell_ref)

        # Check if cell is effectively empty
        is_empty = pd.isna(cell_value) or len(str(cell_value).strip()) < 2

        if is_empty:
            empty_cell_counter += 1
        else:
            empty_cell_counter = 0
            sequence.append(cell_ref)

        # Move to next cell
        if mode == "col":
            current_row += 1
        elif mode == "row":
            current_col = next_col(current_col)
        else:
            break # Should not happen with valid config

    return sequence

def read_topics_from_excel(file_path: str, start_cell: str, mode: str) -> list[str]:
    """Helper to read all topics from the excel file."""
    try:
        df = pd.read_excel(file_path, header=None)
        cell_sequence = generate_sequence(df, start_cell, mode)
        values = [str(get_cell_value(df, cell_ref)).strip() for cell_ref in cell_sequence]
        return values
    except Exception as e:
        print(f"[ERROR] Reading Excel file: {e}")
        return []
