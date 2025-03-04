# **Container Analyzer**

## **1. CPU Usage Calculation**

### **Extracted Parameters**

To compute **CPU cores used**, we need the following values from `Docker stats`:

- `cpu_stats['cpu_usage']['total_usage']`
- `precpu_stats['cpu_usage']['total_usage']`
- `cpu_stats['system_cpu_usage']`
- `precpu_stats['system_cpu_usage']`
- `cpu_stats['online_cpus']`

### **Formula**

$$\text{CPU Cores Used} = \left(\frac{\Delta \text{total usage}}{\Delta \text{system usage}} \right) \times \text{online CPUs}$$

Where:

$$\Delta \text{total usage} = \texttt{cpu\_stats['cpu\_usage']['total\_usage']} - \texttt{precpu_stats['cpu\_usage']['total\_usage']}$$

$$\Delta \text{system usage} = \texttt{cpu\_stats['system\_cpu\_usage']} - \texttt{precpu_stats['system\_cpu\_usage']}$$

$$\text{online CPUs} = \texttt{cpu\_stats['online\_cpus']}$$

### **Description**

- `total_usage` represents the CPU time consumed by the container.
- `system_cpu_usage` represents the total system CPU time.
- We take the difference between current and previous values to get the **CPU consumption**.
- The result is multiplied by the **number of available CPUs** to obtain **CPU cores actively used**.

---

## **2. RAM Usage Calculation**

### **Extracted Parameters**

To determine **RAM consumption in MB**, we need the following values from `Docker stats`:

- `memory_stats['usage']` (current memory usage in bytes)

### **Formula**

$$\text{RAM Usage (MB)} = \frac{\text{memory_stats['usage']}}{1024^2}$$

### **Description**

- This formula converts the memory usage from **bytes** to **megabytes (MB)**.
- Unlike percentage-based memory usage, this method provides the **exact amount of RAM consumed** by the container.

---

## **3. Disk Usage Calculation**

Instead of measuring **Disk Read/Write speeds**, we now compute the **total disk space used** by the container.

### **Extracted Parameters**

- `self.analyzer.get_disk_usage(container_id)`

### **Description**
- This retrieves the **total storage space occupied** by the container.
- Unlike disk I/O speed, this metric **shows actual space usage** on disk.

---

## **4. Network Usage Calculation**
Instead of measuring **network speed (MB/s)**, we calculate the **total network data used (MB)**.

### **Extracted Parameters**
To compute **total network traffic**, we need:
- `networks[interface]['rx_bytes']` → Total received bytes
- `networks[interface]['tx_bytes']` → Total transmitted bytes

### **Formula**
$$\text{Total Network RX (MB)} = \frac{\text{Final RX Bytes} - \text{Initial RX Bytes}}{1024^2}$$

$$\text{Total Network TX (MB)} = \frac{\text{Final TX Bytes} - \text{Initial TX Bytes}}{1024^2}$$

Where:

$$\text{Initial RX Bytes} = \text{start_stat['networks'][interface]['rx_bytes']}$$  
$$\text{Final RX Bytes} = \text{end_stat['networks'][interface]['rx_bytes']}$$

$$\text{Initial TX Bytes} = \text{start_stat['networks'][interface]['tx_bytes']}$$  
$$\text{Final TX Bytes} = \text{end_stat['networks'][interface]['tx_bytes']}$$  

### **Description**
- Instead of **network speed**, we now compute **total data sent and received** over the time window.
- This helps in tracking **container network consumption** instead of just speed.
