from fastapi import APIRouter
from db import get_connection
from models import Commande, LigneCommande

router = APIRouter()

@router.get("/commandes", response_model=list[Commande])
def get_commandes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM commandes")
    commandes = cursor.fetchall()

    result = []
    for cmd in commandes:
        cursor.execute("SELECT * FROM lignes_commande WHERE commande_id = %s", (cmd["commande_id"],))
        lignes = cursor.fetchall()
        result.append(Commande(
            commande_id=cmd["commande_id"],
            client_id=cmd["client_id"],
            total=cmd["total"],
            lignes=[LigneCommande(**l) for l in lignes]
        ))

    conn.close()
    return result
