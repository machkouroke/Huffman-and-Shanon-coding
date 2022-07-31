"""
Nom: Oke Machkour
Ce fichier contient des classes et fonctions utiles nécessaires à l'execution des deux algorithmes
"""


class Noeud:
    """
    Classe d'arbre personnalisé pour le parcours
    des arbres de Shanon et de Huffman
    """

    def __init__(self, value: list | float, name: str, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.name = name
        self.code = ''

    # Accesseur utile
    def get_name(self):
        return self.name

    def get_code(self):
        return self.code

    # Fonction d'obtention des fils du nœuds
    # elles sont assez explicite par leur nom
    def get_children(self) -> list:
        """
        Affiche la liste de tous les fils d'un nœud
        :return:
        """
        if all([self.left, self.right]):
            return [self.right, self.left] + [*self.right.get_children(), *self.left.get_children()]
        elif self.left is not None:
            return [self.left] + [*self.left.get_children()]
        elif self.right is not None:
            return [self.right] + [*self.right.get_children()]
        else:
            return []

    def get_right_child(self):
        return [self.right] + [*self.right.get_children()]

    def get_left_child(self):
        return [self.left] + [*self.left.get_children()]

    # Fonction nécessaire à la comparaison des nœuds
    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return f'Code({self.name}) = {self.code}'


class Tree:
    """
    Structure d'arbre avec quelque fonction intéressante pour la gestion d'un arbre de codage
    """

    def __init__(self, base: Noeud):
        self.base: Noeud = base
        Tree.tree_reader(self.base)

    def get_leaf(self) -> list[Noeud]:
        """
        :return: Liste des nœuds feuilles de l'arbre
        """
        return [x for x in self.base.get_children() if all(y is None for y in x.get_children())]

    def get_base(self) -> Noeud:
        """
        Renvoie la racine de l'arbre
        :return:
        """
        return self.base

    @staticmethod
    def tree_reader(base: Noeud):
        """
        Attribut à chaque fils gauche de l'arbre donné 0 et le fils droit 1
        Nécessaire pour la lecture des codages de caractère dans un arbre de Huffman ou de
        Shanon
        :param base: Racine de l'arbre
        """

        # Si la racine est unique dans l'arbre
        if not base.get_children():
            return

        # À chaque fils gauche on attribue 0 et 1 au fils
        # droit, et ce, de manière récursive
        for i in base.get_left_child():
            i.code += '0'
        for i in base.get_right_child():
            i.code += '1'
        Tree.tree_reader(base.left)
        Tree.tree_reader(base.right)


def probability(word: str) -> dict[str, float]:
    """
    Calcule pour un mot donné la propablité d'apparition de chaque
    caractère
    :param word: Mot dont on veut connaitre la probabilité de chaque caractère
    :return: dictionnaire contenant un caractère et sa propablité d'apparition
    """
    n: int = len(word)
    proba = {i: word.count(i) / n for i in set(word)}
    return dict(sorted(proba.items(), key=lambda x: x[1], reverse=True))


def main(f, g, name: str):
    """
    Fonction principale qui va être
    lancé en fonction du fichier algorithmique que vous utilisiez
    Sa compréhension n'est pas très importante
    :param f: fonction de construction de l'arbre
    :param g: fonction factory de l'algorithme
    :param name: nom de l'algorithme
    """
    print("Connaissiez vous les probabilité de vos mots ou vouliez vous encoder un mot")
    print("1- Encoder un mot")
    print("2- Probabilité connu")
    choice = int(input())
    match choice:
        case 1:
            word = input("Quelle est votre mot:")
            print(f"Voici les encodages de {name}")
            print(*g(word))
        case 2:
            print("NB: les probabilité doivent être saisi dans le même ordres que les paramètres")
            print("Veuillez entrer les caractère séparé par un espace")
            word = [x for x in input().split()]
            print("Veuillez entrer les probabilités séparé par un espace")
            proba = [float(x) for x in input().split()]
            dico_user: dict[str, float] = dict(sorted({x: y for x, y in zip(word, proba)}.items(), key=lambda x: x[1],
                                                      reverse=True))
            parameter: dict | list = dico_user if name == 'huffman' \
                else [list(dico_user.values()), list(dico_user.keys())]
            print(f"Voici les encodages de {name}")
            answer = f(parameter) if name == 'huffman' else Tree(f(*parameter))
            print(*[str(x) for x in answer.get_leaf()], sep="\n")
