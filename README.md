# blue_green_deployment_kind_cluster

These usecases are tried out in ubuntu-20.04 LTS machine, which is running as standalone VM in GCP cloud

## Pre-requisites
* Install kind in ubuntu machine
  ```
  # For AMD64 / x86_64
  [ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
  # For ARM64
  [ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-arm64
  chmod +x ./kind
  sudo mv ./kind /usr/local/bin/kind
  ```
* Install docker in ubuntu machine
```
sudo apt-get update
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER
docker --version
docker info
```
* Install kubectl in ubuntu machine
```
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client
```

## Usecase-1 
* create 5 node k8s cluster using kind
* create 2 separate namespaces namely 'blue' and 'green'
* Deploy web-apps in both namespaces

## Solution
* Create 5 node k8s cluster using kind.
```
kubectl cluster-info --context kind-kind
cat <<EOF > kind-config.yaml
   kind: Cluster
   apiVersion: kind.x-k8s.io/v1alpha4
   nodes:
       - role: control-plane
       - role: worker
       - role: worker
       - role: worker
       - role: worker
     EOF
kind create cluster --config kind-config.yaml #wait till cluster creation completes
kubectl get nodes
```
Inside `k8s-files` folder of this repo , you will get deploy,svc files for blue and green objects.
```
cd k8s-files
kubectl apply -f blue-deploy.yaml
kubectl apply -f blue-service.yaml
kubectl apply -f green-deploy.yaml
kubectl apply -f green-service.yaml
```
Once above apply completes, you should be able to see 'blue-app' deploy and 'blue-service' service in blue namespace  & 'green-app' deploy and 'green-service' service in green namespace.
```
kubectl get po -n blue
kubectl get po -n green
kubectl get deploy -n blue
kubectl get deploy -n green
kubectl get svc -n blue
kubectl get svc -n green
```

## Usecase-2
* create a test-user in machine
* Give only 'service' access to test-user, so that he can access only svc in 'green' namespace
* test changes and confirm


## Solution
* create role and rolebinding for `test-user` : this is already created and present in `k8s-files` repo
```
kubectl apply -f user-role.yaml
kubectl apply -f user-rolebinding.yaml
```
* To test these changes, we can create a temporary user or use an existing test user account to verify the access permissions. Here's how you can do it:







