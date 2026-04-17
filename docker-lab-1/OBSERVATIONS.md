# Docker Lab 1 Observations — Alpine:3.19

### 1. Image Size

The size of my `alpine:3.19` image is **3.42MB** (Content Size) or **11.5MB** (Disk Usage). This is considered small compared to other local images like `postgres:17`, which is 161MB. This small footprint is due to Alpine including only the bare essentials needed for a Linux environment without any bloated utilities.

### 2. Image Layers

My image has **2 layers**:

- **Layer 1 (Bottom):** Adds the `alpine-minirootfs` tarball (8.08MB), which contains the root filesystem and base OS files.
- **Layer 2 (Top):** Sets the default command (`CMD ["/bin/sh"]`), which occupies 0B as it is a configuration change rather than a file addition.

### 3. Operating System and Architecture

According to the `docker inspect` metadata:

- **OS:** linux
- **Architecture:** amd64

### 4. Alpine Specific Exploration

When I installed `curl` inside the container using `apk add curl`, the package manager added the tool to the container's temporary writable layer. after exiting and starting a brand new container, `curl` was **no longer installed**. This occurs because Docker containers are ephemeral; changes made during runtime are restricted to that specific container instance and are not saved back to the read-only base image.

### 5. Personal Reflection

I was surprised by how tiny the Alpine image is—only about 3MB for a full Linux environment and It showed me how Docker keeps things clean and isolated without the heavy setup of a traditional virtual machine.
