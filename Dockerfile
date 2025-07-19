################ 1. Build React UI ################
FROM node:20-alpine AS ui-build
WORKDIR /ui

# install UI deps
COPY frontend/package*.json ./
RUN npm ci

# build
COPY frontend .
RUN npm run build      # outputs to /ui/dist

################ 2. Build Python API ##############
FROM python:3.12-slim
WORKDIR /app

# ---- Python deps ----
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Backend code ----
COPY backend/app ./app

# ---- Copy built UI ----
# main.py lives in /app/app, and mounts "../frontend/dist" → /app/frontend/dist
COPY --from=ui-build /ui/dist ./frontend/dist

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
