lower_case_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
upper_case_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def rot13(plaintext):
    lower_case_map = create_map(lower_case_list)
    upper_case_map = create_map(upper_case_list)
    
    output = ""
    for char in plaintext:
        if char in lower_case_map:
            output += lower_case_map[char]
        elif char in upper_case_map:
            output += upper_case_map[char]
        else:
            output += char
    return output

def create_map(input_list):
    output = {}
    for i in range(0, len(input_list)):
        key = input_list[i]
        output[key] = input_list[(i+13)%26]
    return output
    
plaintext = "Hello world!"
ciphertext = rot13(plaintext)

print plaintext
print rot13(plaintext)
print rot13(ciphertext)