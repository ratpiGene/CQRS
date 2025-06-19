def insert_commande(cursor, commande):
    cursor.execute("""
        INSERT INTO commandes (commande_id, client_id, total)
        VALUES (%s, %s, %s)
    """, (commande["id"], commande["client_id"], commande["total"]))

    for produit in commande["produits"]:
        cursor.execute("""
            INSERT INTO lignes_commande (commande_id, produit_id, quantite)
            VALUES (%s, %s, %s)
        """, (commande["id"], produit["produit_id"], produit["quantite"]))
