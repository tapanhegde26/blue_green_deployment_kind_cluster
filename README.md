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
```
sudo adduser test-user
su - test-user
# Create a private key
openssl genrsa -out test-user.key 2048

# Create a certificate signing request (CSR)
openssl req -new -key test-user.key -out test-user.csr -subj "/CN=test-user"

# exit from testuser
exit

# Sign the CSR with the Kubernetes CA
openssl x509 -req -in /home/test-user/test-user.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out /home/test-user/test-user.crt -days 365
```
you might face below error
```
 Can't open /etc/kubernetes/pki/ca.crt for reading, No such file or directory
139919017391424:error:02001002:system library:fopen:No such file or directory:../crypto/bio/bss_file.c:69:fopen('/etc/kubernetes/pki/ca.crt','r')
139919017391424:error:2006D080:BIO routines:BIO_new_file:no such file:../crypto/bio/bss_file.c:76:
unable to load certificate
```
The reason for above error is, we are using kind to create k8s cluster and kind uses docker-containers under the hood. So we need different approach to get key and certifcate file

1. Extract the CA Files from the kind Cluster
First, identify the control plane container:

```
docker ps --filter "label=io.x-k8s.kind.cluster" --format "{{.Names}}"
```
This command will list the names of the kind containers. Identify the control plane container name (it will typically be something like kind-control-plane).

Next, copy the CA certificate and key from the kind control plane container to your local machine:


### Replace <control-plane-container-name> with the actual name
```
docker cp <control-plane-container-name>:/etc/kubernetes/pki/ca.crt .
docker cp <control-plane-container-name>:/etc/kubernetes/pki/ca.key .
```
2. Generate Certificates for the Test User
While logged in as your current user (not test-user), generate the necessary certificates:
```
# Create a private key for the test user
openssl genrsa -out test-user.key 2048

# Create a certificate signing request (CSR)
openssl req -new -key test-user.key -out test-user.csr -subj "/CN=test-user"

# Sign the CSR with the Kubernetes CA
openssl x509 -req -in test-user.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out test-user.crt -days 365
```
3. Create a kubeconfig File for the Test User
Generate a kubeconfig file for test-user:
```
# Set credentials for test-user
kubectl config set-credentials test-user --client-certificate=$(pwd)/test-user.crt --client-key=$(pwd)/test-user.key
```

### Set context for test-user
```
kubectl config set-context test-user-context --cluster=kind-kind --namespace=green --user=test-user
```

### Switch to the test-user context
```
kubectl config use-context test-user-context
```
* Test the Permissions
Switch to the test-user context and test the permissions:

```
kubectl config use-context test-user-context
```
```
# Try to list services in the green namespace
kubectl get services -n green
```
```
# Try to list services in the blue namespace (should fail)
kubectl get services -n blue
```

## Closing Notes
You can have your k8s cluster in any of cloud providers like AKS, EKS or GKS, and in real case senario, any of user-management services like Azure active directory or AWS SSO you will be using. In this case your role, rolebinding configuration changes and you will need to handle 'set-context' sections accordingly. 







