from utility import Noeud, probability, Tree, main


def list_split(liste: list[float]) -> int:
    """
    Retourne l'index ou il faut couper la liste de la liste
    par exemple si k = 2 on coupe la liste comme suit:
    liste[:k] et liste[:k]
    :param : liste contenant les probabilités d'apparition des éléments
    :return: index k ou couper la liste
    """

    ecart: dict[int, float] = {}
    for i in range(len(liste)):
        # On cherche le plus petit écart entre les deux parties d'une liste
        # Cette liste étant trié en décroissant l'écart vont dans un premier
        # temps croitre dès que l'écart augmente alors le plus petit écart est
        # forcément l'écart précédent
        ecart[i] = abs(sum(liste[i:]) - sum(liste[:i]))
        if i >= 1 and ecart[i] > ecart[i - 1]:
            return i - 1
    return min(ecart.items(), key=lambda x: x[1])[0]


def shanon_tree(word_probability: list[float], word_liste: list[str]) -> Noeud:
    """
    Construit un arbre de Shanon
    :param word_probability: Contient la liste des probabilités triée par ordre décroissant
    :param word_liste: Contient la liste des mots dans le même ordre que les probablité
    :return: retourne la racine de notre Arbre de Shanon construit
    """

    # Si la liste à un élément unique on forme un nœud avec comme valeur la liste
    # et comme jointure le nom de ses éléments
    if len(word_probability) == 1:
        return Noeud(word_probability, "".join(word_liste))

    # Si l'élément n'est pas unique on le coupe selon le fait que chaque moitié a des sommes
    # de probablité à peu près égales
    k: int = list_split(word_probability)

    # Récursivement on applique l'algorithme de shanon à chaque partie
    left, right = shanon_tree(word_probability[:k], word_liste[:k]), \
                  shanon_tree(word_probability[k:], word_liste[k:])
    return Noeud(word_probability, "".join(word_liste), left, right)


def shanon_factory(sentence: str) -> list:
    """
    Construit l'arbre de Shanon puis
    retourne chaque lettre avec son code
    Cette fonction est utile si on veut coder un mot directement
    dans le cas où les probabilités sont connu on peut directement utiliser la fonction
    Shanon_tree
    :param sentence: Mot à coder
    :return: liste de lettre avec le code respectif qui lui est attribué
    """

    # On Calcule la probabilité de chaque lettre dans le mot
    probability_words: dict[str, float] = probability(sentence.replace(' ', ''))

    # On construit l'arbre de Shanon
    answer: Tree = Tree(shanon_tree(list(probability_words.values()), list(probability_words.keys())))

    return [str(x) for x in answer.get_leaf()]


if __name__ == '__main__':
    main(shanon_tree, shanon_factory, 'shanon')
