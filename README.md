


# Tracking kubernetes configmaps with kosli


1. download configmaps
2. filter out generated fields in configmaps
3. snapshot 

## 1. Download configmaps

```bash
gcloud container clusters get-credentials autopilot-cluster-1 --region us-central1 --project test-kubernetes-environment

# Download Configmaps
./download-configmaps.sh -o snapdir gamestore

# Download CRDs
./download-configmaps.sh -o snapdir -c gamestore
```

## 2. Filter configmaps

```bash
source env/bin/activate


```