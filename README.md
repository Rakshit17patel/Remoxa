# Topics of Distributed Computing Research Project - Team Alliance


## Research Topic: 

Efficient Deep Learning Model Deployment in Distributed Environments with Kubernetes

## Team Members:
Azad Patel, Abhyush Rajak, Rakshit Patel, Smit Rajeshkumar Patel

## Introduction

This application allows users to remove the background from images using the **U²-Net** deep learning model. The project is built with **Flask** for the web interface and API, **Docker** for containerization, and **Kubernetes** with **Minikube** for orchestration and deployment.

This README provides a comprehensive guide to setting up, running, and deploying the application, including simulations of various Kubernetes features such as auto-scaling and fault tolerance.

---
## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
   - [Clone the Repository](#clone-the-repository)
   - [Download the U²-Net Model](#download-the-u²-net-model)
4. [Running the Application Locally](#running-the-application-locally)
5. [Dockerizing the Application](#dockerizing-the-application)
   - [Building the Docker Image](#building-the-docker-image)
   - [Running the Docker Container Locally](#running-the-docker-container-locally)
6. [Pushing the Docker Image to Docker Hub](#pushing-the-docker-image-to-docker-hub)
7. [Deploying to Kubernetes with Minikube](#deploying-to-kubernetes-with-minikube)
   - [Starting Minikube](#starting-minikube)
   - [Creating Kubernetes Deployment and Service](#creating-kubernetes-deployment-and-service)
   - [Applying the Configuration](#applying-the-configuration)
   - [Accessing the Application](#accessing-the-application)
8. [Simulating Kubernetes Benefits](#simulating-kubernetes-benefits)
   - [Horizontal Scaling](#horizontal-scaling)
   - [Auto-scaling Based on CPU Utilization](#auto-scaling-based-on-cpu-utilization)
   - [Fault Tolerance](#fault-tolerance)
   - [Node Failure Handling](#node-failure-handling)
   - [Resource Efficiency](#resource-efficiency)
   - [Resource Usage Monitoring](#resource-usage-monitoring)
   - [Resource Contention](#resource-contention)
9. [Conclusion](#conclusion)
10. [References](#references)

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.7 or higher**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Hub Account**: [Sign Up for Docker Hub](https://hub.docker.com/signup)
- **Minikube**: [Install Minikube](https://minikube.sigs.k8s.io/docs/start/)
- **kubectl**: [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- **Optional**: Virtual environment tool like `venv` or `conda`

---

## Project Structure

```
├── app.py
├── Dockerfile
├── requirements.txt
├── k8s
│   └── deployment.yaml
│   └── service.yaml
├── LoadTesting
│   └── load_test.py
├── u2net.pth
└── README.md
```

- **app.py**: The main Flask application file.
- **Dockerfile**: Instructions to build the Docker image.
- **requirements.txt**: Python dependencies.
- **load_test.py**: Script to send concurrent request at once.
- **u2net.pth**: Pre-trained U²-Net model weights (to be downloaded).
- **deployment.yaml**: Kubernetes Deployment configuration.
- **service.yaml**: Kubernetes Service configuration.
- **README.md**: Project documentation.

---

## Installation

### Clone the Repository

Clone this repository to your local machine using:

```bash
git clone https://github.com/smit-in/Remoxa-TDC-Research-Project.git
cd remoxa
```

### Download the U²-Net Model

Download the pre-trained U²-Net model weights and place them in the project directory.

1. **Download Link**: [U²-Net (176.6 MB)](https://drive.google.com/file/d/1gl4qutT0wluuKLIv1mpbP7wj5ZsErhjw/)

2. **Place the File**: Ensure the file is named `u2net.pth` and located in the project root.

---

## Running the Application Locally

1. **Create a Virtual Environment (Optional but Recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Run the Flask Application**:

   ```bash
   python app.py
   ```

4. **Access the Application**:

   Open your browser and navigate to `http://localhost:8000` to use the application.

---

## Dockerizing the Application

### Building the Docker Image

1. **Build the Docker Image**:

   ```bash
   docker build -t your_dockerhub_username/remoxa:latest .
   ```

   Replace `your_dockerhub_username` with your actual Docker Hub username.

2. **Verify the Image**:

   ```bash
   docker images
   ```

   You should see your image listed.

### Running the Docker Container Locally

1. **Run the Container**:

   ```bash
   docker run -d -p 8000:8000 --name remoxa-app your_dockerhub_username/remoxa:latest
   ```

2. **Verify it's Running**:

   ```bash
   docker ps
   ```

3. **Access the Application**:

   Open your browser and navigate to `http://localhost:8000`.

4. **Stop and Remove the Container**:

   ```bash
   docker stop remoxa-app
   docker rm remoxa-app
   ```

---

## Pushing the Docker Image to Docker Hub

1. **Login to Docker Hub**:

   ```bash
   docker login
   ```

2. **Tag the Image (if necessary)**:

   ```bash
   docker tag your_dockerhub_username/remoxa:latest your_dockerhub_username/remoxa:latest
   ```

3. **Push the Image**:

   ```bash
   docker push your_dockerhub_username/remoxa:latest
   ```

4. **Verify on Docker Hub**:

   - Log in to your Docker Hub account and check the repository to ensure the image is uploaded.

---

## Deploying to Kubernetes with Minikube

### Starting Minikube

1. **Start Minikube**:

   ```bash
   minikube start --cpus=4 --memory=8192
   ```

2. **Verify Minikube Status**:

   ```bash
   kubectl get nodes
   ```

### Creating Kubernetes Deployment and Service

1. **Create `deployment.yaml`**:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: remoxa-deployment
     labels:
       app: remoxa
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: remoxa
     template:
       metadata:
         labels:
           app: remoxa
       spec:
         containers:
         - name: remoxa-container
           image: your_dockerhub_username/remoxa:latest
           ports:
           - containerPort: 8000
           resources:
             requests:
               memory: "1Gi"
               cpu: "500m"
             limits:
               memory: "2Gi"
               cpu: "1"
           livenessProbe:
             httpGet:
               path: /
               port: 8000
             initialDelaySeconds: 30
             periodSeconds: 10
           readinessProbe:
             httpGet:
               path: /
               port: 8000
             initialDelaySeconds: 15
             periodSeconds: 10
   ```

2. **Create `service.yaml`**:

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: remoxa-service
   spec:
     type: NodePort
     selector:
       app: remoxa
     ports:
       - protocol: TCP
         port: 8000
         targetPort: 8000
         nodePort: 30000
   ```

### Applying the Configuration

1. **Apply Deployment**:

   ```bash
   kubectl apply -f deployment.yaml
   ```

2. **Apply Service**:

   ```bash
   kubectl apply -f service.yaml
   ```

3. **Verify Resources**:

   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl get services
   ```

### Accessing the Application

1. **Get the Minikube IP**:

   ```bash
   minikube ip
   ```

   Let's say the IP is `192.168.49.2`.

2. **Access the Application**:

   Open your browser and navigate to `http://192.168.49.2:30000`.

   Alternatively, you can use:

   ```bash
   minikube service remoxa-service --url
   ```

   This command provides the URL to access the application.

---

## Simulating Kubernetes Benefits

### Horizontal Scaling

1. **Scale the Deployment**:

   ```bash
   kubectl scale deployment remoxa-deployment --replicas=4
   ```

2. **Verify Scaling**:

   ```bash
   kubectl get pods
   ```

   You should see 4 pods running.

### Auto-scaling Based on CPU Utilization

1. **Enable Metrics Server**:

   ```bash
   minikube addons enable metrics-server
   ```

2. **Create Horizontal Pod Autoscaler (HPA)**:

   ```bash
   kubectl autoscale deployment remoxa-deployment --cpu-percent=50 --min=2 --max=10
   ```

3. **Generate CPU Load**:

   Since generating CPU load requires sending multiple requests, you can use a Python script:

   **Create `load_test.py`**:

   ```python
    import requests
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time
    
    URL = "URL_HERE"
    IMAGE_PATH = "./PATH_HERE"
    NUM_REQUESTS = 20
    CONCURRENT_WORKERS = 2
    
    def send_request(session, url, image_path, retry=3):
        with open(image_path, 'rb') as img:
            files = {'image': img}
            for attempt in range(retry):
                try:
                    response = session.post(url, files=files, timeout=10)
                    return response.status_code
                except requests.exceptions.RequestException as e:
                    print(f"Attempt {attempt+1}: Request failed: {e}")
                    time.sleep(1)  # Wait before retrying
        return None

    def main():
        start_time = time.time()
        success = 0
        failures = 0
        with ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
            with requests.Session() as session:
                futures = [
                    executor.submit(send_request, session, URL, IMAGE_PATH)
                    for _ in range(NUM_REQUESTS)
                ]
                for future in as_completed(futures):
                    status = future.result()
                    if status and 200 <= status < 300:
                        print(f"Request completed with status code: {status}")
                        success += 1
                    else:
                        print(f"Request failed with status code: {status}")
                        failures += 1
        end_time = time.time()
        print(f"Completed {NUM_REQUESTS} requests in {end_time - start_time:.2f} seconds.")
        print(f"Successful requests: {success}")
        print(f"Failed requests: {failures}")
    
    if __name__ == "__main__":
        main()
   ```

   - **Note**: Ensure you have `test_image.jpg` in your directory and update the `IMAGE_PATH` accordingly.

4. **Run the Load Test**:

   ```bash
   python load_test.py
   ```

5. **Monitor HPA**:

   ```bash
   kubectl get hpa --watch
   ```

   You should see the number of replicas increase based on CPU utilization.

### Fault Tolerance

1. **Simulate Pod Failure**:

   ```bash
   kubectl delete pod <pod_name>
   ```

   Replace `<pod_name>` with one of your pod names.

2. **Observe Recovery**:

   ```bash
   kubectl get pods
   ```

   Kubernetes will automatically create a new pod to maintain the desired state.

### Node Failure Handling

1. **Simulate Node Failure**:

   Since Minikube is single-node, you can simulate by stopping Minikube:

   ```bash
   minikube stop
   ```

2. **Observe Impact**:

   The application becomes unavailable.

3. **Start Minikube Again**:

   ```bash
   minikube start
   ```

4. **Verify Pods**:

   ```bash
   kubectl get pods
   ```

   Pods will be recreated as Kubernetes restores the desired state.

### Resource Efficiency

1. **Review Resource Requests and Limits**:

   Ensure your `deployment.yaml` has appropriate resource definitions.

2. **Monitor Resource Usage**:

   ```bash
   kubectl top pods
   ```

3. **Adjust Resources as Needed**:

   Update `deployment.yaml` and reapply:

   ```bash
   kubectl apply -f deployment.yaml
   ```

### Resource Usage Monitoring

1. **Access Kubernetes Dashboard**:

   ```bash
   minikube dashboard
   ```

2. **Use `kubectl top`**:

   ```bash
   kubectl top nodes
   kubectl top pods
   ```

### Resource Contention

1. **Deploy a Resource-Intensive Pod**:

   ```bash
   kubectl run stress --image=alpine --restart=Never -- sleep 3600
   kubectl exec -it stress -- sh
   apk add --no-cache stress-ng
   stress-ng --cpu 4 --timeout 300
   ```

2. **Monitor Impact**:

   ```bash
   kubectl top pods
   ```

3. **Implement Resource Quotas**:

   **Create `quota.yaml`**:

   ```yaml
   apiVersion: v1
   kind: ResourceQuota
   metadata:
     name: remoxa-quota
   spec:
     hard:
       requests.cpu: "4"
       requests.memory: "8Gi"
       limits.cpu: "8"
       limits.memory: "16Gi"
   ```

4. **Apply the Quota**:

   ```bash
   kubectl apply -f quota.yaml
   ```

---

## Conclusion

Congratulations! You've successfully:

- Set up and run the Image Background Remover application locally.
- Dockerized the application and pushed the image to Docker Hub.
- Deployed the application to a Kubernetes cluster using Minikube.
- Simulated various Kubernetes features to demonstrate benefits like auto-scaling, fault tolerance, and resource management.

This project showcases the power of combining Flask, Docker, and Kubernetes to build scalable and reliable applications.

---

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/start/)
- [U²-Net Paper](https://arxiv.org/abs/2005.09007)
- [U²-Net Repository](https://github.com/xuebinqin/U-2-Net)

---

## Additional Notes

- **Cleaning Up**:

  To delete all resources created during this project:

  ```bash
  kubectl delete deployment remoxa-deployment
  kubectl delete service remoxa-service
  kubectl delete hpa remoxa-deployment
  kubectl delete resourcequota remoxa-quota
  ```

- **Troubleshooting**:

  - If you encounter issues with `kubectl top`, ensure Metrics Server is running.
  - Use `kubectl describe pod <pod_name>` to get detailed information about pod issues.

- **Extending the Project**:

  - Integrate authentication for secure access.
  - Deploy the application to a cloud-based Kubernetes service like GKE, EKS, or AKS.
  - Implement continuous integration and deployment (CI/CD) pipelines.

---