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

## Usecase-2
* create a test-user in machine
* Give only 'service' access to test-user, so that he can access only svc in 'green' namespace
* test changes and confirm

## Solution - 1
* Create 5 node k8s cluster using kind.
```

