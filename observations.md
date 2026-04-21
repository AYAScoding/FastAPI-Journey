## 📝 OBSERVATIONS.md

Create an `OBSERVATIONS.md` file inside `docker-lab-2/`. Answer all of the following in your own words:

---

### 1. What is the difference between running a container with `docker run` and deploying a pod with `kubectl run`? Both used the same image — what changed?

When I used `docker run`, the container just ran on my local laptop. But with `kubectl run`, I’m asking the Kubernetes cluster to handle it.

---

### 2. In `kubectl describe pod`, what is the role of the **Scheduler** event? Which control plane component does that correspond to?

The Scheduler event shows the moment Kubernetes decided which node was the best place for the pod to live.This corresponds to the kube-scheduler component in the control plane. It’s basically the "matchmaker" that picks a home for the pod based on available RAM and CPU.

---

### 3. In `kubectl get pods -n kube-system`, name two components you recognised from the lecture and describe what they do.

* **etcd-minikube:** This is the cluster's "brain".
* **kube-apiserver:** This is the front door. Every time I type a `kubectl` command, I’m actually talking to this component.

---

### 4. **Image-specific observation** (Alpine):
**What happened to any changes you made inside the pod shell when you exited? Compare this to your experience in Docker Lab 1.**

When I exited and deleted the pod, all my changes vanished. Unlike Docker Lab 1, where a container might stick around unless I explicitly remove it.

---

### 5. Task 6 reflection: 
**After deleting the pod, Kubernetes did not restart it. In one paragraph, explain why, and what Kubernetes object would change this behaviour.**

Kubernetes didn't restart `my-pod` because I created it as "run this once," but I didn't give it a supervisor. If I want it to be "self-healing" and come back after a deletion or crash, I should use a Deployment or a ReplicaSet.