# Fluctuation

## Workload Fluctuation Calculation

### **Formula for Workload Fluctuation/Fluctuation**

Let:

- $R$ = Base resource requirement (e.g., CPU, RAM, Disk, Bandwidth).
- $S$ = Fluctuation percentage (e.g., $cpu\_fluctuation\_percent$).
- $R_{current}$ = Current workload requirement after fluctuation.
- $R_{fluctuation}$ = Fluctuation effect applied to the base resource.
- $LB$ = Lower bound of fluctuation = $R - \frac{R \cdot S}{100}$.
- $UB$ = Upper bound of fluctuation = $R + \frac{R \cdot S}{100}$.

---

### **Current Workload Fluctuation Formula**

The current workload $R_{current}$ is randomly chosen within the range of $LB$ and $UB$:

$$R_{current} = Random(LB, UB)$$

Where:

$$LB = R - \frac{R \cdot S}{100}$$

$$UB = R + \frac{R \cdot S}{100}$$

---

### **Current Fluctuation Formula**

The fluctuation effect $R_{fluctuation}$ is a random deviation from the base value within $\pm S$:

$$R_{\text{fluctuation}} = \text{Random}(-\frac{R \cdot S}{100}, \frac{R \cdot S}{100})$$

---

### **Example for CPU Fluctuation**

Given:

- $R = 2.5$ [core] (Base CPU requirement).
- $S = 10$ [%] (CPU fluctuation percentage).

1. **Bounds for Current Workload**:

   $$LB = 2.5 - \frac{2.5 \cdot 10}{100} = 2.5 - 0.25 = 2.25$$

   $$UB = 2.5 + \frac{2.5 \cdot 10}{100} = 2.5 + 0.25 = 2.75$$

   The randomly fluctuated current workload $R_{current}$ lies between $2.25$ and $2.75$.

2. **Fluctuation Effect**:

   $$R_{fluctuation} = Random(-\frac{2.5 \cdot 10}{100}, \frac{2.5 \cdot 10}{100}) = Random(-0.25, 0.25)$$

---

### **Generalized Formula**

For any resource type (CPU, RAM, Disk, Bandwidth):

1. **Current Workload**:

   $$R_{current} = Random\left(R - \frac{R \cdot S}{100}, R + \frac{R \cdot S}{100}\right)$$

2. **Current Fluctuation**:

   $$R_{fluctuation} = Random\left(-\frac{R \cdot S}{100}, \frac{R \cdot S}{100}\right)$$

This formula allows realistic workload behavior by simulating fluctuating resource demands.

---

## Container Fluctuation

### **Formula for Container Resource Fluctuation**

Containers experience resource fluctuations due to workload assignments and base fluctuation applied dynamically. The total **current resource usage** for a container is calculated as:

$$C_{current} = \sum_{i=1}^{n} W_{current} + C_{fluctuation}$$

Where:

- $C_{current}$ = Current total resource usage of the container.
- $W_{current}$ = Current workload requirements of the $i.$ active workload.
- $n$ = Number of active workloads assigned to the container.
- $C_{fluctuation}$ = Base fluctuation applied to the container's total resource limits.

---

### **Base Fluctuation Formula**

The base fluctuation $C_{fluctuation}$ for the container is calculated as:

$$C_{\text{fluctuation}} = Random(\left(-\frac{C \cdot S}{100}, \frac{C \cdot S}{100}\right)$$

Where:

- $C$ = Container's base resource limit (e.g., CPU, RAM, Disk, Bandwidth).
- $S$ = Fluctuation percentage for the corresponding resource.

---

### **Example for Container CPU Fluctuation**

Given:

- $C = 2$ [core] (Base CPU limit for the container).
- $S = 5$ [%] (CPU fluctuation percentage for the container).

**Fluctuation Calculation**:

   $$C_{\text{fluctuation}} = Random(-\frac{2 \cdot 5}{100}, \frac{2 \cdot 5}{100}) = Random(-0.1, 0.1)$$

**Resulting CPU Usage**:

   $$C_{current} = \sum_{i=1}^{n} W_{current} + C_{\text{fluctuation}}$$

---

## Node Fluctuation

### **Formula for Node Resource Fluctuation**

Virtual Machines experience fluctuation effects on their **available resources** (total capacity minus the usage by containers).
The fluctuation can be only positive because it represents the Nodes own consumption, like kernel functions or other processes.

The **current available resource** for a Node is:

$$V_{available} = V - \left(\sum_{i=1}^{m} C_{current} + V_{fluctuation}\right)$$

Where:

- $V_{available}$ = Current available resource in the Node.
- $V$ = Total resource capacity of the Node (e.g., CPU, RAM, Disk, Bandwidth).
- $C_{current}$ = Current resource usage of the $i$. container assigned to the Node.
- $m$ = Number of containers in the Node.
- $V_{fluctuation}$ = Fluctuation effect applied to the Node's total resource capacity.

---

### **Base Fluctuation Formula**

The base fluctuation $V_{fluctuation}$ for the Node is calculated as:

$$V_{\text{fluctuation}} = |Random\left(-\frac{V \cdot S}{100}, \frac{V \cdot S}{100}\right)|$$

Where:

- $V$ = Node's total resource capacity (e.g., CPU, RAM, Disk, Bandwidth).
- $S$ = Fluctuation percentage for the corresponding resource.

---

### **Example for Node RAM Fluctuation**

Given:

- $V = 16,384$ [MB] (Base RAM capacity for the Node).
- $S = 8$ [%] (RAM fluctuation percentage for the Node).
- Total RAM usage by containers: $\sum_{i=1}^{m} C_{current} = 12,000$ [MB].

**Fluctuation Calculation**:

   $$V_{\text{fluctuation}} = |Random(-\frac{16,384 \cdot 8}{100}, \frac{16,384 \cdot 8}{100})| = |Random(-1,310.72, 1,310.72)|$$

**Available RAM**:

   $$V_{available} = 16,384 - (12,000 + V_{\text{fluctuation}})$$

---

## Summary

1. **Workload Fluctuation**:

   $$R_{current} = Random(R - \frac{R \cdot S}{100}, R + \frac{R \cdot S}{100})$$

2. **Container Fluctuation**:

   $$C_{current} = \sum_{i=1}^{n} W_{current} + C_{\text{fluctuation}}$$

3. **Node Fluctuation**:

   $$V_{available} = V - \left(\sum_{i=1}^{m} C_{current} + V_{\text{fluctuation}}\right)$$
