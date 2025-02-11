# Saturation

## Workload Saturation Calculation

### **Formula for Workload Saturation/Fluctuation**

Let:

- $R$ = Base resource requirement (e.g., CPU, RAM, Disk, Bandwidth).
- $S$ = Saturation percentage (e.g., $cpu{\_saturation\_percent}$).
- $R_{current}$ = Current workload requirement after fluctuation.
- $R_{saturation}$ = Saturation effect applied to the base resource.
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

### **Current Saturation Formula**

The saturation effect $R_{saturation}$ is a random deviation from the base value within $\pm S$:

$$R_{\text{saturation}} = \text{Random}(-\frac{R \cdot S}{100}, \frac{R \cdot S}{100})$$

---

### **Example for CPU Saturation**

Given:

- $R = 2.5$ [core] (Base CPU requirement).
- $S = 10$ [%] (CPU saturation percentage).

1. **Bounds for Current Workload**:

   $$LB = 2.5 - \frac{2.5 \cdot 10}{100} = 2.5 - 0.25 = 2.25$$

   $$UB = 2.5 + \frac{2.5 \cdot 10}{100} = 2.5 + 0.25 = 2.75$$

   The randomly fluctuated current workload $R_{current}$ lies between $2.25$ and $2.75$.

2. **Saturation Effect**:

   $$R_{saturation} = Random(-\frac{2.5 \cdot 10}{100}, \frac{2.5 \cdot 10}{100}) = Random(-0.25, 0.25)$$

---

### **Generalized Formula**

For any resource type (CPU, RAM, Disk, Bandwidth):

1. **Current Workload**:

   $$R_{current} = Random\left(R - \frac{R \cdot S}{100}, R + \frac{R \cdot S}{100}\right)$$

2. **Current Saturation**:

   $$R_{saturation} = Random\left(-\frac{R \cdot S}{100}, \frac{R \cdot S}{100}\right)$$

This formula allows realistic workload behavior by simulating fluctuating resource demands.

---

## Container Saturation

### **Formula for Container Resource Saturation**

Containers experience resource fluctuations due to workload assignments and base saturation applied dynamically. The total **current resource usage** for a container is calculated as:

$$C_{current} = \sum_{i=1}^{n} W_{current} + C_{saturation}$$

Where:

- $C_{current}$ = Current total resource usage of the container.
- $W_{current}$ = Current workload requirements of the $i.$ active workload.
- $n$ = Number of active workloads assigned to the container.
- $C_{saturation}$ = Base saturation applied to the container's total resource limits.

---

### **Base Saturation Formula**

The base saturation $C_{saturation}$ for the container is calculated as:

$$C_{\text{saturation}} = Random\left(-\frac{C \cdot S}{100}, \frac{C \cdot S}{100}\right)$$

Where:

- $C$ = Container's base resource limit (e.g., CPU, RAM, Disk, Bandwidth).
- $S$ = Saturation percentage for the corresponding resource.

---

### **Example for Container CPU Saturation**

Given:

- $C = 2$ [core] (Base CPU limit for the container).
- $S = 5$ [%] (CPU saturation percentage for the container).

**Saturation Calculation**:

   $$C_{\text{saturation}} = Random(-\frac{2 \cdot 5}{100}, \frac{2 \cdot 5}{100}) = Random(-0.1, 0.1)$$

**Resulting CPU Usage**:

   $$C_{current} = \sum_{i=1}^{n} W_{current} + C_{\text{saturation}}$$

---

## VM Saturation

### **Formula for VM Resource Saturation**

Virtual Machines experience saturation effects on their **available resources** (total capacity minus the usage by containers). The **current available resource** for a VM is:

$$V_{available} = V - \sum_{i=1}^{m} C_{current} + V_{saturation}$$

Where:

- $V_{available}$ = Current available resource in the VM.
- $V$ = Total resource capacity of the VM (e.g., CPU, RAM, Disk, Bandwidth).
- $C_{current}$ = Current resource usage of the $i$. container assigned to the VM.
- $m$ = Number of containers in the VM.
- $V_{saturation}$ = Saturation effect applied to the VM's total resource capacity.

---

### **Base Saturation Formula**

The base saturation $V_{saturation}$ for the VM is calculated as:

$$V_{\text{saturation}} = Random\left(-\frac{V \cdot S}{100}, \frac{V \cdot S}{100}\right)$$

Where:

- $V$ = VM's total resource capacity (e.g., CPU, RAM, Disk, Bandwidth).
- $S$ = Saturation percentage for the corresponding resource.

---

### **Example for VM RAM Saturation**

Given:

- $V = 16,384$ [MB] (Base RAM capacity for the VM).
- $S = 8$ [%] (RAM saturation percentage for the VM).
- Total RAM usage by containers: $\sum_{i=1}^{m} C_{current} = 12,000$ [MB].

**Saturation Calculation**:

   $$V_{\text{saturation}} = Random(-\frac{16,384 \cdot 8}{100}, \frac{16,384 \cdot 8}{100}) = Random(-1,310.72, 1,310.72)$$

**Available RAM**:

   $$V_{available} = 16,384 - (12,000 + V_{\text{saturation}})$$

---

## Summary

1. **Workload Fluctuation**:

   $$R_{current} = Random(R - \frac{R \cdot S}{100}, R + \frac{R \cdot S}{100})$$

2. **Container Saturation**:

   $$C_{current} = \sum_{i=1}^{n} W_{current} + C_{\text{saturation}}$$

3. **VM Saturation**:

   $$V_{available} = V - \sum_{i=1}^{m} C_{current} + V_{\text{saturation}}$$
