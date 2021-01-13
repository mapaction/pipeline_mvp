# Update cloud composer
# Pass version as single argument

VERSION=$1

sh ./scripts/build_and_push_kubernetes_pod_docker_image.sh $VERSION

echo "$(cat ./plugins/pipeline_plugin/config/config.yaml | sed -E "s/  imageVersion: (.*)/  imageVersion: $VERSION/g")" > ./plugins/pipeline_plugin/config/config.yaml

export BUCKET=europe-west2-mapaction-deve-542e8027-bucket

gsutil -m cp -r $(pwd)/dags gs://$BUCKET
gsutil -m cp -r $(pwd)/plugins gs://$BUCKET
