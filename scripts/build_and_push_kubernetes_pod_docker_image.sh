# To authenticate:
# cat $keyfile.json | docker login -u _json_key --password-stdin https://eu.gcr.io

bash $(pwd)/scripts/create_kubernetes_pod_docker_image.sh

docker push eu.gcr.io/datapipeline-295515/mapaction-cloudcomposer-kubernetes-image:latest
