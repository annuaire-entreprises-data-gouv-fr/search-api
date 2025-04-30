---
name: "✨ Proposer une amélioration"
about: Suggérez une nouvelle fonctionnalité ou une amélioration pour l'API.
title: "[FEATURE] Résumé de la fonctionnalité"
labels: enhancement
assignees:
  - HAEKADI
---

## 🧩 Contexte de la demande

*Cette amélioration est-elle liée à un problème existant ? Si oui, décrivez-le brièvement.*

Exemple : *« Lors de l'utilisation de l'endpoint `/search`, il manque la possibilité de filtrer par catégorie. »*

---

## 💡 Description de la fonctionnalité souhaitée

*Décrivez clairement la fonctionnalité ou l'amélioration que vous proposez.*

Exemple : *« Ajouter un paramètre `category` à l'endpoint `/search` pour filtrer les résultats par catégorie spécifique. »*

---

## 🔄 Comportement actuel

*Expliquez le comportement actuel de l'API en relation avec votre demande.*

Exemple : *« Actuellement, l'endpoint `/search` retourne tous les résultats sans possibilité de filtrer par catégorie. »*

---

## ✅ Comportement attendu

*Décrivez le comportement attendu si la fonctionnalité est mise en œuvre.*

Exemple : *« L'endpoint `/search` devrait permettre de filtrer les résultats en fonction du paramètre `category` fourni. »*

---

## 🔁 Alternatives envisagées

*Avez-vous considéré d'autres solutions ou contournements ? Si oui, décrivez-les.*

Exemple : *« Une alternative serait de récupérer tous les résultats et de filtrer côté client, mais cela augmente la charge et le temps de traitement. »*

---

## 📎 Informations supplémentaires

*Ajoutez toute information pertinente, comme des exemples de requêtes, des captures d'écran ou des références à des discussions antérieures.*

Exemple :

```http
GET /search?q=entreprise&category=technologie
