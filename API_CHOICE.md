# API Choice

- Étudiant : Ibrahima Dieng
- API choisie : Agify
- URL base : https://api.agify.io
- Documentation officielle : https://agify.io/documentation
- Auth : None

- Endpoints testés :
  - GET https://api.agify.io?name={name} — prédit l'âge à partir d'un prénom
  - GET https://api.agify.io?name={name}&country_id={code} — avec filtre par pays
  - GET https://api.agify.io?name[]={name1}&name[]={name2} — requête batch (plusieurs prénoms)

- Hypothèses de contrat (champs attendus, types, codes) :
  - Réponse HTTP 200
  - Content-Type: application/json
  - Champs : `name` (string), `age` (integer ou null), `count` (integer)
  - Requête batch → liste de résultats
  - Prénom inconnu → `age` null, HTTP 200

- Limites / rate limiting connu :
  - Plan gratuit : 1000 requêtes/jour
  - Pas de rate limiting strict signalé (pas de 429 documenté)

- Risques :
  - `age` peut être null si le prénom est trop rare
  - Latence variable selon la charge serveur
  - Disponibilité non garantie (service tiers)
