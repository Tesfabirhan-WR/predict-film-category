# Fin de vie du projet

API de classification de films (horreur / comédie) : modèle, application, registre et dépôt.

## 1. Objet

Ce document décrit **quand** et **comment** retirer le service : arrêter la mise en ligne, conserver ce qui doit l'être, supprimer ce qui coûte ou expose, et prouver que c'est fait.

## 2. Déclencheurs de fin de vie

La fin de vie est décidée si l'un des cas suivants se produit :

| Déclencheur | Exemple |
|---|---|
| Fin de la période de formation ou du projet | Rendu validé, plus d'usage prévu |
| Qualité insuffisante | Le F1 ne respecte plus le seuil de `config.yaml` après réentraînement |
| Remplacement | Un nouveau modèle ou une nouvelle API prend la suite |
| Obsolescence technique | Bibliothèques (TensorFlow, FastAPI, Python) plus maintenues |
| Coût | Registre ou application facturés sans usage |
| Sécurité | Faille non corrigeable ou secret compromis |

## 3. Ce qui est concerné

| Élément | Où | Décision à la fin de vie |
|---|---|---|
| Application de conteneur et son environnement | Azure | **Supprimer** |
| Registre de conteneurs (ACR) | Azure | **Supprimer** (facturé tant qu'il existe) |
| Groupe de ressources partagé | Azure | **Conserver, ne jamais supprimer** |
| Secrets GitHub (adresse, utilisateur, mot de passe du registre) | GitHub | **Supprimer** ; changer le mot de passe du registre s'il subsiste |
| Dépôt GitHub (code, notebook, `model/`, workflow) | GitHub | **Archiver** |
| Dossier `model/` (`model.keras`, `tfidf.joblib`, `metrics.json`, échantillon) | Dépôt | **Conserver** avec la dernière version |
| Journal des versions | `PROCEDURE_MISE_EN_PRODUCTION.md` | **Conserver** |
| Images locales Docker | Poste | **Supprimer** si plus utiles |

## 4. Données et conformité

- Les données d'entraînement sont des résumés de films (texte public) : pas de données personnelles prévues.
- L'API ne doit pas conserver les textes envoyés. Vérifier qu'aucun journal ne contient de texte d'utilisateurs avant d'archiver ou de supprimer.
- L'échantillon de référence (`reference_sample.csv`) ne contient que des résumés de films et leur catégorie.
- Aucun secret n'est stocké dans le dépôt : vérifier l'historique Git avant l'archivage.

## 5. Procédure de fin de vie

### Étape 1 : Décider et annoncer

- [x] Décision prise et motif noté (section 2)
- [x] Date de fin de service annoncée aux utilisateurs de l'adresse publique (formateur, relecteurs)

### Étape 2 : Figer la dernière version

- [x] Dernière version consignée dans le journal des versions (commit, F1 test, état)
- [x] Étiquette Git de clôture, par exemple :

  ```bash
  git tag -a fin-de-vie -m "Dernière version avant retrait du service"
  git push origin fin-de-vie
  ```

- [x] Preuves rassemblées : `/health` avec le commit, tests, chaîne verte, capture de l'adresse publique

### Étape 3 : Arrêter le trafic

- [x] Désactiver l'entrée (*ingress*) ou arrêter l'application pour vérifier que personne ne l'utilise
- [x] Constater que l'adresse publique ne répond plus

### Étape 4 : Relever le coût

- [x] Noter le coût estimé de ce qui a été créé (Cost Management) avant suppression

### Étape 5 : Supprimer les ressources Azure

Remplacer les noms par ceux du projet.

```bash
az containerapp delete --name <APP> --resource-group <RG> --yes
az containerapp env delete --name <ENV> --resource-group <RG> --yes
az acr delete --name <ACR> --resource-group <RG> --yes
```

Vérifier qu'il ne reste rien du projet (seules les ressources créées pour lui doivent avoir disparu) :

```bash
az containerapp list --resource-group <RG> --output table
az acr list --resource-group <RG> --output table
```

- [x] Application supprimée
- [x] Environnement supprimé
- [x] Registre supprimé
- [x] Capture d'écran montrant que ces ressources n'existent plus
- [x] Groupe de ressources partagé intact

### Étape 6 : Nettoyer GitHub

- [x] Secrets du dépôt supprimés (Settings → Secrets)
- [x] Workflow désactivé ou supprimé pour éviter des échecs répétés (le job `publier` ne peut plus se connecter au registre)
- [x] README mis à jour : service retiré, date, lien vers ce document
- [x] Dépôt archivé (Settings → Archive this repository)

### Étape 7 : Nettoyer le poste

```bash
docker image rm <IMAGE>:local
docker system prune
```

- [x] Images et conteneurs locaux supprimés
- [x] Environnement virtuel supprimé s'il n'est plus utile

### Étape 8 : Vérifier le coût après suppression

- [x] Après 24 à 48 heures, contrôler dans Cost Management qu'aucune nouvelle dépense n'apparaît

## 6. Ce qui reste après la fin de vie

| Élément conservé | Raison |
|---|---|
| Dépôt archivé (lecture seule) | Preuve du travail, reprise possible |
| `model/` et `metrics.json` | Retrouver la version et le score du modèle |
| Journal des versions | Historique des déploiements et retours en arrière |
| Preuves (captures) | Rendu du projet |

**Reprise possible :** cloner le dépôt, recréer un registre, ajouter les secrets, pousser le code, puis suivre `PROCEDURE_MISE_EN_PRODUCTION.md`.

## 7. Responsabilités

| Rôle | Responsable | Actions |
|---|---|---|
| Décision de fin de vie | `Tesfabirhan` | Étapes 1 et 2 |
| Suppression des ressources Azure | `Tesfabirhan` | Étapes 3 à 5 |
| Nettoyage GitHub et poste | `Tesfabirhan` | Étapes 6 et 7 |
| Contrôle final des coûts | `Tesfabirhan` | Étape 8 |

## 8. Fiche de clôture

| Champ | Valeur |
|---|---|
| Date de fin de service | `28/10/2026` |
| Motif | `<déclencheur de la section 2>` |
| Dernière version déployée | `<version / commit>` |
| F1 test de la dernière version | `0.848 ± 0.032` |
| Coût total estimé | `700 €` |
| Ressources supprimées le | `28/10/2026` |
| Preuve de suppression | `<lien ou nom de la capture>` |
| Leçons apprises | `Deep learning, Git, Azure` |
