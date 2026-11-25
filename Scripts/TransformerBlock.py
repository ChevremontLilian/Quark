import torch
import torch.nn as nn
import torch.nn.functional as F

# ----------------------------
# Classes originales (pour compatibilité avec pyAI.py)
# ----------------------------
class SelfAttentionHead(nn.Module):
    """
    Tête d'auto-attention.
    Calcule les projections clé / requête / valeur puis applique une
    attention pondérée où chaque position ne peut regarder que les
    positions précédentes (masque triangulaire inférieur).
    """

    def __init__(self, dimension_embedding, taille_bloc, taille_tete):
        """
        Args:
            dimension_embedding (int): dimension des vecteurs d'entrée.
            taille_bloc (int): longueur maximale de la séquence (contexte).
            taille_tete (int): dimension de sortie de cette tête d'attention.
        """
        super().__init__()
        self.cle = nn.Linear(dimension_embedding, taille_tete, bias=False)
        self.requete = nn.Linear(dimension_embedding, taille_tete, bias=False)
        self.valeur = nn.Linear(dimension_embedding, taille_tete, bias=False)
        self.register_buffer('triangle_inferieur', torch.tril(torch.ones(taille_bloc, taille_bloc)))

    def forward(self, x):
        """
        Args:
            x (torch.Tensor): tenseur d'entrée de forme (batch, temps, canaux).

        Returns:
            torch.Tensor: sortie pondérée par l'attention, de forme (batch, temps, taille_tete).
        """
        taille_lot, longueur_sequence, nb_canaux = x.shape
        k = self.cle(x)
        q = self.requete(x)
        poids_attention = q @ k.transpose(-2, -1) / (nb_canaux ** 0.5)
        poids_attention = poids_attention.masked_fill(
            self.triangle_inferieur[:longueur_sequence, :longueur_sequence] == 0, float('-inf')
        )
        poids_attention = F.softmax(poids_attention, dim=-1)
        v = self.valeur(x)
        sortie = poids_attention @ v
        return sortie

# ----------------------------
# Attention multi-têtes (originale)
# ----------------------------
class MultiHeadAttention(nn.Module):
    """
    Combine plusieurs têtes d'auto-attention exécutées en parallèle puis
    fusionne leurs sorties par une projection linéaire.
    """

    def __init__(self, dimension_embedding, taille_bloc, nb_tetes):
        """
        Args:
            dimension_embedding (int): dimension des vecteurs d'entrée/sortie.
            taille_bloc (int): longueur maximale de la séquence.
            nb_tetes (int): nombre de têtes d'attention en parallèle.
        """
        super().__init__()
        taille_tete = dimension_embedding // nb_tetes
        self.tetes = nn.ModuleList(
            [SelfAttentionHead(dimension_embedding, taille_bloc, taille_tete) for _ in range(nb_tetes)]
        )
        self.projection = nn.Linear(nb_tetes * taille_tete, dimension_embedding)

    def forward(self, x):
        """
        Args:
            x (torch.Tensor): tenseur d'entrée de forme (batch, temps, canaux).

        Returns:
            torch.Tensor: sortie combinée de toutes les têtes, reprojetée dans l'espace de dimension_embedding.
        """
        sortie = torch.cat([tete(x) for tete in self.tetes], dim=-1)
        return self.projection(sortie)

# ----------------------------
# Réseau feed-forward (original)
# ----------------------------
class FeedForward(nn.Module):
    """
    Petit réseau entièrement connecté (MLP), appliqué indépendamment à
    chaque position, avec une couche cachée quatre fois plus large que
    l'embedding.
    """

    def __init__(self, dimension_embedding, dropout_rate=0.2):
        """
        Args:
            dimension_embedding (int): dimension d'entrée et de sortie du réseau.
            dropout_rate (float): taux de dropout pour la régularisation.
        """
        super().__init__()
        self.reseau = nn.Sequential(
            nn.Linear(dimension_embedding, 4 * dimension_embedding),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(4 * dimension_embedding, dimension_embedding)
        )

    def forward(self, x):
        """
        Args:
            x (torch.Tensor): tenseur d'entrée.

        Returns:
            torch.Tensor: tenseur transformé par le MLP.
        """
        return self.reseau(x)

# ----------------------------
# Bloc Transformer (original, pour compatibilité avec pyAI.py)
# ----------------------------
class Block(nn.Module):
    """
    Un bloc Transformer standard : attention multi-têtes puis réseau
    feed-forward, chacun précédé d'une normalisation (pre-LayerNorm) et
    suivi d'une connexion résiduelle.
    """

    def __init__(self, dimension_embedding, taille_bloc, nb_tetes, dropout_rate=0.2):
        """
        Args:
            dimension_embedding (int): dimension des vecteurs traités par le bloc.
            taille_bloc (int): longueur maximale de la séquence (contexte).
            nb_tetes (int): nombre de têtes d'attention.
            dropout_rate (float): taux de dropout pour la régularisation.
        """
        super().__init__()
        self.attention = MultiHeadAttention(dimension_embedding, taille_bloc, nb_tetes)
        self.reseau_ffwd = FeedForward(dimension_embedding, dropout_rate)
        self.norme1 = nn.LayerNorm(dimension_embedding)
        self.norme2 = nn.LayerNorm(dimension_embedding)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, x):
        """
        Args:
            x (torch.Tensor): tenseur d'entrée de forme (batch, temps, canaux).

        Returns:
            torch.Tensor: tenseur de même forme, après attention et feed-forward.
        """
        x = x + self.dropout(self.attention(self.norme1(x)))
        x = x + self.dropout(self.reseau_ffwd(self.norme2(x)))
        return x

# ----------------------------
# Nouvelles classes optimisées (optionnelles)
# ----------------------------
class SharedMultiHeadAttention(nn.Module):
    """
    Attention multi-têtes avec projection partagée pour Q, K, V.
    Réduit le nombre de paramètres en partageant les couches linéaires entre les têtes.
    """

    def __init__(self, dimension_embedding, taille_bloc, nb_tetes):
        """
        Args:
            dimension_embedding (int): dimension des vecteurs d'entrée/sortie.
            taille_bloc (int): longueur maximale de la séquence.
            nb_tetes (int): nombre de têtes d'attention en parallèle.
        """
        super().__init__()
        taille_tete = dimension_embedding // nb_tetes
        self.dimension_embedding = dimension_embedding
        self.nb_tetes = nb_tetes
        self.taille_tete = taille_tete

        # Projection partagée pour Q, K, V
        self.shared_proj = nn.Linear(dimension_embedding, 3 * dimension_embedding, bias=False)
        self.projection = nn.Linear(dimension_embedding, dimension_embedding)
        self.register_buffer('triangle_inferieur', torch.tril(torch.ones(taille_bloc, taille_bloc)))

    def forward(self, x):
        """
        Args:
            x (torch.Tensor): tenseur d'entrée de forme (batch, temps, canaux).

        Returns:
            torch.Tensor: sortie combinée de toutes les têtes, reprojetée dans l'espace de dimension_embedding.
        """
        batch, seq_len, _ = x.shape

        # Projection partagée pour Q, K, V
        qkv = self.shared_proj(x)  # (batch, seq_len, 3 * dimension_embedding)
        qkv = qkv.chunk(3, dim=-1)  # Séparation en Q, K, V

        # Reshape pour l'attention multi-têtes
        q = qkv[0].view(batch, seq_len, self.nb_tetes, self.taille_tete).transpose(1, 2)
        k = qkv[1].view(batch, seq_len, self.nb_tetes, self.taille_tete).transpose(1, 2)
        v = qkv[2].view(batch, seq_len, self.nb_tetes, self.taille_tete).transpose(1, 2)

        # Calcul de l'attention
        scores = torch.matmul(q, k.transpose(-2, -1)) / (self.taille_tete ** 0.5)
        scores = scores.masked_fill(
            self.triangle_inferieur[:seq_len, :seq_len].unsqueeze(0).unsqueeze(0) == 0,
            float('-inf')
        )
        scores = F.softmax(scores, dim=-1)

        # Application de l'attention
        out = torch.matmul(scores, v)  # (batch, nb_tetes, seq_len, taille_tete)
        out = out.transpose(1, 2).contiguous().view(batch, seq_len, -1)  # (batch, seq_len, dimension_embedding)

        # Projection finale
        return self.projection(out)

class LowRankFeedForward(nn.Module):
    """
    Réseau FeedForward avec approximation de rang faible.
    Réduit le nombre de paramètres en utilisant une décomposition de rang faible.
    """

    def __init__(self, dimension_embedding, rank=16, dropout_rate=0.2):
        """
        Args:
            dimension_embedding (int): dimension d'entrée et de sortie.
            rank (int): rang de l'approximation (plus petit = moins de paramètres).
            dropout_rate (float): taux de dropout.
        """
        super().__init__()
        self.rank = rank
        self.up = nn.Linear(dimension_embedding, rank, bias=False)
        self.down = nn.Linear(rank, 4 * dimension_embedding, bias=False)
        self.final = nn.Linear(4 * dimension_embedding, dimension_embedding)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, x):
        """
        Args:
            x (torch.Tensor): tenseur d'entrée.

        Returns:
            torch.Tensor: tenseur transformé par le MLP à rang faible.
        """
        x = self.down(self.relu(self.up(x)))  # (batch, seq_len, 4 * dimension_embedding)
        return self.final(self.dropout(x))

class OptimizedTransformerBlock(nn.Module):
    """
    Bloc Transformer optimisé :
    - Utilise SharedMultiHeadAttention pour réduire les paramètres.
    - Utilise LowRankFeedForward pour réduire les paramètres.
    - Ajoute des tokens de réflexion pour améliorer la modélisation des dépendances longues.
    - Ajoute une mémoire externe pour étendre le contexte.
    """

    def __init__(
        self,
        dimension_embedding,
        taille_bloc,
        nb_tetes,
        dropout_rate=0.2,
        memory_size=64,
        num_reflection_tokens=4,
        rank=16
    ):
        """
        Args:
            dimension_embedding (int): dimension des vecteurs traités par le bloc.
            taille_bloc (int): longueur maximale de la séquence (contexte).
            nb_tetes (int): nombre de têtes d'attention.
            dropout_rate (float): taux de dropout.
            memory_size (int): taille de la mémoire externe.
            num_reflection_tokens (int): nombre de tokens de réflexion.
            rank (int): rang pour le FeedForward à rang faible.
        """
        super().__init__()
        self.dimension_embedding = dimension_embedding
        self.memory_size = memory_size
        self.num_reflection_tokens = num_reflection_tokens

        # Mémoire externe (apprise)
        self.memory = nn.Parameter(torch.randn(1, memory_size, dimension_embedding))

        # Tokens de réflexion (appris)
        self.reflection_tokens = nn.Parameter(
            torch.randn(1, num_reflection_tokens, dimension_embedding)
        )

        # Attention multi-têtes avec poids partagés
        self.attention = SharedMultiHeadAttention(
            dimension_embedding,
            taille_bloc + memory_size + num_reflection_tokens,
            nb_tetes
        )

        # FeedForward à rang faible
        self.reseau_ffwd = LowRankFeedForward(dimension_embedding, rank, dropout_rate)

        # Normalisation et dropout
        self.norme1 = nn.LayerNorm(dimension_embedding)
        self.norme2 = nn.LayerNorm(dimension_embedding)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, x):
        """
        Args:
            x (torch.Tensor): tenseur d'entrée de forme (batch, temps, canaux).

        Returns:
            torch.Tensor: tenseur de même forme, après attention et feed-forward.
        """
        batch, seq_len, _ = x.shape

        # Ajouter la mémoire et les tokens de réflexion
        memory_expanded = self.memory.expand(batch, -1, -1)
        reflection_expanded = self.reflection_tokens.expand(batch, -1, -1)
        extended_x = torch.cat([memory_expanded, reflection_expanded, x], dim=1)

        # Attention
        attn_out = self.attention(self.norme1(extended_x))
        # Ne garder que la partie correspondant à x (ignorer mémoire et tokens de réflexion)
        attn_out = attn_out[:, -seq_len:]
        x = x + self.dropout(attn_out)

        # FeedForward
        x = x + self.dropout(self.reseau_ffwd(self.norme2(x)))

        return x