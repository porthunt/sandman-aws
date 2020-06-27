echo "Zipping lambda functions..."
zip -r sandman_start.zip src start.py > /dev/null
zip -r sandman_stop.zip src stop.py > /dev/null

echo "Deploying Sandman..."
terraform apply -var-file="deployment.tfvars"
