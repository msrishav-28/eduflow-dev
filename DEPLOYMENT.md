# Deployment Guide

Complete deployment guide for all platforms and environments.

---

## 🎯 Deployment Options

| Option | Best For | Difficulty | Cost |
|--------|----------|------------|------|
| **Vercel** | Quick deployment, serverless | ⭐ Easy | Free tier available |
| **Docker** | Full control, any cloud | ⭐⭐ Medium | Varies |
| **Cloud Providers** | Enterprise, scalability | ⭐⭐⭐ Advanced | Pay as you go |

---

## 🚀 Vercel Deployment (Recommended)

Deploy both frontend and backend together on Vercel.

### Prerequisites
- GitHub account
- Vercel account (free)
- MongoDB Atlas (free tier) for V3 features

### Step-by-Step

#### 1. Prepare MongoDB Atlas

```bash
# 1. Go to https://www.mongodb.com/cloud/atlas
# 2. Create free cluster
# 3. Create database user
# 4. Whitelist IP: 0.0.0.0/0 (allow from anywhere)
# 5. Get connection string:
#    mongodb+srv://username:password@cluster.mongodb.net/eduflow
```

#### 2. Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Save this for environment variables
```

#### 3. Push to GitHub

```bash
git add .
git commit -m "Production ready"
git push origin main
```

#### 4. Deploy to Vercel

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Vercel auto-detects configuration

#### 5. Add Environment Variables

In Vercel dashboard, add:

```bash
# Required
GEMINI_API_KEY=your-gemini-api-key
SECRET_KEY=your-generated-secret-key

# Required for V3 features
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/eduflow

# Optional
ENV=production
DEBUG=False
CORS_ORIGINS=https://your-app.vercel.app
```

#### 6. Deploy!

Click "Deploy" and wait ~2 minutes.

**Your app will be at:** `https://your-app.vercel.app`

### Vercel Configuration

The `vercel.json` file is already configured:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build"
    },
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {"src": "/api/(.*)", "dest": "/api/index.py"},
    {"src": "/(.*)", "dest": "/index.html"}
  ]
}
```

**Benefits:**
- Frontend and backend on same domain (no CORS issues)
- Automatic HTTPS
- CDN for frontend
- Serverless backend
- Free SSL certificate

---

## 🐳 Docker Deployment

Deploy using Docker containers for full control.

### Local Docker

#### Using Docker Compose (Easiest)

```bash
# 1. Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your values

# 2. Build and start
docker-compose up -d

# 3. Verify
docker-compose ps
docker-compose logs

# 4. Access
# Frontend: http://localhost
# Backend: http://localhost:8000
```

#### Manual Docker Build

**Backend:**
```bash
cd backend
docker build -t eduflow-backend .
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your-key \
  -e MONGO_URL=mongodb://host.docker.internal:27017 \
  eduflow-backend
```

**Frontend:**
```bash
cd frontend
docker build -t eduflow-frontend .
docker run -p 80:80 eduflow-frontend
```

**MongoDB:**
```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

### Cloud Docker Deployment

#### AWS ECS

```bash
# 1. Build and push to ECR
aws ecr create-repository --repository-name eduflow-backend
docker tag eduflow-backend:latest <ecr-url>/eduflow-backend:latest
docker push <ecr-url>/eduflow-backend:latest

# 2. Create ECS task definition
# 3. Create ECS service
# 4. Configure load balancer
```

#### Google Cloud Run

```bash
# 1. Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/eduflow-backend
gcloud builds submit --tag gcr.io/PROJECT_ID/eduflow-frontend

# 2. Deploy
gcloud run deploy eduflow-backend --image gcr.io/PROJECT_ID/eduflow-backend
gcloud run deploy eduflow-frontend --image gcr.io/PROJECT_ID/eduflow-frontend
```

#### Azure Container Instances

```bash
# 1. Push to Azure Container Registry
az acr build --registry myregistry --image eduflow-backend:latest .

# 2. Deploy
az container create \
  --resource-group myResourceGroup \
  --name eduflow-backend \
  --image myregistry.azurecr.io/eduflow-backend:latest \
  --dns-name-label eduflow-backend \
  --ports 8000
```

---

## ☁️ Cloud Providers

### AWS Deployment

**Architecture:**
- **Frontend:** S3 + CloudFront
- **Backend:** ECS Fargate or Lambda
- **Database:** MongoDB Atlas or DocumentDB

**Steps:**

1. **Frontend (S3 + CloudFront):**
```bash
# Build frontend
cd frontend
npm run build

# Upload to S3
aws s3 sync build/ s3://your-bucket-name

# Create CloudFront distribution
aws cloudfront create-distribution --origin-domain-name your-bucket.s3.amazonaws.com
```

2. **Backend (ECS):**
```bash
# Push image to ECR
docker push <ecr-url>/eduflow-backend

# Create ECS service with task definition
```

3. **Database:**
- Use MongoDB Atlas or
- Use AWS DocumentDB (MongoDB-compatible)

**Estimated Costs:**
- S3: ~$1-5/month
- CloudFront: ~$1-10/month
- ECS: ~$30-100/month
- Total: ~$40-120/month

### Google Cloud Platform

**Architecture:**
- **Frontend:** Cloud Storage + Cloud CDN
- **Backend:** Cloud Run
- **Database:** MongoDB Atlas

**Steps:**

1. **Frontend:**
```bash
gsutil -m rsync -r build gs://your-bucket-name
gcloud compute url-maps create eduflow-lb
```

2. **Backend:**
```bash
gcloud run deploy eduflow-backend \
  --image gcr.io/PROJECT_ID/eduflow-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Estimated Costs:**
- Cloud Storage: ~$1-5/month
- Cloud Run: ~$0-20/month (free tier available)
- Total: ~$5-30/month

### Azure

**Architecture:**
- **Frontend:** Azure Static Web Apps
- **Backend:** Azure Container Instances or App Service
- **Database:** MongoDB Atlas

**Steps:**

```bash
# Deploy frontend
az staticwebapp create \
  --name eduflow-frontend \
  --resource-group myResourceGroup

# Deploy backend
az container create \
  --resource-group myResourceGroup \
  --name eduflow-backend \
  --image myregistry.azurecr.io/eduflow-backend
```

---

## 🎛️ Production Configuration

### Environment Variables

**Required:**
```bash
# LLM Provider
GEMINI_API_KEY=your-key

# MongoDB (for V3)
MONGO_URL=mongodb+srv://...

# Security
SECRET_KEY=your-secret-key-32-chars-min

# Environment
ENV=production
DEBUG=False
```

**Security:**
```bash
CORS_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

**Optional:**
```bash
# Alternative LLM providers
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

### SSL/TLS Certificate

**Vercel:** Automatic

**Docker/Cloud:**
```bash
# Using Let's Encrypt with Certbot
certbot certonly --standalone -d yourdomain.com

# Or use cloud provider's certificate manager
# - AWS: Certificate Manager
# - GCP: Managed SSL Certificates
# - Azure: App Service Certificates
```

### Nginx Configuration (for Docker)

Already configured in `frontend/nginx.conf`:
- Security headers
- Gzip compression
- Static asset caching
- React Router support

---

## 📊 Performance Optimization

### Frontend

```bash
# Build with optimization
npm run build

# Analyze bundle size
npm install -g source-map-explorer
source-map-explorer 'build/static/js/*.js'
```

**Optimizations applied:**
- Code splitting
- Tree shaking
- Minification
- Gzip compression

### Backend

**Already optimized:**
- Async/await throughout
- Connection pooling (MongoDB)
- GZip middleware
- Rate limiting

**Additional optimizations:**
```python
# Add in backend/.env
WORKERS=4  # Number of worker processes
```

### Database

**MongoDB Atlas:**
- Auto-scaling
- Automatic backups
- Performance monitoring

**Indexes:**
```javascript
// Create indexes for performance
db.users.createIndex({email: 1}, {unique: true})
db.users.createIndex({points: -1})
db.activities.createIndex({user_id: 1})
db.activities.createIndex({timestamp: -1})
```

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] `SECRET_KEY` is random and secure (32+ chars)
- [ ] `DEBUG=False` in production
- [ ] `CORS_ORIGINS` set to specific domain (not *)
- [ ] SSL/TLS certificate configured
- [ ] MongoDB authentication enabled
- [ ] Firewall configured (only ports 80, 443 open)
- [ ] Rate limiting enabled
- [ ] Environment variables not in code
- [ ] `.env` files in `.gitignore`
- [ ] Security headers configured
- [ ] Regular dependency updates scheduled

---

## 📈 Monitoring & Logging

### Health Checks

**Endpoints:**
- `/health` - Basic liveness check
- `/readiness` - Database connectivity check

**Setup monitoring:**

```bash
# Vercel: Built-in analytics
# - No setup needed

# Docker: External monitoring
# - UptimeRobot (free)
# - Pingdom
# - DataDog
```

### Error Tracking

**Sentry Integration:**

```bash
# Install
pip install sentry-sdk[fastapi]

# Configure in backend/.env
SENTRY_DSN=your-sentry-dsn

# Already integrated in monitoring.py
```

### Logging

**Structured logging configured:**
```python
# Logs include:
# - Timestamp
# - Log level
# - Request ID
# - Message
```

**View logs:**
```bash
# Vercel
vercel logs

# Docker
docker-compose logs -f

# Cloud providers
# - AWS: CloudWatch
# - GCP: Cloud Logging
# - Azure: Application Insights
```

---

## 💾 Backup & Recovery

### Database Backups

**MongoDB Atlas:** Automatic backups included

**Self-hosted MongoDB:**

```bash
# Manual backup
bash scripts/backup-db.sh

# Automated with cron
crontab -e
# Add: 0 2 * * * /path/to/scripts/backup-db.sh
```

**Backup script includes:**
- Automatic compression
- Optional S3 upload
- Retention policy (7 days default)
- Restore instructions

### Disaster Recovery

**Full system backup:**

```bash
# 1. Backup database
mongodump --uri="$MONGO_URL" --out=backup

# 2. Backup environment
cp .env .env.backup

# 3. Backup code
git push origin main

# 4. Document infrastructure
# - DNS settings
# - Environment variables
# - SSL certificates
```

---

## 🔄 CI/CD Pipeline

GitHub Actions workflow already configured in `.github/workflows/ci-cd.yml`

**Pipeline includes:**
- Backend testing
- Frontend testing
- Linting
- Security scanning
- Docker build
- Optional deployment

**Automatic deployment:**

```yaml
# Add to .github/workflows/ci-cd.yml
- name: Deploy to Vercel
  if: github.ref == 'refs/heads/main'
  run: |
    vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

---

## 📊 Scaling

### Horizontal Scaling

**Backend:**
```bash
# Docker Compose: Increase replicas
docker-compose up --scale backend=4

# Kubernetes: Adjust replicas
kubectl scale deployment eduflow-backend --replicas=4
```

**Database:**
- MongoDB Atlas: Auto-scaling
- Add read replicas
- Enable sharding for >1TB data

### Vertical Scaling

**Increase resources:**
```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### Load Balancing

**Nginx load balancer:**
```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location /api/ {
        proxy_pass http://backend;
    }
}
```

---

## 🧪 Testing Deployment

### Pre-deployment Tests

```bash
# Run full test suite
make test

# Security scan
make security-check

# Build test
make docker-build

# Integration test
make docker-up
make health
```

### Post-deployment Tests

```bash
# Health check
curl https://your-app.vercel.app/health

# API test
curl https://your-app.vercel.app/api/

# Frontend test
curl https://your-app.vercel.app/

# Full test
bash scripts/health-check.sh
```

---

## 💰 Cost Estimates

### Vercel (Recommended)

- **Hobby Plan:** $0/month
  - Free tier sufficient for small projects
  - 100GB bandwidth
  - Serverless functions

- **Pro Plan:** $20/month
  - Better for production
  - More resources
  - Team features

### Self-Hosted (Docker)

- **VPS (DigitalOcean, Linode):** $12-48/month
  - 2GB RAM minimum
  - 2 CPU cores
  - 50GB SSD

- **MongoDB Atlas:** $0-57/month
  - Free tier: 512MB storage
  - Paid: $57/month for 10GB

**Total estimated:** $12-105/month

### Cloud Providers

- **AWS:** $40-200/month
- **GCP:** $30-150/month
- **Azure:** $40-180/month

---

## 🎯 Quick Deploy Commands

```bash
# Vercel (one command!)
vercel --prod

# Docker Compose
docker-compose up -d

# Manual Docker
docker build -t eduflow-backend backend/
docker build -t eduflow-frontend frontend/
docker run -d eduflow-backend
docker run -d eduflow-frontend

# Kubernetes
kubectl apply -f k8s/
```

---

## 🆘 Troubleshooting

### "Module not found" on Vercel
**Solution:** Check `api/requirements.txt` has all dependencies

### Frontend can't reach backend
**Solution:** Leave `REACT_APP_BACKEND_URL` empty for same-domain deployment

### MongoDB connection timeout
**Solution:** Whitelist IP 0.0.0.0/0 in MongoDB Atlas

### 502 Bad Gateway
**Solution:** Check backend logs, ensure backend is running

### Memory errors
**Solution:** Increase memory limit in deployment config

---

## ✅ Deployment Checklist

- [ ] Environment variables configured
- [ ] MongoDB accessible
- [ ] SSL certificate obtained
- [ ] Domain DNS configured
- [ ] Health checks passing
- [ ] Monitoring enabled
- [ ] Backups configured
- [ ] CI/CD pipeline working
- [ ] Load testing completed
- [ ] Security scan passed
- [ ] Documentation updated

---

**Your app is ready for production!** 🚀

For installation instructions, see [INSTALLATION.md](INSTALLATION.md)  
For API details, see [API_REFERENCE.md](API_REFERENCE.md)
