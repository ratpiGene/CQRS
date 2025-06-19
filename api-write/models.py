from pydantic import BaseModel
from typing import List

class ProduitCommande(BaseModel):
    produit_id: str
    quantite: int

class Commande(BaseModel):
    client_id: str
    produits: List[ProduitCommande]
    total: float
