# PLAN.md: From Notebook to Live API (5 days, 1 person)

Project objective: film classifier (horror/comedy) from a notebook to a public API on Azure.

- **Human resource:** 1 person (me) · **Duration:** 5 working days · **Capacity:** ~7 h/day (35 h)
- **Planning tool:** Notion (this file can be imported as a page)
- **Dates:** Day 1 = Monday 26/10/2026 (assumption: change them if you start another day)
- **How to use:** fill **Charge réelle** after each task, tick the box in the *Fait* column, update the totals at the end of each day

## 1. Planning table

| Fait | ID | Tâche | Dépend de | Charge estimée (h) | Charge réelle (h) | Ressources humaines | Ressources matérielles | Ressources techniques | Ressources financières | Date prévue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [ ] | 1.1 | Create GitHub repo, local folders (notebooks/, model/, src/, tests/), virtual env, .gitignore, first commit | - | 0.5 |  | Me (1 pers.) | PC, internet | Git, GitHub, VS Code | 0 € | Mon 26/10/2026 |
| [ ] | 1.2 | Install and pin libraries in requirements.txt (pandas, scikit-learn, tensorflow-cpu, keras-tuner, optuna, joblib, fastapi, uvicorn, pytest) | 1.1 | 0.5 |  | Me (1 pers.) | PC, internet | Python, pip, venv | 0 € | Mon 26/10/2026 |
| [ ] | 1.3 | Part 1: Audit and cleaning (load CSV, count rows and categories, text lengths, str.strip, drop_duplicates, one-sentence finding) | 1.2 | 1 |  | Me (1 pers.) | PC, internet | pandas | 0 € | Mon 26/10/2026 |
| [ ] | 1.4 | Part 2: Split with train_test_split + stratify: 60% train / 20% test / 20% production | 1.3 | 0.5 |  | Me (1 pers.) | PC, internet | scikit-learn | 0 € | Mon 26/10/2026 |
| [ ] | 1.5 | Part 3: TF-IDF fitted on train only, transform the 3 parts with the same object | 1.4 | 0.5 |  | Me (1 pers.) | PC, internet | TfidfVectorizer | 0 € | Mon 26/10/2026 |
| [ ] | 1.6 | Part 4a: Baselines - logistic regression + Naive Bayes, F1 on 5 seeds (validation from train) | 1.5 | 1 |  | Me (1 pers.) | PC, internet | scikit-learn, f1_score | 0 € | Mon 26/10/2026 |
| [ ] | 1.7 | Part 4b: Simple network (1 hidden layer, small dropout, EarlyStopping), F1 on 5 seeds | 1.5 | 1 |  | Me (1 pers.) | PC, internet | Keras, EarlyStopping | 0 € | Mon 26/10/2026 |
| [ ] | 1.8 | Compute noise margin 1.96*sqrt(p(1-p)/n) for each score | 1.6, 1.7 | 0.5 |  | Me (1 pers.) | PC, internet | Python (formula) | 0 € | Mon 26/10/2026 |
| [ ] | 1.9 | Add a title for each notebook part and re-run top to bottom | 1.8 | 0.5 |  | Me (1 pers.) | PC, internet | Jupyter | 0 € | Mon 26/10/2026 |
| [ ] | 1.10 | Commit and push; end-of-day notes in Notion | 1.9 | 0.25 |  | Me (1 pers.) | PC, internet | Git | 0 € | Mon 26/10/2026 |
| [ ] | 1.11 | Buffer | - | 0.75 |  | Me (1 pers.) | - | - | - | Mon 26/10/2026 |
| [ ] | 2.1 | Part 5a: write build_model(...) with 5 hyperparameters (layers, neurons, dropout, regularisation, learning rate) | 1.8 | 0.75 |  | Me (1 pers.) | PC, internet | Keras | 0 € | Tue 27/10/2026 |
| [ ] | 2.2 | Part 5b: KerasTuner RandomSearch, 20 trials (disable tracking files if Windows errno 22 / tensorboard) | 2.1 | 1 |  | Me (1 pers.) | PC, internet | KerasTuner | 0 € | Tue 27/10/2026 |
| [ ] | 2.3 | Part 6: Optuna with same 5 settings, same ranges, 20 trials, reuse build_model; compare both tools with noise margin | 2.1, 2.2 | 1.25 |  | Me (1 pers.) | PC, internet | Optuna | 0 € | Tue 27/10/2026 |
| [ ] | 2.4 | Part 7a: retrain best settings on full train set, 5 seeds; compare with starting network and best simple model | 2.3 | 1 |  | Me (1 pers.) | PC, internet | Keras, scikit-learn | 0 € | Tue 27/10/2026 |
| [ ] | 2.5 | Part 7b: measure on test set ONCE; honest conclusion | 2.4 | 0.5 |  | Me (1 pers.) | PC, internet | scikit-learn | 0 € | Tue 27/10/2026 |
| [ ] | 2.6 | Part 8: save to model/ (.keras, TF-IDF joblib, metrics.json UTF-8, reference data sample) | 2.5 | 1 |  | Me (1 pers.) | PC, internet | joblib, json, model.save | 0 € | Tue 27/10/2026 |
| [ ] | 2.7 | Restart kernel, run notebook top to bottom; push notebook + model/ | 2.6 | 0.5 |  | Me (1 pers.) | PC, internet | Jupyter, Git | 0 € | Tue 27/10/2026 |
| [ ] | 2.8 | Buffer (KerasTuner/Windows issues are common) | - | 1 |  | Me (1 pers.) | - | - | - | Tue 27/10/2026 |
| [ ] | 3.1 | A1: FastAPI app, model loaded once at startup, /health and /predict, pydantic validation, clear errors | 2.7 | 1.5 |  | Me (1 pers.) | PC, internet | FastAPI, pydantic, uvicorn | 0 € | Wed 28/10/2026 |
| [ ] | 3.2 | A2: run with uvicorn, open /docs, test 3 cases (valid, invalid, very short) | 3.1 | 0.5 |  | Me (1 pers.) | PC, internet | uvicorn, /docs | 0 € | Wed 28/10/2026 |
| [ ] | 3.3 | A3: pytest tests (API responds, valid works, invalid refused, model min score) + pytest.ini pythonpath | 3.2 | 1 |  | Me (1 pers.) | PC, internet | pytest, TestClient | 0 € | Wed 28/10/2026 |
| [ ] | 3.4 | A4: config.yaml (min F1, min test size) + check_quality.py; justify threshold with noise margin | 2.7, 3.3 | 0.75 |  | Me (1 pers.) | PC, internet | YAML, Python | 0 € | Wed 28/10/2026 |
| [ ] | 3.5 | B5: Dockerfile (slim base, tensorflow-cpu, pinned versions) + .dockerignore; docker build; note image size | 3.3 | 1 |  | Me (1 pers.) | PC, internet, Docker Desktop | Docker | 0 € | Wed 28/10/2026 |
| [ ] | 3.6 | B6: docker run and redo the 3 tests of A2 | 3.5 | 0.5 |  | Me (1 pers.) | PC, internet, Docker Desktop | Docker | 0 € | Wed 28/10/2026 |
| [ ] | 3.7 | Commit and push; end-of-day notes | 3.4, 3.6 | 0.25 |  | Me (1 pers.) | PC, internet | Git | 0 € | Wed 28/10/2026 |
| [ ] | 3.8 | Buffer | - | 0.5 |  | Me (1 pers.) | - | - | - | Wed 28/10/2026 |
| [ ] | 4.1 | C7: workflow in .github/workflows/ - job test (install, quality gate, pytest) then job image (needs: test; build + check API starts) | 3.4, 3.5 | 1.25 |  | Me (1 pers.) | PC, internet, Docker Desktop | GitHub Actions | 0 € | Thu 29/10/2026 |
| [ ] | 4.2 | C8: raise threshold above reachable, push (test red, image not started); restore threshold, all green | 4.1 | 0.5 |  | Me (1 pers.) | PC, internet, Docker Desktop | GitHub Actions | 0 € | Thu 29/10/2026 |
| [ ] | 4.3 | D9: create Azure Container Registry (Basic, unique lowercase name, no dashes); enable admin user | 3.7 | 0.5 |  | Me (1 pers.) | PC, internet, Azure account | Azure portal, ACR | ~0.17 $/day (ACR Basic) | Thu 29/10/2026 |
| [ ] | 4.4 | D10a: store the 3 values as GitHub secrets (never in code or chat) | 4.3 | 0.25 |  | Me (1 pers.) | PC, internet | GitHub secrets | 0 € | Thu 29/10/2026 |
| [ ] | 4.5 | D10b: add job publier (needs: image), docker/login-action, push image tagged with github.sha | 4.1, 4.4 | 1 |  | Me (1 pers.) | PC, internet, Docker Desktop | GitHub Actions, docker/login-action | ACR storage (included) | Thu 29/10/2026 |
| [ ] | 4.6 | D11: create Container App from the image (secret auth, 1 CPU, 2 GB, external ingress, target port) | 4.5 | 1 |  | Me (1 pers.) | PC, internet, Azure account | Azure Container Apps, az CLI | 0 to 1 $ (free grant) | Thu 29/10/2026 |
| [ ] | 4.7 | D12: test /health and /predict (3 cases) on public URL; show the trainer | 4.6 | 0.5 |  | Me (1 pers.) | PC, internet, Azure account | Browser | 0 to 1 $ (free grant) | Thu 29/10/2026 |
| [ ] | 4.8 | Buffer (permissions, MANIFEST_UNKNOWN, restart loops) | - | 1 |  | Me (1 pers.) | - | - | - | Thu 29/10/2026 |
| [ ] | 5.1 | E13: add /hello route, push, 3 green jobs, deploy new image by hand (az containerapp update) with commit id | 4.7 | 1 |  | Me (1 pers.) | PC, internet, Azure account | az CLI, git rev-parse | 0 to 1 $ (free grant) | Fri 30/10/2026 |
| [ ] | 5.2 | E14: rollback - redeploy the previous commit | 5.1 | 0.5 |  | Me (1 pers.) | PC, internet, Azure account | az CLI | 0 to 1 $ (free grant) | Fri 30/10/2026 |
| [ ] | 5.3 | F15a: note estimated cost of what was created | 5.2 | 0.25 |  | Me (1 pers.) | PC, internet, Azure account | Azure Cost Management | 0 € | Fri 30/10/2026 |
| [ ] | 5.4 | F15b: delete Container App, its environment and the registry (never the shared resource group) | 5.3 | 0.5 |  | Me (1 pers.) | PC, internet, Azure account | Azure portal / az CLI | Stops costs | Fri 30/10/2026 |
| [ ] | 5.5 | Write README.md (how to run notebook, API, tests, quality gate, Docker, workflow) | 4.7 | 1 |  | Me (1 pers.) | PC, internet | Markdown | 0 € | Fri 30/10/2026 |
| [ ] | 5.6 | Write the one-page sheet in your own words (model journey, threshold, manual deploy, automation needs, limits) | 5.4 | 1 |  | Me (1 pers.) | PC, internet | Notion / Word | 0 € | Fri 30/10/2026 |
| [ ] | 5.7 | Gather all proofs | 5.4 | 0.5 |  | Me (1 pers.) | PC, internet | Screenshots | 0 € | Fri 30/10/2026 |
| [ ] | 5.8 | Final check of repo against deliverables; push | 5.5, 5.6, 5.7 | 0.5 |  | Me (1 pers.) | PC, internet | Git, GitHub | 0 € | Fri 30/10/2026 |
| [ ] | 5.9 | Buffer | - | 1 |  | Me (1 pers.) | - | - | - | Fri 30/10/2026 |
|  |  | **TOTAL** |  | **32.25** |  |  |  |  | **~1 $ (if resources deleted on Day 5)** |  |

## 2. Totals per day

| Day | Date | Charge estimée (h) | Charge réelle (h) | Écart (h) |
| --- | --- | --- | --- | --- |
| Day 1 | Mon 26/10/2026 | 7.0 |  |  |
| Day 2 | Tue 27/10/2026 | 7.0 |  |  |
| Day 3 | Wed 28/10/2026 | 6.0 |  |  |
| Day 4 | Thu 29/10/2026 | 6.0 |  |  |
| Day 5 | Fri 30/10/2026 | 6.25 |  |  |
| **Total** |  | **32.25** |  |  |

## 3. Resources summary

| Type | Resources |
| --- | --- |
| Humaines | 1 person (junior data engineer), ~7 h/day, trainer for help after 20 min blocked and for the demo on step D12 |
| Matérielles | Personal computer (enough RAM for TensorFlow), internet connection, Docker Desktop |
| Techniques | Python, pandas, scikit-learn, Keras, KerasTuner, Optuna, joblib, FastAPI, uvicorn, pytest, Docker, Git/GitHub (Actions, secrets), Azure (Container Registry, Container Apps, az CLI), VS Code, Notion |
| Financières | Azure training account (Contributor role); see budget below |

## 4. Budget estimate

Prices are estimates from Microsoft public pricing (USD); they can vary by region.

| Item | Assumption | Estimated cost |
| --- | --- | --- |
| Azure Container Registry (Basic) | Up ~2 days (Day 4 to Day 5), ~0.167 $/day, 10 GB included | ~0.35 $ |
| Azure Container Apps | 1 vCPU, 2 GB, ~1 to 2 days; monthly free grant of 180,000 vCPU-s and 360,000 GiB-s | 0 to 1 $ |
| GitHub Actions | 3 jobs per push, ~10 pushes (free minutes on a free account; check if repo is private) | 0 $ |
| Notion, VS Code, Docker Desktop, GitHub, open source libraries | Free plans | 0 $ |
| **Total cash** | If all Azure resources are deleted on Day 5 | **~1 $** |
| Forgotten resources (risk) | Registry ~5 $/month + always-on Container App ~20 $/month | ~25 to 30 $/month |
| Value of time (optional) | 35 h x 20 €/h (rough junior rate, replace with yours) | ~700 € |

Tips: set an Azure budget alert at 5 $ (Cost Management, Budgets); note the estimated cost in task 5.3 before deleting; do task 5.4 before the end of Day 5.

## 5. Dependencies (critical path)

`1.1 → 1.2 → 1.3 → 1.4 → 1.5 → 1.6/1.7 → 1.8 → 2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.6 → 2.7 → 3.1 → 3.2 → 3.3 → 3.5 → 4.1 → 4.5 → 4.6 → 4.7 → 5.1 → 5.2 → 5.3 → 5.4 → 5.8`

## 6. Risks

| Risk | Mitigation |
| --- | --- |
| Stuck more than 20 min | Ask for help; use the day's buffer |
| KerasTuner errors on Windows | Disable tracking files; install tensorboard |
| Suspiciously high score | Re-check duplicates and TF-IDF fitted on train only |
| Contributor role on Azure | Use registry admin user; deploy by hand |
| Container restarts in a loop | Give 2 GB memory; check az containerapp logs |
| Registry left running | Do task 5.4 before the end of Day 5 |

## 7. Deliverables checklist

- [ ] GitHub repo: notebook, model/, API, tests, thresholds file, quality-gate script, dependency files, Dockerfile, .dockerignore, workflow, README.md
- [ ] Proofs: local tests, local container, green chain, red chain, public URL, /health with commit, /hello added then removed, resources deleted
- [ ] One-page sheet in your own words
