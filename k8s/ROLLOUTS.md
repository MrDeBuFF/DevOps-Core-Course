# Lab 14 — Progressive Delivery with Argo Rollouts

---

## 1. Argo Rollouts Setup

### Installation

Argo Rollouts controller was installed into the cluster:

```bash
kubectl create namespace argo-rollouts

kubectl apply -n argo-rollouts \
  -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```

Verification:

```bash
kubectl get pods -n argo-rollouts
```

![](screenshots_l14/t1_p1.png)

---

### CLI Plugin

Installed using:

```bash
brew install argoproj/tap/kubectl-argo-rollouts
```

Verification:

```bash
kubectl argo rollouts version
```

![](screenshots_l14/t1_p2.png)

---

### Dashboard

Installed dashboard:

```bash
kubectl apply -n argo-rollouts \
  -f https://github.com/argoproj/argo-rollouts/releases/latest/download/dashboard-install.yaml
```

Access:

```bash
kubectl port-forward svc/argo-rollouts-dashboard -n argo-rollouts 3100:3100
```

![](screenshots_l14/t1_p3.png)

Open in browser:

```
http://localhost:3100
```

![](screenshots_l14/t1_p4.png)

---

### Rollout vs Deployment

| Feature             | Deployment    | Rollout             |
| ------------------- | ------------- | ------------------- |
| Update strategy     | RollingUpdate | Canary / Blue-Green |
| Traffic control     | ❌             | ✅                   |
| Manual promotion    | ❌             | ✅                   |
| Rollback control    | Basic         | Advanced            |
| Metrics integration | ❌             | ✅                   |

---

## 2. Canary Deployment

### Strategy Configuration

Deployment was replaced with Rollout using canary strategy:

```yaml
strategy:
  canary:
    steps:
      - setWeight: 20
      - pause: {}

      - setWeight: 40
      - pause:
          duration: 30s

      - setWeight: 60
      - pause:
          duration: 30s

      - setWeight: 80
      - pause:
          duration: 30s

      - setWeight: 100
```

#### Explanation

* 20% traffic → manual approval required
* 40%, 60%, 80% → automatic progression after 30 seconds
* 100% → full rollout

---

### Rollout Process

1. Initial deployment (v1)
2. Update application (e.g. change VERSION env)
3. Rollout starts automatically
4. Traffic gradually shifts to new version

![](screenshots_l14/t2_p1.png)

![](screenshots_l14/t2_p2.png)

![](screenshots_l14/t2_p3.png)

![](screenshots_l14/t2_p4.png)

---

### Manual Promotion

Command:

```bash
kubectl argo rollouts promote <rollout-name> -n dev
```

Used to move past manual pause (20%).

![](screenshots_l14/t2_p5.png)

![](screenshots_l14/t2_p6.png)

![](screenshots_l14/t2_p7.png)

---

### Rollback (Abort)

Command:

```bash
kubectl argo rollouts abort <rollout-name> -n dev
```

Result:

* Traffic immediately shifts back to stable version

![](screenshots_l14/t2_p8.png)

![](screenshots_l14/t2_p9.png)

![](screenshots_l14/t2_p10.png)

---

## 3. Blue-Green Deployment

### Strategy Configuration

```yaml
strategy:
  blueGreen:
    activeService: <app-name>
    previewService: <app-name>-preview
    autoPromotionEnabled: false
```

---

### Key Concepts

* **Active Service (Blue)** → production traffic
* **Preview Service (Green)** → new version for testing

---

### Deployment Flow

#### Step 1 — Initial Deployment (Blue)

* Only active service is used
* Stable version is running

![](screenshots_l14/t3_p1.png)

![](screenshots_l14/t3_p2.png)

---

#### Step 2 — Deploy New Version (Green)

Triggered by changing values (e.g. VERSION):

```yaml
env:
  VERSION: "v3"
```

Result:

* New pods are created
* They are attached to **preview service**

![](screenshots_l14/t3_p3.png)

![](screenshots_l14/t3_p4.png)

![](screenshots_l14/t3_p5.png)

![](screenshots_l14/t3_p6.png)

---

### Promotion

```bash
kubectl argo rollouts promote <rollout-name> -n dev
```

Result:

* Traffic switches instantly from blue → green

![](screenshots_l14/t3_p7.png)

![](screenshots_l14/t3_p8.png)

---

### Rollback

```bash
kubectl argo rollouts undo <rollout-name> -n dev
```

Result:

* Instant switch back to previous version

![](screenshots_l14/t3_p9.png)

![](screenshots_l14/t3_p10.png)

![](screenshots_l14/t3_p11.png)

---

## 4. Strategy Comparison

### Canary vs Blue-Green

| Feature        | Canary  | Blue-Green     |
| -------------- | ------- | -------------- |
| Traffic shift  | Gradual | Instant        |
| Risk level     | Low     | Medium         |
| Rollback       | Fast    | Instant        |
| Resource usage | Low     | High (2x pods) |
| Testing        | Limited | Full preview   |

---

### When to Use

#### Canary

Use when:

* You want gradual exposure
* You need to monitor metrics
* You want minimal risk

#### Blue-Green

Use when:

* You need full testing before release
* Instant rollback is critical
* Downtime must be zero

---

### Pros & Cons

#### Canary

Pros:

* Safer rollout
* Gradual exposure
* Works well with metrics

Cons:

* Slower deployment
* More complex

---

#### Blue-Green

Pros:

* Instant switch
* Easy rollback
* Full testing before release

Cons:

* Requires double resources
* More infrastructure overhead

---

### Recommendation

* Use **Canary** for production systems with high risk
* Use **Blue-Green** for critical systems where rollback speed is important

---

## 5. CLI Commands Reference

### Monitoring

```bash
kubectl get rollouts -n dev
kubectl argo rollouts get rollout <name> -n dev -w
```

---

### Control

```bash
kubectl argo rollouts promote <name> -n dev
kubectl argo rollouts abort <name> -n dev
kubectl argo rollouts retry <name> -n dev
kubectl argo rollouts undo <name> -n dev
```

---

### Debugging

```bash
kubectl describe rollout <name> -n dev
kubectl get pods -n dev
kubectl get svc -n dev
```

---

### ArgoCD

```bash
kubectl get applications -n argocd
kubectl describe application <name> -n argocd
```

