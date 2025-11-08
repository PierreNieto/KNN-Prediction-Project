#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 22:32:18 2024

@author: nieto
"""

class Iris:
    def __init__(self, c1, c2, c3, c4, c5, c6, c7, label=None):
        self.features = [c1, c2, c3, c4, c5, c6, c7]
        self.label = label

    def __getitem__(self, key):
        if key == "features":
            return self.features
        elif key == "label":
            return self.label


def charger_donnees(fichier, has_label=True): #Charge un fichier CSV dans une liste d'instances de la classe Iris
    repertoire = []
    with open(fichier, 'r') as f:
        lignes = f.readlines()
        for ligne in lignes[1:]:
            valeurs = ligne.strip().split(',')
            if has_label:
                repertoire.append(Iris(float(valeurs[1]), float(valeurs[2]), float(valeurs[3]), 
                                       float(valeurs[4]), float(valeurs[5]), float(valeurs[6]), 
                                       float(valeurs[7]), valeurs[8]))
            else:
                repertoire.append(Iris(float(valeurs[1]), float(valeurs[2]), float(valeurs[3]), 
                                       float(valeurs[4]), float(valeurs[5]), float(valeurs[6]), 
                                       float(valeurs[7])))
    return repertoire


def tableau_distance_manhattan(nouvelles_features, tab1):
    distances = []
    for e in tab1:
        if isinstance(e, Iris):
            # Distance de Manhattan
            result = sum(abs(a - b) for a, b in zip(e["features"], nouvelles_features))
            distances.append([result, e])
    return sorted(distances, key=lambda x: x[0])


def prediction(k, tab):
    label_count = {}
    for i in range(k):
        label = tab[i][1]["label"]
        if label not in label_count:
            label_count[label] = 0
        label_count[label] += 1
    return max(label_count, key=label_count.get)


def knn(train_data, nouvelles_features, k=1):  # Fixer k à 1
    tableau_classe = tableau_distance_manhattan(nouvelles_features, train_data)
    return prediction(k, tableau_classe)


# Charger les fichiers CSV
train_file_path = 'train.csv'
test_file_path = 'test.csv'

train_data = charger_donnees(train_file_path, has_label=True)
test_data = charger_donnees(test_file_path, has_label=False)

# Effectuer les prédictions
results = []
for i, e in enumerate(test_data):
    prediction_label = knn(train_data, e["features"], k=1)  # on fixe k à 1
    results.append(f"{i + 1030},{prediction_label}")  # on ajoute l'index et le label qui commence à partir de 1030

# Enregistrer les prédictions dans un fichier CSV
output_file_path = 'predictions_knn_man.csv'
with open(output_file_path, 'w') as f:
    f.write("Id,Label\n")
    f.write("\n".join(results))

print(f"Les prédictions sont dans : {output_file_path}")