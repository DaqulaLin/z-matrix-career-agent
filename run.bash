# 官方推荐配置：显式注入环境变量，防止 ADK 初始化迷路
gcloud run deploy compass-job-api \
  --source . \
  --region asia-northeast1 \
  --memory 2Gi \
  --allow-unauthenticated \
  --timeout 300 \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=spatial-cargo-484310-t2,GOOGLE_CLOUD_LOCATION=asia-northeast1,GOOGLE_GENAI_USE_VERTEXAI=True"