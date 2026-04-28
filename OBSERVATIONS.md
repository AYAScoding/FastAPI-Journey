> **1-** What is the difference between a Pod and a Deployment? Why would you use a Deployment instead of a bare Pod?

- A Pod is the smallest unit in Kubernetes that runs your container.
- A Deployment is like a manager for Pods.
- Why use a Deployment? If a bare Pod dies, it stays dead. A Deployment will notice the Pod is gone and automatically start a new one to keep your app running.

> **2-** Why is a ConfigMap used for the MongoDB URL instead of hardcoding it in the Deployment YAML?

- Flexibility: It separates the configuration (like the database URL) from the application settings.
- Efficiency: If the database URL changes, you only update the ConfigMap instead of editing every single Deployment file.

> **3-** What happened to the original Pod when you scaled the WebApp to 3 replicas? Did it get replaced, or were new Pods added alongside it?

- When I changed the replicas to 3, the original Pod stayed running and two others were added.

> **4-** What would happen to the application if the MongoDB Pod crashed? How would Kubernetes respond?

- Kubernetes would see the Pod has failed and immediately try to pull a new image and restart a fresh MongoDB Pod to fix itself.
