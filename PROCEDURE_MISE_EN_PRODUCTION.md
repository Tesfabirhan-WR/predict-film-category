# Procédure de mise en production

API de classification de films (horreur / comédie) : FastAPI, Docker, GitHub Actions, Azure Container Apps.

> **Règle d'or :** un mot de passe, un secret ou une clé ne s'écrit jamais dans ce fichier, dans le code ni dans une conversation. Ils sont stockés dans les *secrets* GitHub.

## 1. Vue d'ensemble

```
Code + model/  →  git push  →  GitHub Actions (test → image → publier)  →  Registre Azure (ACR)
                                                                              │
                                              déploiement manuel (az containerapp update)
                                                                              ↓
                                                              Application de conteneur (URL publique)
```

- **Identifiant de version :** le *commit* Git (`git rev-parse HEAD`), utilisé comme étiquette de l'image.
- **Pourquoi le déploiement est manuel :** sur le compte de formation, le rôle est *Contributeur*. Le robot GitHub peut construire l'image et la ranger dans le registre, mais pas ordonner à Azure de la mettre en ligne (pas de droit `roleAssignments/write`). C'est donc la personne responsable qui déploie, en indiquant l'identifiant du commit.

## 2. Variables à renseigner

| Variable | Valeur | Remarque |
|---|---|---|
| `RG` | `<groupe-de-ressources>` | Groupe partagé de la formation : ne jamais le supprimer |
| `ACR` | `<nomregistre>` | Unique au monde, minuscules, sans tiret |
| `IMAGE` | `<nom-image>` | Ex. nom du dépôt |
| `APP` | `<nom-application>` | Application de conteneur |
| `ENV` | `<nom-environnement>` | Environnement des applications de conteneur |
| `URL` | `https://<fqdn>` | Adresse publique de l'application |
| `PORT` | `<port-api>` | Port d'écoute de l'API (port cible de l'ingress) |

Secrets GitHub (dépôt → Settings → Secrets) : adresse du registre, nom d'utilisateur administrateur, mot de passe administrateur.

## 3. Prérequis

- [ ] `az login` fait (option code d'appareil si la fenêtre de connexion pose problème sous Windows)
- [ ] Docker Desktop lancé (pour les tests locaux)
- [ ] Dossier `model/` complet : `model.keras`, `tfidf.joblib`, `metrics.json`, `reference_sample.csv`
- [ ] Registre créé avec l'utilisateur administrateur activé
- [ ] Les trois secrets enregistrés dans GitHub
- [ ] Workflow présent dans `.github/workflows/` (avec un **s**)

## 4. Procédure de mise en production

### Étape 1 : Contrôler en local

```bash
pytest
python check_quality.py          # barrière qualité (config.yaml + metrics.json)
docker build -t IMAGE:local .
docker run -p PORT:PORT IMAGE:local
```

Tester trois cas sur `/docs` : texte valide, texte invalide, cas limite (très court). Résultat attendu : une classe pour le cas valide, un message d'erreur clair pour les deux autres.

### Étape 2 : Envoyer le code

```bash
git add .
git commit -m "feat: <description du changement>"
git push
```

### Étape 3 : Vérifier la chaîne GitHub Actions

Dans l'onglet **Actions**, attendre trois jobs verts :

1. `test` : installation, barrière qualité, tests
2. `image` : construction de l'image, vérification que l'API démarre dedans
3. `publier` : envoi de l'image dans le registre, étiquetée avec l'identifiant du commit

Si un job est rouge, **ne pas déployer** : corriger, puis refaire un `git push`.

### Étape 4 : Noter l'identifiant du commit à déployer

```bash
git rev-parse HEAD
```

Vérifier qu'il existe dans le registre :

```bash
az acr repository show-tags --name ACR --repository IMAGE --output table
```

Si l'étiquette est absente (erreur `MANIFEST_UNKNOWN` au déploiement), le job `publier` n'est pas passé ou l'étiquette est mauvaise.

### Étape 5 : Déployer à la main

```bash
az containerapp update \
  --name APP \
  --resource-group RG \
  --image ACR.azurecr.io/IMAGE:<identifiant-du-commit>
```

Première création de l'application (une seule fois) : authentification par secret avec l'utilisateur administrateur du registre (pas l'identité managée), 1 processeur, 2 Go de mémoire, entrée (*ingress*) activée et externe, port cible = port de l'API. Le mot de passe est saisi dans le portail ou le terminal, jamais écrit dans un fichier.

### Étape 6 : Vérifier la mise en ligne

Récupérer l'adresse publique :

```bash
az containerapp show --name APP --resource-group RG \
  --query properties.configuration.ingress.fqdn --output tsv
```

Puis depuis le navigateur ou `curl` :

| Contrôle | Attendu |
|---|---|
| `URL/health` | « ok » + version du modèle (+ identifiant du commit) |
| `URL/predict` avec un texte valide | classe, probabilité, version |
| `URL/predict` avec un texte vide | message d'erreur clair |
| `URL/predict` avec un texte très court | message d'erreur clair ou réponse cohérente |

Les réponses doivent être les mêmes qu'en local. Un `Not Found` sur l'adresse seule est normal : ajouter `/health` ou `/docs`.

### Étape 7 : Consigner la version

Ajouter une ligne dans le **journal des versions** (section 6) : date, commit, changement, résultat des contrôles.

## 5. Retour en arrière (rollback)

À utiliser si `/health` ou `/predict` ne répondent plus comme prévu après un déploiement.

1. Retrouver l'identifiant du dernier commit stable dans le journal des versions.
2. Redéployer cette image :

   ```bash
   az containerapp update \
     --name APP \
     --resource-group RG \
     --image ACR.azurecr.io/IMAGE:<ancien-identifiant>
   ```

3. Vérifier `/health` : l'ancien identifiant est de retour (et une route ajoutée depuis, par exemple `/hello`, a disparu).
4. Consigner le retour en arrière dans le journal, avec la cause.

## 6. Dépannage

| Ce que vous voyez | Ce que ça veut dire | Où chercher |
|---|---|---|
| `MANIFEST_UNKNOWN` | Image absente du registre ou mauvaise étiquette | `az acr repository show-tags` |
| `roleAssignments/write` refusé | Le rôle ne permet pas de donner des droits | Utiliser l'utilisateur administrateur du registre |
| Le conteneur redémarre sans cesse | Mémoire insuffisante (TensorFlow) | Mémoire allouée : 2 Go ; `az containerapp logs show --name APP --resource-group RG` |
| Pas d'adresse publique | Entrée (*ingress*) désactivée | Paramètres réseau de l'application |
| `Not Found` sur l'adresse | L'API marche, mais cette adresse n'est pas une route | Ajouter `/health` ou `/docs` |
| Job `publier` rouge | Secrets absents ou faux | Secrets du dépôt GitHub |
| Workflow absent dans Actions | Mauvais dossier ou Actions désactivées | `.github/workflows` (avec un **s**), réglages du dépôt |

## 7. Journal des versions

Une ligne par déploiement ou retour en arrière. Ne jamais supprimer une ligne : en cas de correction, ajouter une nouvelle ligne.

| Version | Date | Commit (court) | Modèle | F1 test | Changement | Contrôles (`/health`, `/predict`) | Action | Responsable |
|---|---|---|---|---|---|---|---|---|
| 1.0.0 | `<jj/mm/aaaa>` | `<sha>` | 1.0.0 | `<0.xx>` | Première mise en ligne : API `/health` et `/predict`, modèle du notebook | `<OK / KO>` | Déploiement | `<nom>` |
| 1.1.0 | `<jj/mm/aaaa>` | `<sha>` | 1.0.0 | `<0.xx>` | Ajout de la route `/hello` (exercice de mise à jour) | `<OK / KO>` | Déploiement | `<nom>` |
| 1.0.0 | `<jj/mm/aaaa>` | `<sha de la 1.0.0>` | 1.0.0 | `<0.xx>` | Retour en arrière : `/hello` retirée | `<OK / KO>` | Retour en arrière | `<nom>` |
| | | | | | | | | |

**Légende :**
- *Version* : numéro de l'application (majeur.mineur.correctif). Le *Modèle* est la version écrite dans `metrics.json`.
- *Commit* : identifiant à utiliser comme étiquette de l'image.
- *Action* : Déploiement, Retour en arrière, Correctif.

**Règle de numérotation :**
- Nouveau modèle ou changement de comportement de `/predict` : version majeure ou mineure.
- Nouvelle route ou changement sans impact sur le modèle : version mineure.
- Correction sans changement de comportement : version de correctif.
