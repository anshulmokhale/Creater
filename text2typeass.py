import random

def text_to_ass(input_text):
    lines = input_text.split('\n')
    ass_lines = []

    for line in lines:
        ass_line = ''
        for char in line:
            random_duration = random.choice(range(10, 26, 5))
            ass_line += f'{{\\k{random_duration}}}{char}'
        ass_lines.append(ass_line)

    ass_text = ' '.join(ass_lines)
    return ass_text

# Example usage
input_text = "Your Text"
ass_output = text_to_ass(input_text)
print(ass_output)
