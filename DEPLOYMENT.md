# 🚀 Cloud Run Deployment Guide

Deploy your Trading Analytics Dashboard to Google Cloud Run with automatic GitHub integration.

---

## ⚡ Quick Deploy (10 minutes)

### Prerequisites

- Google Cloud account (free tier available)
- GitHub repository with your code
- gcloud CLI installed: https://cloud.google.com/sdk/docs/install

---

## 📋 Step-by-Step Deployment

### 1. Setup Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Create project (or use existing)
gcloud projects create trading-analytics-prod

# Set as active project
gcloud config set project trading-analytics-prod

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### 2. Create Secrets

**Upload Google Sheets credentials:**
```bash
cd backend
gcloud secrets create google-credentials --data-file=credentials.json
```

**Add environment variables to Cloud Run:**

Go to [Cloud Run Console](https://console.cloud.google.com/run) → Your Service → Edit & Deploy New Revision → Variables & Secrets

Add these **Environment Variables**:
```
OPENAI_API_KEY=sk-your-openai-key
GOOGLE_SHEET_IDS=1VRU2WWKW5vtaGTNZjaxIMBngsO1a2IvzVixN6MRTTCQ
GOOGLE_SHEET_GID=1186874097
```

Add this **Secret**:
- Name: `GOOGLE_CREDENTIALS_JSON`
- Secret: `google-credentials`
- Version: `latest`

### 3. Connect GitHub for Auto-Deploy

1. Go to [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers)
2. Click "Connect Repository"
3. Select "GitHub" → Authorize
4. Choose your repository
5. Create trigger:
   - **Name**: `deploy-on-push`
   - **Event**: Push to branch
   - **Branch**: `^main$`
   - **Configuration**: Cloud Build configuration file
   - **Location**: `cloudbuild.yaml`
6. Click "Create"

### 4. Push to Deploy

```bash
git add .
git commit -m "Deploy to Cloud Run"
git push origin main
```

**That's it!** Cloud Build automatically:
- Builds Docker image
- Deploys to Cloud Run
- Provides live URL

---

## 🌐 Get Your Live URL

```bash
gcloud run services describe trading-analytics-dashboard \
  --region=europe-west2 \
  --format='value(status.url)'
```

Example: `https://trading-analytics-dashboard-823333525467.europe-west2.run.app`

---

## 🔧 Configuration

### Environment Variables (Set in Cloud Run Console)

| Variable | Value | Required |
|----------|-------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ Yes |
| `GOOGLE_SHEET_IDS` | Your sheet ID | ✅ Yes |
| `GOOGLE_SHEET_GID` | Worksheet GID | Optional |
| `PORT` | Auto-set by Cloud Run | No |

### Secrets (Set in Secret Manager)

| Secret | Value | Mounted As |
|--------|-------|------------|
| `google-credentials` | credentials.json content | `GOOGLE_CREDENTIALS_JSON` |

---

## 📊 Monitoring

### View Logs

```bash
gcloud run services logs read trading-analytics-dashboard \
  --region=europe-west2 \
  --limit=50
```

Or visit: [Cloud Run Logs](https://console.cloud.google.com/run/detail/europe-west2/trading-analytics-dashboard/logs)

### Check Build Status

[Cloud Build History](https://console.cloud.google.com/cloud-build/builds)

---

## 💰 Cost Estimate

**Cloud Run (Free Tier):**
- 2 million requests/month free
- 360,000 GB-seconds memory free
- 180,000 vCPU-seconds free

**Expected monthly cost**: **$0 - $5** for demo/small usage

[Cloud Run Pricing Calculator](https://cloud.google.com/run/pricing)

---

## 🔄 Update Deployment

Simply push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Auto-deploys in 3-5 minutes! ✨

---

## 🔙 Rollback to Previous Version

```bash
# List revisions
gcloud run revisions list --service=trading-analytics-dashboard --region=europe-west2

# Rollback to specific revision
gcloud run services update-traffic trading-analytics-dashboard \
  --region=europe-west2 \
  --to-revisions=REVISION_NAME=100
```

---

## 🐛 Troubleshooting

### Build Fails

**Check build logs:**
```bash
gcloud builds list --limit=5
gcloud builds log BUILD_ID
```

**Common issues:**
- Missing `cloudbuild.yaml` → Ensure it's in root
- Wrong region → Check `cloudbuild.yaml` uses `europe-west2`
- Service account permissions → Grant Cloud Build access to secrets

### "Authentication failed" in Logs

1. Go to [Secret Manager](https://console.cloud.google.com/security/secret-manager)
2. Click `google-credentials` → View secret
3. Verify it's the **full JSON** (not file path)
4. If wrong, recreate secret with JSON content

### "No data synced yet"

1. Check environment variables are set in Cloud Run
2. Verify Google Sheet ID is correct
3. Ensure service account email has Sheet access
4. Click "Sync Data" button in dashboard

### Connection Issues

- Service running? Check Cloud Run console
- Correct URL? Get it with `gcloud run services describe`
- Allow unauthenticated? Check service permissions

---

## 🔐 Security Best Practices

### Enable IAM Authentication (Optional)

```bash
gcloud run services update trading-analytics-dashboard \
  --region=europe-west2 \
  --no-allow-unauthenticated
```

Then use: `gcloud auth print-identity-token` for requests

### Use Secret Manager (Already Configured)

✅ Credentials stored in Secret Manager
✅ Never commit `.env` or `credentials.json`
✅ Secrets injected at runtime

---

## 🌍 Custom Domain (Optional)

1. Go to [Cloud Run Domain Mappings](https://console.cloud.google.com/run/domains)
2. Click "Add Mapping"
3. Select service: `trading-analytics-dashboard`
4. Enter your domain: `trading.yourdomain.com`
5. Update DNS records as instructed
6. SSL certificate auto-provisioned!

---

## 🔗 Useful Links

- [Cloud Run Console](https://console.cloud.google.com/run)
- [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers)
- [Secret Manager](https://console.cloud.google.com/security/secret-manager)
- [Build Logs](https://console.cloud.google.com/cloud-build/builds)
- [IAM & Permissions](https://console.cloud.google.com/iam-admin/iam)

---

## 📞 Need Help?

1. Check [Cloud Run documentation](https://cloud.google.com/run/docs)
2. View build logs for errors
3. Check service logs for runtime issues
4. Verify all secrets and env vars are set

---

**Your dashboard is now live and auto-deploys on every push! 🎉**
