# Predict Film Category






**Stages**

<p align="center">
  <img src="resources/pipeline.png" alt="Pipeline diagram" width="900">
</p>



**`PROCEDURE_MISE_EN_PRODUCTION.md`**
- It describes the full path: local checks, `git push`, the three GitHub Actions jobs, a manual `az containerapp update` using the commit ID, and checks on `/health` and `/predict`.
- It has a rollback section and a troubleshooting table with the errors from your brief (`MANIFEST_UNKNOWN`, `roleAssignments/write`, restart loops, `Not Found`).
- The **journal des versions** table has pre-filled lines for the first release (1.0.0), the `/hello` update (1.1.0) and the rollback to 1.0.0, plus an empty row. The numbering rule is explained under the table.

**`FIN_DE_VIE.md`**
- It lists the triggers for retiring the service and what to delete, keep or archive.
- It covers data and compliance notes, and an 8-step checklist with the delete and verify commands. The checklist stops traffic, records the cost, deletes the app, its environment and the registry, and cleans GitHub and your computer. Your shared resource group is never touched.
- It ends with a responsibilities table and a closing sheet to fill in.

