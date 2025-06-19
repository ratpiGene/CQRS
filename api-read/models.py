from pydantic import BaseModel
from typing import List

class LigneCommande(BaseModel):
    produit_id: str
    quantite: int

class Commande(BaseModel):
    commande_id: str
    client_id: str
    total: float
    lignes: List[LigneCommande]
