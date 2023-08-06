'''
NesterRato: Biblioteca Pyton de exemplo
'''

def print_lol(the_list):
	'''
    print_lol: Funcao exemplo para ler uma lista generica,
               que pode ser composta por itens ou outras listas
    '''

	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
