'''
divides protein into smaller proteins
'''

def divide(proteinstring):

    protein = []

    pieces = []

    for i in proteinstring:
        protein.append(i)

    lenprotein = len(protein)

    if lenprotein % 9 == 0:
        n = 9
    elif lenprotein % 8 == 0:
        n = 8
    elif lenprotein % 7 == 0:
        n = 7
    elif lenprotein % 6 == 0:
        n = 6
    elif lenprotein % 5 == 0:
        n = 5
    else:
        n = 4

    for i in range(0, lenprotein, n):
        pieces.append(protein[i:i + n])


    return pieces
#     print pieces
# divide("HHPHPHPHPHHHHPHPPPHPPPHPP")
