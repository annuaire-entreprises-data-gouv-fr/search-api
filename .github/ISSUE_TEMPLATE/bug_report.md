---
name: "🐞 Signaler un bug API"
about: Signalez un problème rencontré avec l'API.
title: "[BUG] Résumé du problème"
labels: bug
assignees: HAEKADI
---

## ❗ Sujet du problème

Décrivez clairement le problème rencontré avec l'API.  
Exemple : *« L'endpoint `/search` renvoie une erreur 500 au lieu d'une réponse 200. »*

---

## 🔁 Étapes pour reproduire le bug

Listez les étapes exactes pour reproduire le problème dans l'API :

1. Effectuer une requête `GET` sur l'endpoint `/search`
2. Ajouter les paramètres nécessaires (par exemple, `?q=terme_de_recherche`)
3. Consulter la réponse API
4. 🚨 Résultat observé : *Expliquez ce qui se passe.*

---

## ✅ Comportement attendu

Décrivez ce à quoi vous vous attendiez lorsque vous avez effectué les actions ci-dessus.

Exemple : *« L'API aurait dû renvoyer un code HTTP 200 avec les résultats de la recherche. »*

---

## 💥 Comportement actuel

Expliquez ce qui se passe actuellement au lieu du comportement attendu.

Exemple : *« L'API renvoie une erreur 500 avec le message 'Internal Server Error'. »*

---

## 📝 Détails de la requête API

### Méthode HTTP
`GET`

### Endpoint
`/search`

### Paramètres de la requête (si applicable)
- **query parameters** : `?q=terme_de_recherche`
- **headers** : Aucun nécessaire

---

## 📄 Réponse de l'API

### Code HTTP retourné :
`500 Internal Server Error`

### Corps de la réponse (si applicable) :
```json
{
  "erreur": "Internal Server Error"
}
