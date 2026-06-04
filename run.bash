# Officially recommended configuration: explicitly inject environment variables to prevent ADK initialization issues
gcloud run deploy z-matrix-career-demo \
  --source . \
  --region asia-northeast1 \
  --memory 2Gi \
  --allow-unauthenticated \
  --timeout 300 \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=spatial-cargo-484310-t2,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=True"