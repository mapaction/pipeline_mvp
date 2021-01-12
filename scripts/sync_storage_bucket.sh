export BUCKET=europe-west2-mapaction-deve-542e8027-bucket

gsutil -m cp -r $(pwd)/dags gs://$BUCKET
gsutil -m cp -r $(pwd)/plugins gs://$BUCKET
