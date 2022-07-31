"""
Nom: Oke Machkour
Algorithme de huffman avec une implémentation par arbre
"""


from utility import Noeud, Tree, probability, main

# Bibliothèque pour gérer les files de priorité avec un temps optimisée
from heapq import heapify, heappop, heappush


def huffman_tree(dico: dict[str, float]) -> Tree:
    """
    Retourne la racine de l'arbre de Huffman
    :param dico: dico qui contient les mots et leur probabilité d'apparition
    :return: Nœud racine de l'arbre de Huffman
    """
    node_list: list[Noeud] = [Noeud(value, i) for i, value in dico.items()]

    huffman_tree_nodes: list[Noeud] = []

    # On transforme la liste en file de priorité
    heapify(node_list)

    while len(node_list) > 1:
        # On prend les deux plus petits nœuds selon la fréquence
        a, b = [heappop(node_list) for _ in range(2)]

        # On les ajoute à l'arbre s'ils n'y sont pas deja
        # le premier nœud extrait à gauche et le second à droite
        huffman_tree_nodes += [x for x in (a, b) if x not in huffman_tree_nodes]

        # On crée un nœud interne qui seras la somme des deux nœuds retirée de la file de priorité
        internal = Noeud(a.value + b.value, f'{a.get_name()}{b.get_name()}', left=a, right=b)

        # On remet ce nœud interne dans la file et on l'ajoute aussi à l'arbre
        heappush(node_list, internal)
        huffman_tree_nodes += [internal]

    return Tree(huffman_tree_nodes[-1])


def huffman_factory(sentence: str) -> list:
    """
    Construit l'arbre de Shanon puis
    retourne chaque lettre avec son code
    Cette fonction est utile si on veut coder un mot directement
    dans le cas où les probabilités sont connu on peut directement utiliser la fonction
    huffman_tree
    :param sentence: Mot à coder
    :return: liste de lettre avec le code respectif qui lui est attribué
    """

    # On Calcule la probabilité de chaque lettre dans le mot (On ne compte pas les espaces)
    probability_words: dict[str, float] = probability(sentence.replace(' ', ''))

    # On construit l'arbre de Huffman
    answer: Tree = huffman_tree(probability_words)

    return [str(x) for x in answer.get_leaf()]


if __name__ == '__main__':
    main(huffman_tree, huffman_factory, 'huffman')
