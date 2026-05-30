---
avatar: avatar-tech-apigee-azure
law: ENG-5.2
title: "CI/CD Pipeline Law"
codebase_source: "AAInternal/apigeeDocs"
---

# ENG-5.2 — CI/CD Pipeline Law: Apigee + Azure

**No manual deployments to any environment. All pipelines created by Runway. Prod deploys require passing tests + human approval + ServiceNow CR.**

---

## AA Runway Provisioning (Standard Starting Point)

All Apigee proxy repos at AA are scaffolded by **Runway** (`https://developer.aa.com/apigee/create`):

1. Select **Micro Gateway** → Runway creates GitHub repo with pre-configured Actions workflows
2. Initial commit triggers automatic **dev** deployment
3. Promote via **Runway MANAGE API** → auto-raises PR against `master` for prod

**Never create an Apigee proxy repo manually** — Runway templates include the correct org names (`aa-dev` / `aa-test` / `aa-stage` / `aa-prod`), pipeline secrets, and environment protection rules.

---

## Apigee — GitHub Actions Pipeline (Runway Template Pattern)

```yaml
# .github/workflows/apigee-deploy.yml (Runway-scaffolded)
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test  # proxy unit tests MUST pass before any deploy

  deploy-nonprod:
    needs: [test]
    environment: nonprod  # maps to aa-dev / aa-test / aa-stage
    steps:
      - run: |
          apigeetool deployproxy \
            --token ${{ secrets.APIGEE_TOKEN }} \
            -o ${{ vars.APIGEE_ORG }} \
            -e ${{ vars.APIGEE_ENV }} \
            -n ${{ vars.PROXY_NAME }} \
            -d ./apiproxy

  deploy-prod:
    needs: [deploy-nonprod]
    environment: production  # GitHub environment protection: requires human approval
    # Prod also requires ServiceNow Change Request (Team Name must be in proxy config)
    steps:
      - run: apigeetool deployproxy ... -o aa-prod -e prod ...
```

**Promotion via Runway MANAGE API:**
- Select repo → Update API Endpoints → select PROD
- Runway commits to `nonprod` branch and **auto-raises PR against `master`**
- Close any open PRs before pushing to prod
- Merge triggers pipeline → deploys to `aa-prod`

---

## Terraform — Plan in PR, Apply with Approval

```yaml
jobs:
  plan:
    steps:
      - run: terraform init -backend-config="..." && terraform plan -out=tfplan
      - uses: actions/upload-artifact@v4
        with: { name: tfplan, path: tfplan }

  apply:
    needs: [plan]
    environment: production  # human approval gate — never terraform apply from local
    steps:
      - uses: actions/download-artifact@v4
        with: { name: tfplan }
      - run: terraform apply tfplan
```

---

## Azure App Service Deployment (Runway Automated Template)

Use the Runway App Service template for Microgateway on Azure App Service:
`https://developer.aa.com/create/templates/default/azureappservice-microgateway`

Required pre-requisites:
- HashiCorp Vault namespace for `EDGEMICRO_KEY` / `EDGEMICRO_SECRET` storage
- Azure storage account for Terraform state
- Azure service principal with Linux plan `P1V2` (prod), `B1` (lower environments)
- Request `EDGEMICRO_KEY` + `EDGEMICRO_SECRET` via DataMovement team issue

---

## Acceptance Criteria
- [ ] Proxy CI runs `npm test` — pipeline fails on test failure
- [ ] All deploys use Runway-scaffolded GitHub Actions — no manual UI bundle uploads
- [ ] `terraform apply` to prod blocked without human approval (GitHub environment protection)
- [ ] Prod Apigee deployments have ServiceNow Team Name in proxy configuration
- [ ] Functions deploy to prod only after staging deploy succeeds + contract tests pass
