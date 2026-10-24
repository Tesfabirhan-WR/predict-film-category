# Predict Film Category
### Project Structure

```text
predict-film-category/
├── .github/
│   └── workflows/
├── data/
│   └── textes_films_horreur_comedie.csv
├── model/
│   ├── metrics.json
│   ├── model.keras
│   ├── model2.png
│   ├── reference_sample.csv
│   └── tfidf.joblib
├── notebook/
│   ├── my_log_dir/
│   │   ├── 20261023-144955/
│   │   ├── 20261023-145843/
│   │   ├── 20261024-195835/
│   │   ├── train/
│   │   ├── validation/
│   │   └── projector_config.pbtxt
│   └── predFilm.ipynb
├── resources/
│   ├── briefs/
│   │   ├── c12-fiche-planifier-le-projet-6ad934865387c314988957.pdf
│   │   └── suite-deploiement-pipeline-production-1-6ad92fa254ca6782626714.pdf
│   ├── api_film.png
│   ├── image.png
│   ├── pipeline.png
│   └── tensorboard.png
├── src/
│   ├── app.py
│   ├── app.py:Zone.Identifier
│   ├── tensorboard.py
│   └── tree.py
├── tests/
├── .dockerignore
├── .env
├── .gitattributes
├── .gitignore
├── config.yaml
├── dockerfile
├── FIN_DE_VIE.md
├── PLAN.md
├── PROCEDURE_MISE_EN_PRODUCTION.md
├── Project planning.md
├── README.md
├── requirements-api.txt
├── requirements-dev.txt
├── requirements.txt
└── structure.txt
```


### Part I: 

<p align="center">
  <img src="resources/pipeline.png" alt="Pipeline diagram" width="900">
</p>

### Part 2 : Fast API

```text

pip install fastapi
pip install uvicorn

```
**`PROCEDURE_MISE_EN_PRODUCTION.md`**
- It describes the full path: local checks, `git push`, the three GitHub Actions jobs, a manual `az containerapp update` using the commit ID, and checks on `/health` and `/predict`.
- It has a rollback section and a troubleshooting table with the errors from your brief (`MANIFEST_UNKNOWN`, `roleAssignments/write`, restart loops, `Not Found`).
- The **journal des versions** table has pre-filled lines for the first release (1.0.0), the `/hello` update (1.1.0) and the rollback to 1.0.0, plus an empty row. The numbering rule is explained under the table.

**`FIN_DE_VIE.md`**
- It lists the triggers for retiring the service and what to delete, keep or archive.
- It covers data and compliance notes, and an 8-step checklist with the delete and verify commands. The checklist stops traffic, records the cost, deletes the app, its environment and the registry, and cleans GitHub and your computer. Your shared resource group is never touched.
- It ends with a responsibilities table and a closing sheet to fill in.

