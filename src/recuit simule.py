import random
import math

def calculer_distance_totale(solution, matrice_distances):
    """Calcule la distance totale d'un parcours"""
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_voisin(solution):
    """Génère un voisin en échangeant deux villes aléatoires"""
    voisin = solution[:]  # Copie de la solution
    i, j = random.sample(range(len(solution)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin

def recuit_simule(matrice_distances, temperature_initiale=1000, temperature_finale=0.1, 
                  alpha=0.99, iterations_par_temp=100):
    """
    Implémentation de l'algorithme du Recuit Simulé pour le TSP
    
    Args:
        matrice_distances: Matrice des distances entre villes
        temperature_initiale: Température de départ
        temperature_finale: Température d'arrêt
        alpha: Facteur de refroidissement (0 < alpha < 1)
        iterations_par_temp: Nombre d'itérations à chaque température
    """
    nombre_villes = len(matrice_distances)
    
    # Solution initiale aléatoire
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)
    
    # Meilleure solution trouvée
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = distance_actuelle
    
    temperature = temperature_initiale
    historique = []
    
    print("Démarrage du Recuit Simulé...")
    print(f"Température initiale: {temperature}")
    print(f"Solution initiale: {solution_actuelle} (distance: {distance_actuelle})")
    
    iteration = 0
    while temperature > temperature_finale:
        acceptations = 0
        
        for _ in range(iterations_par_temp):
            # Générer un voisin
            solution_voisine = generer_voisin(solution_actuelle)
            distance_voisine = calculer_distance_totale(solution_voisine, matrice_distances)
            
            # Calculer la différence de coût
            delta = distance_voisine - distance_actuelle
            
            # Accepter la solution si elle est meilleure
            # ou avec une certaine probabilité si elle est pire
            if delta < 0:
                # Solution améliorante : toujours acceptée
                solution_actuelle = solution_voisine
                distance_actuelle = distance_voisine
                acceptations += 1
            else:
                # Solution dégradante : acceptée avec probabilité exp(-delta/T)
                probabilite = math.exp(-delta / temperature)
                if random.random() < probabilite:
                    solution_actuelle = solution_voisine
                    distance_actuelle = distance_voisine
                    acceptations += 1
            
            # Mettre à jour la meilleure solution
            if distance_actuelle < meilleure_distance:
                meilleure_solution = solution_actuelle[:]
                meilleure_distance = distance_actuelle
            
            iteration += 1
        
        # Afficher les statistiques
        taux_acceptation = acceptations / iterations_par_temp
        print(f"Itération {iteration}: Temp={temperature:.2f}, Meilleure={meilleure_distance:.2f}, "
              f"Actuelle={distance_actuelle:.2f}, Taux_accept={taux_acceptation:.2f}")
        
        # Refroidissement
        temperature *= alpha
    
    print("Optimisation terminée!")
    return meilleure_solution, meilleure_distance

# Matrice de distances (identique à votre code original)
matrice_distances = [
    [0, 2, 2, 7, 15, 2, 5, 7, 6, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [2, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [7, 10, 4, 2, 0, 7, 3, 2, 2, 7],
    [2, 3, 3, 7, 7, 0, 1, 7, 2, 10],
    [5, 7, 3, 7, 3, 1, 0, 2, 1, 3],
    [7, 7, 4, 7, 2, 7, 2, 0, 1, 10],
    [6, 8, 2, 5, 2, 2, 1, 1, 0, 15],
    [5, 2, 3, 4, 7, 10, 3, 10, 15, 0]
]

# Exécution du Recuit Simulé
print("=== ALGORITHME DU RECUIT SIMULÉ ===")
meilleure_solution, meilleure_distance = recuit_simule(
    matrice_distances,
    temperature_initiale=1000,
    temperature_finale=0.1,
    alpha=0.95,
    iterations_par_temp=50
)

print("\n=== RÉSULTATS FINAUX ===")
print(f"Meilleure solution trouvée: {meilleure_solution}")
print(f"Distance minimale: {meilleure_distance}")

# Comparaison avec Tabu Search
print("\n" + "="*50)
print("COMPARAISON AVEC TABU SEARCH")
print("="*50)

def tabu_search_comparaison(matrice_distances, nombre_iterations=1000, taille_tabu=50):
    """Version Tabu Search pour comparaison"""
    nombre_villes = len(matrice_distances)
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)

    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)

    tabu_list = deque(maxlen=taille_tabu)

    for iter in range(nombre_iterations):
        voisins = []
        # Générer des voisins par échange de deux villes
        for i in range(len(solution_actuelle)):
            for j in range(i + 1, len(solution_actuelle)):
                voisin = solution_actuelle[:]
                voisin[i], voisin[j] = voisin[j], voisin[i]
                if tuple(voisin) not in tabu_list:
                    voisins.append(voisin)
        
        if not voisins:
            break

        # Choisir le meilleur voisin non-tabou
        solution_actuelle = min(voisins, key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)

        tabu_list.append(tuple(solution_actuelle))

        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle
            
        if iter % 200 == 0:
            print(f"Tabu Search - Itération {iter}: Meilleure distance = {meilleure_distance:.2f}")

    return meilleure_solution, meilleure_distance

# Exécuter Tabu Search pour comparaison
print("\nExécution de Tabu Search...")
meilleure_solution_tabu, meilleure_distance_tabu = tabu_search_comparaison(
    matrice_distances, 
    nombre_iterations=1000, 
    taille_tabu=50
)

print(f"\nTabu Search - Meilleure solution: {meilleure_solution_tabu}")
print(f"Tabu Search - Distance minimale: {meilleure_distance_tabu}")

print("\n" + "="*50)
print("SYNTHÈSE DES RÉSULTATS")
print("="*50)
print(f"Recuit Simulé:  {meilleure_distance:.2f}")
print(f"Tabu Search:    {meilleure_distance_tabu:.2f}")

if meilleure_distance < meilleure_distance_tabu:
    print("✅ Recuit Simulé a trouvé une meilleure solution")
elif meilleure_distance > meilleure_distance_tabu:
    print("✅ Tabu Search a trouvé une meilleure solution")
else:
    print("✅ Les deux algorithmes ont trouvé la même solution")