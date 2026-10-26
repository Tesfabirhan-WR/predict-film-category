# Project planning: Film Category Prediction

# 🚀 From Notebook to Live API: 5-Day Project Plan

Project objective: take a horror/comedy film classifier from a notebook to a public API on Azure.

- 👤 Team: 1 person
- 🗓️ Duration: 5 working days (~7 h/day, ~6 h planned + ~1 h buffer)
- 🛠️ Tool: Notion, VS Code, Azure, Github

## 📁 Phases

- **P1 · Notebook (8 parts)** | Priority: High | Day 1 - Day 2 | Goal: Model + model/ folder pushed to GitHub
- **P2 · API + tests + quality gate** | Priority: High | Day 3 | Goal: FastAPI /health + /predict, passing tests, config.yaml threshold
- **P3 · Docker container** | Priority: High | Day 3 | Goal: Light image, same answers as local
- **P4 · GitHub Actions (CI)** | Priority: High | Day 4 | Goal: 3 green jobs: test, image, publier
- **P5 · Azure deployment** | Priority: High | Day 4 | Goal: Public URL, trainer demo
- **P6 · Release, rollback, cleanup** | Priority: Medium | Day 5 | Goal: /hello added then removed, resources deleted
- **P7 · Deliverables** | Priority: Medium | Day 5 | Goal: README, proofs, one-page sheet

## 📅 Day 1

**Goal:** Setup + notebook parts 1 to 4: clean data, correct split, TF-IDF, baselines with noise margin

**Total:** 7.0 h | **Date:** (to fill)

- [x]  **1.1** Create GitHub repo, local folders (notebooks/, model/, src/, tests/), virtual env, .gitignore, first commit
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Repo exists, first push done
- [x]  **1.2** Install and pin libraries in requirements.txt (pandas, scikit-learn, tensorflow-cpu, keras-tuner, optuna, joblib, fastapi, uvicorn, pytest)
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: pip install -r requirements.txt works
- [x]  **1.3** Part 1: Audit and cleaning (load CSV, count rows and categories, text lengths, str.strip, drop_duplicates, one-sentence finding)
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: One sentence: what was found, what was fixed
- [x]  **1.4** Part 2: Split with train_test_split + stratify: 60% train / 20% test / 20% production
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Class proportions printed for the 3 parts
- [x]  **1.5** Part 3: TF-IDF fitted on train only, transform the 3 parts with the same object
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: No fit call on test or production
- [x]  **1.6** Part 4a: Baselines - logistic regression + Naive Bayes, F1 on 5 seeds (validation from train)
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: Mean and spread of F1 per model
- [x]  **1.7** Part 4b: Simple network (1 hidden layer, small dropout, EarlyStopping), F1 on 5 seeds
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: Mean and spread of F1
- [x]  **1.8** Compute noise margin 1.96*sqrt(p(1-p)/n) for each score
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Table of scores +/- margin
- [x]  **1.9** Add a title for each notebook part and re-run top to bottom
    - Project: P1 · Notebook (8 parts) | Priority: Medium | Estimate: 0.5 h | Status: Not started
    - Done when: No error
- [x]  **1.10** Commit and push; end-of-day notes in Notion
    - Project: P1 · Notebook (8 parts) | Priority: Low | Estimate: 0.25 h | Status: Not started
    - Done when: Commit visible on GitHub
- [x]  **1.11** Buffer
    - Project: Buffer | Priority: Low | Estimate: 0.75 h | Status: Not started

## 📅 Day 2

**Goal:** Notebook parts 5 to 8: tuned network, honest verdict, complete model/ folder pushed

**Total:** 7.0 h | **Date:** (to fill)

- [x]  **2.1** Part 5a: write build_model(…) with 5 hyperparameters (layers, neurons, dropout, regularisation, learning rate)
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 0.75 h | Status: Not started
    - Done when: Function returns a compiled model
- [x]  **2.2** Part 5b: KerasTuner RandomSearch, 20 trials (disable tracking files if Windows errno 22 / tensorboard)
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: Best score and best settings printed
- [x]  **2.3** Part 6: Optuna with same 5 settings, same ranges, 20 trials, reuse build_model; compare both tools with noise margin
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 1.25 h | Status: Not started
    - Done when: Comparison sentence: better or within margin
- [x]  **2.4** Part 7a: retrain best settings on full train set, 5 seeds; compare with starting network and best simple model
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: Comparison table
- [x]  **2.5** Part 7b: measure on test set ONCE; honest conclusion
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Written conclusion
- [x]  **2.6** Part 8: save to model/ (.keras, TF-IDF joblib, metrics.json UTF-8, reference data sample)
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: 4 files present in model/
- [x]  **2.7** Restart kernel, run notebook top to bottom; push notebook + model/
    - Project: P1 · Notebook (8 parts) | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Notebook runs with no error, push done
- [x]  **2.8** Buffer (KerasTuner/Windows issues are common)
    - Project: Buffer | Priority: Low | Estimate: 1 h | Status: Not started

## 📅 Day 3

**Goal:** API, tests, quality gate, Docker: a tested API running locally and in a light container

**Total:** 6.0 h | **Date:** (to fill)

- [x]  **3.1** A1: FastAPI app, model loaded once at startup, /health and /predict, pydantic validation, clear errors
    - Project: P2 · API + tests + quality gate | Priority: High | Estimate: 1.5 h | Status: Not started
    - Done when: App starts without error
- [x]  **3.2** A2: run with uvicorn, open /docs, test 3 cases (valid, invalid, very short)
    - Project: P2 · API + tests + quality gate | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Screenshots: class for valid case, clear errors for the 2 others
- [x]  **3.3** A3: pytest tests (API responds, valid works, invalid refused, model min score) + pytest.ini pythonpath
    - Project: P2 · API + tests + quality gate | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: All tests green (screenshot)
- [x]  **3.4** A4: config.yaml (min F1, min test size) + check_quality.py; justify threshold with noise margin
    - Project: P2 · API + tests + quality gate | Priority: High | Estimate: 0.75 h | Status: Not started
    - Done when: Real model accepted, fake model rejected, one-sentence justification
- [x]  **3.5** B5: Dockerfile (slim base, tensorflow-cpu, pinned versions) + .dockerignore; docker build; note image size
    - Project: P3 · Docker container | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: Image built, size noted
- [x]  **3.6** B6: docker run and redo the 3 tests of A2
    - Project: P3 · Docker container | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Same answers as local (screenshot)
- [x]  **3.7** Commit and push; end-of-day notes
    - Project: P2 · API + tests + quality gate | Priority: Low | Estimate: 0.25 h | Status: Not started
    - Done when: Push done
- [x]  **3.8** Buffer
    - Project: Buffer | Priority: Low | Estimate: 0.5 h | Status: Not started

## 📅 Day 4

**Goal:** GitHub Actions + Azure: green CI, image in registry, public URL (heaviest day)

**Total:** 6.0 h | **Date:** (to fill)

- [ ]  **4.1** C7: workflow in .github/workflows/ - job test (install, quality gate, pytest) then job image (needs: test; build + check API starts)
    - Project: P4 · GitHub Actions (CI) | Priority: High | Estimate: 1.25 h | Status: Not started
    - Done when: 2 green jobs in Actions tab (screenshot)
- [ ]  **4.2** C8: raise threshold above reachable, push (test red, image not started); restore threshold, all green
    - Project: P4 · GitHub Actions (CI) | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Red chain then green chain (screenshots)
- [ ]  **4.3** D9: create Azure Container Registry (Basic, unique lowercase name, no dashes); enable admin user
    - Project: P5 · Azure deployment | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Registry address, username, password
- [ ]  **4.4** D10a: store the 3 values as GitHub secrets (never in code or chat)
    - Project: P5 · Azure deployment | Priority: High | Estimate: 0.25 h | Status: Not started
    - Done when: 3 secrets visible, values hidden
- [ ]  **4.5** D10b: add job publier (needs: image), docker/login-action, push image tagged with github.sha
    - Project: P4 · GitHub Actions (CI) | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: 3 green jobs + image with commit id in registry
- [ ]  **4.6** D11: create Container App from the image (secret auth, 1 CPU, 2 GB, external ingress, target port)
    - Project: P5 · Azure deployment | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: Public URL available
- [ ]  **4.7** D12: test /health and /predict (3 cases) on public URL; show the trainer
    - Project: P5 · Azure deployment | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Same answers as local + trainer OK
- [ ]  **4.8** Buffer (permissions, MANIFEST_UNKNOWN, restart loops)
    - Project: Buffer | Priority: Low | Estimate: 1 h | Status: Not started

## 📅 Day 5

**Goal:** Release, rollback, cleanup, deliverables

**Total:** 6.25 h | **Date:** (to fill)

- [ ]  **5.1** E13: add /hello route, push, 3 green jobs, deploy new image by hand (az containerapp update) with commit id
    - Project: P6 · Release, rollback, cleanup | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: /hello visible, new commit id in /health
- [ ]  **5.2** E14: rollback - redeploy the previous commit
    - Project: P6 · Release, rollback, cleanup | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: /hello gone, old commit id back in /health
- [ ]  **5.3** F15a: note estimated cost of what was created
    - Project: P6 · Release, rollback, cleanup | Priority: Medium | Estimate: 0.25 h | Status: Not started
    - Done when: Cost written down
- [ ]  **5.4** F15b: delete Container App, its environment and the registry (never the shared resource group)
    - Project: P6 · Release, rollback, cleanup | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Screenshot: resources no longer exist
- [ ]  **5.5** Write README.md (how to run notebook, API, tests, quality gate, Docker, workflow)
    - Project: P7 · Deliverables | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: A classmate could follow it
- [ ]  **5.6** Write the one-page sheet in your own words (model journey, threshold, manual deploy, automation needs, limits)
    - Project: P7 · Deliverables | Priority: High | Estimate: 1 h | Status: Not started
    - Done when: One page
- [ ]  **5.7** Gather all proofs
    - Project: P7 · Deliverables | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Proof list complete
- [ ]  **5.8** Final check of repo against deliverables; push
    - Project: P7 · Deliverables | Priority: High | Estimate: 0.5 h | Status: Not started
    - Done when: Everything present
- [ ]  **5.9** Buffer
    - Project: Buffer | Priority: Low | Estimate: 1 h | Status: Not started

## 📦 Deliverables checklist

- [ ]  GitHub repo: notebook, model/, API, tests, thresholds file, quality-gate script, dependency files, Dockerfile, .dockerignore, workflow, README.md
- [x]  Proof: tests in local
- [x]  Proof: container in local
- [ ]  Proof: green chain
- [ ]  Proof: red chain (impossible threshold)
- [ ]  Proof: public URL
- [ ]  Proof: /health with commit
- [ ]  Proof: /hello added then removed
- [ ]  Proof: resources deleted
- [ ]  One-page sheet in your own words

## ⚠️ Risks

- **KerasTuner errors on Windows**: disable tracking files; install tensorboard
- **Suspiciously high score**: re-check duplicates and TF-IDF fitted on train only
- **Contributor role on Azure**: use registry admin user; deploy by hand
- **Container restarts in a loop**: give 2 GB memory; check az containerapp logs

## 🧭 Daily routine

1. After each task: attach the proof, tick the checkbox.
2. Evening: 10 min review, move unfinished tasks to the next day, commit and push.