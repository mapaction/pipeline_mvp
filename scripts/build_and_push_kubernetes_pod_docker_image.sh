# To authenticate:
# cat $keyfile.json | docker login -u _json_key --password-stdin https://eu.gcr.io

VERSION=$1

sudo docker build -t eu.gcr.io/datapipeline-295515/mapaction-cloudcomposer-kubernetes-image:$VERSION \
          -f docker/kubernetesPodOperator.Dockerfile $(pwd)
docker push eu.gcr.io/datapipeline-295515/mapaction-cloudcomposer-kubernetes-image:$VERSION
