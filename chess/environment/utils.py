
def square_str_to_pos(square_str):
    letters = 'ABCDEFGH'
    row = letters.index(square_str[0])
    col = int(square_str[1]) - 1
    return row, col
    
def square_pos_to_str(pos):
    letters = 'ABCDEFGH'
    row, col = pos
    return f"{letters[row]}{col + 1}"