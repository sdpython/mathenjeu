# -*- coding: utf-8 -*-
"""
@file
@brief Shortcut to *tests*.
"""
import math
from ..activities import Notion, QuestionChoice, ActivityGroup


def simple_french_qcm():
    """
    Builds a simple French :epkg:`QCM` about mathématiques.
    """
    math_sixieme = Notion('not-math-1', 'not-math-1', 'fr',
                          domain='maths', level='6A')

    objs = [
        QuestionChoice('ch1', '2prem', 'fr', 'Le nombre 2 est-il un nombre premier ?',
                       notion=math_sixieme,
                       answers=['Oui', 'Non', 'Je ne sais pas'],
                       expected_answers=['Oui']),
        QuestionChoice('ch2', 'airecercle', 'fr', 'Quelle est la surface d\'un cercle en fonction du rayon R ?',
                       notion=math_sixieme,
                       answers=['$\\pi R$', '$2 \\pi R$',
                                '$\\pi R^2$', '$\\pi^2 R^2$', '$3R^2/4$'],
                       expected_answers=['$\\pi R^2$']),
        QuestionChoice('ch3', 'pen', 'fr', 'La figure est un pavage...',
                       notion=math_sixieme,
                       answers=['Impossible, aucune régularité.',
                                'Cela ne peut couvrir tout l\'espace.',
                                'Oui et j\'en connais l\'auteur.',
                                'C\'est un piège.'],
                       expected_answers=['Oui et j\'en connais l\'auteur.'],
                       show='static/img/pen.png'),
        QuestionChoice('ch4', 'peri', 'fr', 'La longueur des côtes françaises est de combien ?',
                       notion=math_sixieme,
                       answers=["%1.3fkm" % ((550000.e6 / math.pi)**0.5 * math.pi * 2 / 499),
                                'Il existe mais c\'est trop long à pied.',
                                'On ne sait pas le mesurer.',
                                'Sa longueur est infinie.',
                                "%1.3fkm" % ((550000.e6 / math.pi)**0.5 * math.pi * 2 / 1000), ],
                       expected_answers=['Sa longueur est infinie.'],
                       show='static/img/koch.png'),
        QuestionChoice('ch5', 'glace', 'fr', 'Un glaçon dans un verre fond. Le niveau de l\'eau monte-t-il ou descend-il ?',
                       notion=math_sixieme,
                       answers=['Il monte.', 'Il descend.', 'Il ne bouge pas.',
                                'Je n\'ai rien compris au réchauffement climatique.'],
                       expected_answers=['Il ne bouge pas.']),
        QuestionChoice('ch6', 'carre', 'fr', 'Un carré est un...',
                       notion=math_sixieme,
                       answers=['rectangle', 'parallélépidède', 'losange', 'un cercle',
                                'Je n\'ai toujours rien compris au réchauffement climatique.'],
                       expected_answers=['rectangle', 'losange']),
        QuestionChoice('ch7', 'tva', 'fr', 'Vous avez acheté un produit à 10 euros. La TVA est à 20%, quel est le prix sans la TVA ?',
                       notion=math_sixieme,
                       answers=['8 euros', '9.2', '10 * 0.8', '10 / 1.2', '7.8',
                                '10 / 1.2'],
                       expected_answers=['10 / 1.2']),
        QuestionChoice('ch8', 'dalton', 'fr', 'Gilles et Jean sont demi-frères, Jean et Charles sont demi-frères. Gilles et Charles sont...',
                       notion=math_sixieme,
                       answers=['frères, demi-frères',
                                'rien du tout', 'on ne sait pas'],
                       expected_answers=['on ne sait pas']),
        QuestionChoice('ch9', 'zoo', 'fr', 'Quel est le théorème de maths qui a servi à mesurer les Pyramides ?',
                       notion=math_sixieme,
                       answers=None,
                       expected_answers=['Thalès']),
    ]
    return ActivityGroup("simple_french_qcm", "simple_french_qcm", objs)


def ml_french_qcm():
    """
    Builds a simple French :epkg:`QCM` about machine learning.
    """
    niveau = Notion('not-math-2', 'not-math-2', 'fr',
                    domain='maths', level='20A')

    objs = [
        QuestionChoice('ch1', 'pen', 'fr', 'Si ce dessin vous inspire quelques mots...',
                       notion=niveau,
                       answers=['Complètement raté.',
                                'Je ne comprends pas la symbolique.',
                                "C'est de l'overfitting.",
                                "Bordel c'est Noël."],
                       expected_answers=[],
                       show='static/img/coeur.png'),
        QuestionChoice('ch2', 'r2', 'fr', 'Vous avez un $R^2$ de 0.99 et...',
                       notion=niveau,
                       answers=["Chouette les vacances !", "Trop facile !", "C'est beaucoup trop facile.",
                                "Ah oui, le découpage train test."],
                       expected_answers=[]),
        QuestionChoice('ch3', 'c1000', 'fr', 'On vous demande de classer 2000 images en 1000 classes.',
                       notion=niveau,
                       answers=["Ok.",
                                "Mais c'est juste une fois ou toutes les semaines ?",
                                "C'est quoi les dix classes les plus importantes ?",
                                "Vous n'êtes pas Harry Potter. Vous êtes datascientiste."],
                       expected_answers=[]),
        QuestionChoice('ch4', 'go6', 'fr', '6 Go de données et une random forest à caler...',
                       notion=niveau,
                       answers=["Il vous faut une plus grosse machine.",
                                "La grosse machine, c'est pas assez, c'est l'occasion de demander un cluster.",
                                "Seuls les russes savent le faire.",
                                "Vous essayez XGBoost.",
                                "Vous bidouillez scikit-learn pour gérer l'apprentissage sans tout charger en mémoire pour chaque arbre.",
                                "Ouais, on va tout refaire en C++."],
                       expected_answers=[]),
        QuestionChoice('ch5', 'noel', 'fr', "C'est Noël et vous devez livrez 1000 paquets en 3 jours avec 10 chauffeurs. "
                       "Ca commence dans 48h.",
                       notion=niveau,
                       answers=["Ce n'est pas possible.",
                                "Impossible n'est pas français.",
                                "Trop cool ! Je vais pondre un algo de folie.",
                                "Je ne le ferai jamais à la main. Je ne sais pas compter de toutes façons.",
                                "Je sens le truc bugger à 3h du mat, soit 3h avant le départ des chauffeurs."],
                       expected_answers=[]),
        QuestionChoice('ch6', 'auc', 'fr', "Une AUC de 0.2.",
                       notion=niveau,
                       answers=["Ce n'est pas possible.",
                                "C'est mieux que zéro.",
                                "Il y a sans doute une erreur de signe.",
                                "C'est quoi le taux de classif déjà ?",
                                "Mais pourquoi mettre l'AUC dans le rapport, personne ne sait ce que c'est !"],
                       expected_answers=[]),
        QuestionChoice('ch7', 'jaune', 'fr', "Vous avez construit un modèle qui prédit la tendance de la mode "
                       "et le jaune est à l'honneur en ce moment.",
                       notion=niveau,
                       answers=["Les prédictions ne seront pas bonnes pendant 6 mois.",
                                "Vous avez vu une série médicale et vous faites une analogie avec un diagnostique différentiel.",
                                "Vous devez construire une autre source de données : vous prenez les photos des tenues de vos employés.",
                                "Vous créez une collection pour laquelle les concepteurs de vêtements ont plus de libertés."],
                       expected_answers=[]),
        QuestionChoice('ch8', 'classif', 'fr', "95% de bonne classification (binaire). c'est bon ou c'est pas bon ?",
                       notion=niveau,
                       answers=["C'est nul.",
                                "C'est génial.",
                                "On n'est pas loin.",
                                "Ca dépend de l'utilisation du modèle.",
                                "Votre commentaire dépend de celui qui vous écoute.",
                                "L'équipe marketting est déjà en train de vendre le produit.",
                                "Au fait, c'est quoi les proportions des deux classes ?"],
                       expected_answers=[]),
        QuestionChoice('ch9', 'csp', 'fr', "Vous aimeriez connaître la catégorie socio professionnelle de l'interviewé.",
                       notion=niveau,
                       answers=["Les gens mentent à cette question.",
                                "Cela introduit un biais non éthique lors de l'étude.",
                                "Trois questions détournées et c'est réglé.",
                                "Combien de fois par semaine achetez-vous du bio ?"],
                       expected_answers=[]),
        QuestionChoice('ch10', 'coche', 'fr', "Vous avez coché...",
                       notion=niveau,
                       answers=["Une seule réponse à chaque fois.",
                                "Une ou plusieurs réponses.",
                                "C'est une question piège.",
                                "Ah on pouvait cocher plusieurs cases ? Mais ce n'était pas précisé."],
                       expected_answers=[]),
        QuestionChoice('ch11', 'st', 'fr', "Encore une prédiction de séries temporelles",
                       notion=niveau,
                       answers=["Cool, sliding windows + random forest comme d'hab et c'et torché.",
                                "LSTM parce que jamais fait.",
                                "Du deep du deep du deep",
                                "Il faut varier les plaisirs, et ce sera utile dans 6 mois."],
                       expected_answers=[]),
        QuestionChoice('ch12', 'biais', 'fr', "Votre modèle prédit un prix plus élevé pour les hommes une assurance automobile.",
                       notion=niveau,
                       answers=["Pour une fois qu'ils gagnent moins.",
                                "C'est un biais non éthique.",
                                "C'est un résultat attendu.",
                                "Il y a peut être d'autres biais. Il faut vérifier."],
                       expected_answers=[]),
        QuestionChoice('ch13', 'vba', 'fr', "Votre patron vous demande une macro VBA parce qu'il a toujours fait comme ça.",
                       notion=niveau,
                       answers=["Vous démissionnez.",
                                "Ca pètera un jour mais vous serez parti d'ici là.",
                                "Ca marche bien le VBA.",
                                "Vous le faites en python quand même."],
                       expected_answers=[]),
        QuestionChoice('ch14', 'apple', 'fr', "Votre père ne comprend pas pourquoi Apple sait qu'il a la grippe.",
                       notion=niveau,
                       answers=["Vous lui demandez comment il le sait.",
                                "Vous lui recommandez de prendre un téléphone avec l'OS de Firefox.",
                                "Vous prenez le temps de passer en revue les paramètres de son téléphone.",
                                "Vous lui apprenez à changer les paramètres de son téléphone."],
                       expected_answers=[]),
        QuestionChoice('ch15', 'tsne', 'fr', "Vous avez utilisé une t-SNE pour projeter les données. Vons songez à l'utiliser pour prédire.",
                       notion=niveau,
                       answers=["Ca marche.",
                                "Vous regardez l'API.",
                                "Vous cherchez une librairie qui implémente une version paramétrisée.",
                                "Vous remplacez par une ACP.",
                                "Vous apprenez le résultat avec un réseau de neurones profond."],
                       expected_answers=[]),
    ]
    return ActivityGroup("ml_french_qcm", "ml_french_qcm", objs)


def simple_cinema_qcm():
    """
    Builds a simple French :epkg:`QCM` about movies.
    """
    cinema_seconde = Notion('not-cinema-1', 'not-cinema-1', 'fr',
                            domain='cinema', level='2A')

    objs = [
        QuestionChoice(
            'ch1', 'hp', 'fr', 'Quel est la deuxieme épreuve de la coupe de feu ?',
            notion=cinema_seconde,
            answers=["L'épreuve du dragon",
                     "l'épreuve des sirènes", "le labyrinthe"],
            expected_answers=["L'épreuve du dragon"]),
        QuestionChoice(
            'ch2', 'bond', 'fr', 'Quel acteur a joué en premier James Bond ?',
            notion=cinema_seconde,
            answers=["Emma Peel", "Sean Connery", "Michael Moore"],
            expected_answers=["Sean Connery"]),
        QuestionChoice(
            'ch3', 'manga', 'fr', "Comment se nomme la sorcière dans 'Le voyage de Chihiro' ?",
            notion=cinema_seconde,
            answers=["yagaba", "Babayaga", "Yubaba"],
            expected_answers=["Yubaba"]),
        QuestionChoice(
            'ch4', 'heros', 'fr', "Dans le film avengers endgame, qui meurt lorsque Thanos claque des doigts ?",
            notion=cinema_seconde,
            answers=["spiderman-blackpanther-docterStrange",
                     "spiderman-ironman-gamorra", "Hulk-blackwidow-rocket"],
            expected_answers=["spiderman-blackpanther-docterStrange"]),
        QuestionChoice(
            'ch5', 'cannes', 'fr', "Quelle est la dernière femme réalisatrice à avoir gagné la palme d'or à Cannes ?",
            notion=cinema_seconde,
            answers=["Agnès Varda", "Jane Campion", "Kathryn Bigelow"],
            expected_answers=["Jane Campion"]),
        QuestionChoice(
            'ch6', 'bat', 'fr', "Quel est le tout premier acteur à avoir joué le Joker ?",
            notion=cinema_seconde,
            answers=["Heath Ledger", "Joaquin Phoenix", "Jack Nickolson"],
            expected_answers=["Jack Nickolson"]),
        QuestionChoice(
            'ch7', 'sw', 'fr', "Quel est le compositeur de la musique de Star Wars ?",
            notion=cinema_seconde,
            answers=["Clint Eastwood", "John Williams",
                     "Hans Zimmer", "Maurice Jarre"],
            expected_answers=["John Williams"]),
        QuestionChoice(
            'ch8', 'rn', 'fr', "Comment se nomme le renne de Kristoff dans la Reine des Neiges ?",
            notion=cinema_seconde,
            answers=["Sven", "Hans", "Mark"],
            expected_answers=["Sven"]),
        QuestionChoice(
            'ch9', 'as', 'fr', ("Dans les aristochats, comment se prénomme le dernier chat "
                                "de Adélaïde Bonnefamille apres Toulouse, Berlioz et Duchesse ?"),
            notion=cinema_seconde,
            answers=["Juliette", "Chloé", "Marie"],
            expected_answers=["Marie"]),
        QuestionChoice(
            'ch10', 'as', 'fr', "Qui joue Edward aux Mains d'argent ?",
            notion=cinema_seconde,
            answers=["Leonardo DiCaprio", "Johnny Depp", "Tom Hanks"],
            expected_answers=["Johnny Depp"]),
    ]
    return ActivityGroup("simple_cinema_qcm", "simple_cinema_qcm", objs)
