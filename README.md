


# Tracking kubernetes configmaps with kosli


# Notes

````
gcloud container clusters get-credentials autopilot-cluster-1 --region us-central1 --project test-kubernetes-environment

# Download Configmaps
./download-configmaps.sh -o snapdir gamestore,monitoring

# Download CRDs
./download-configmaps.sh -o snapdir -c WebStore gamestore
````




````
# Tracking configmaps as artifacts

kosli create flow --use-empty-template k8s-configmaps --description "Tracking kubernetes config maps in Kosli"

kosli begin trail $(git rev-parse HEAD) --flow k8s-configmaps


````