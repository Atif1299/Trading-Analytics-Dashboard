# 🚀 Cloud Run Deployment Guide

Complete guide to deploy your Trading Analytics Dashboard to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account** - [Sign up here](https://cloud.google.com/free)
2. **Google Cloud CLI** - [Install gcloud](https://cloud.google.com/sdk/docs/install)
3. **GitHub Repository** - Your code pushed to GitHub

---

## Quick Deployment (5-10 minutes)

### Step 1: Setup Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Create new project (or use existing)
gcloud projects create trading-analytics-prod --name="Trading Analytics"

# Set as active project
gcloud config set project trading-analytics-prod

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### Step 2: Upload Secrets (Credentials & API Keys)

```bash
# Upload Google Sheets credentials
gcloud secrets create google-credentials --data-file=backend/credentials.json

# Create OpenAI API key secret
echo -n "your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-

# Grant Cloud Run access to secrets
gcloud secrets add-iam-policy-binding google-credentials \
    --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor

gcloud secrets add-iam-policy-binding openai-api-key \
    --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor
```

*Replace `PROJECT_NUMBER` with your actual project number (find it with `gcloud projects describe trading-analytics-prod`)*

### Step 3: Deploy to Cloud Run

**Option A: Deploy from Local**

```bash
# Build and deploy in one command
gcloud run deploy trading-analytics \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_SHEET_IDS=YOUR_SHEET_ID,GOOGLE_SHEET_GID=YOUR_GID \
  --set-secrets credentials.json=google-credentials:latest,OPENAI_API_KEY=openai-api-key:latest
```

**Option B: Connect GitHub for Auto-Deploy**

1. Go to [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers)
2. Click "Connect Repository"
3. Select GitHub → Authenticate → Choose your repo
4. Create trigger:
   - **Name:** auto-deploy-main
   - **Branch:** ^main$
   - **Build configuration:** cloudbuild.yaml
5. Push to GitHub → Auto deploys! 🎉

### Step 4: Get Your Live URL

After deployment completes:
```bash
gcloud run services describe trading-analytics --region us-central1 --format 'value(status.url)'
```

You'll get a URL like: `https://trading-analytics-xyz-uc.a.run.app`

---

## Environment Variables Setup

Set these in Cloud Run:

```bash
gcloud run services update trading-analytics \
  --region us-central1 \
  --set-env-vars "\
GOOGLE_SHEET_IDS=1VRU2WWKW5vtaGTNZjaxIMBngsO1a2IvzVixN6MRTTCQ,\
GOOGLE_SHEET_GID=1186874097,\
PORT=8080"
```

---

## Using n8n with Cloud Run

Once deployed, update your n8n HTTP Request node:

- **URL:** `https://your-cloud-run-url.a.run.app/api/chat`
- **Method:** POST
- **Body:** `{"message": "{{ $json.message.text }}"}`

No more localhost issues! 🎉

---

## Local Development (Unchanged!)

Your local setup still works exactly the same:

```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

Nothing changes for local development!

---

## Monitoring & Logs

**View Logs:**
```bash
gcloud run services logs read trading-analytics --region us-central1
```

**Monitor Dashboard:**
[Cloud Run Console](https://console.cloud.google.com/run)

---

## Cost Estimate

**Cloud Run Pricing (Free Tier):**
- ✅ 2 million requests/month free
- ✅ 360,000 GB-seconds memory free
- ✅ 180,000 vCPU-seconds free

**Your estimated cost:** $0-5/month (likely $0 for testing)

---

## Troubleshooting

**Issue: "Permission denied" for secrets**
```bash
# Grant access to service account
gcloud projects add-iam-policy-binding trading-analytics-prod \
  --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor
```

**Issue: Build fails**
```bash
# Check build logs
gcloud builds list --limit=5
gcloud builds log BUILD_ID
```

**Issue: "credentials.json not found"**
- Make sure you uploaded the secret: `gcloud secrets list`
- Verify mounting in Cloud Run console

---

## Update Deployment

**Push to GitHub** (if auto-deploy enabled):
```bash
git add .
git commit -m "Update feature"
git push origin main
# Automatically deploys! ✨
```

**Manual update:**
```bash
gcloud run deploy trading-analytics --source . --region us-central1
```

---

## Rollback to Previous Version

```bash
# List revisions
gcloud run revisions list --service trading-analytics --region us-central1

# Rollback to specific revision
gcloud run services update-traffic trading-analytics \
  --region us-central1 \
  --to-revisions REVISION_NAME=100
```

---

## Need Help?

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Build GitHub Integration](https://cloud.google.com/build/docs/automating-builds/github/build-repos-from-github)
- Check logs: `gcloud run services logs read trading-analytics --region us-central1`

---

**Your app is now production-ready! 🚀**
