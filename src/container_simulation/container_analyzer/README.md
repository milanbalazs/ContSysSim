# Container Analyzer

## **1. CPU Usage Calculation**

**To compute CPU usage, we need the following parameters:**

- `cpu_stats['cpu_usage']['total_usage']`
- `precpu_stats['cpu_usage']['total_usage']`
- `cpu_stats['system_cpu_usage']`
- `precpu_stats['system_cpu_usage']`
- `cpu_stats['online_cpus']`

### **Formula**

$$\text{CPU Usage (%)} = \left(\frac{\Delta \text{total usage}}{\Delta \text{system usage}} \right) \times \text{online CPUs} \times 100$$

Where:

$\Delta \text{total usage} = \text{cpu_stats['cpu_usage']['total_usage']} - \text{precpu_stats['cpu_usage']['total_usage']}$

$\Delta \text{system usage} = \text{cpu_stats['system_cpu_usage']} - \text{precpu_stats['system_cpu_usage']}$

$\text{online CPUs} = \text{cpu_stats['online_cpus']}$

### **Description**

- `total_usage` represents the CPU time consumed by the container.
- `system_cpu_usage` represents the total system CPU time.
- We take the difference between current and previous values to get the CPU usage over a time interval.
- The result is multiplied by the number of CPUs to normalize the value.

---

## **2. RAM Usage Calculation**

**To determine memory consumption, we need:**

- `memory_stats['usage']` (current memory usage in bytes)
- `memory_stats['limit']` (total memory allocated)

### **Formula**

$$\text{RAM Usage (%)} = \left(\frac{\text{memory_stats['usage']}}{\text{memory_stats['limit']}} \right) \times 100$$

### **Description**
- The formula calculates how much of the allocated memory is currently used.
- If `memory_stats['limit']` is `0`, we avoid division by zero.

---

## **3. Disk I/O Usage Calculation**

**To determine disk read/write operations, we extract:**

- `blkio_stats['io_service_bytes_recursive']` (list of read/write operations)

From this list, we sum:

- `'op': 'read'` → Total bytes read
- `'op': 'write'` → Total bytes written

### **Formulas**
$$\text{Disk Read Speed (B/s)} = \frac{\Delta \text{read bytes}}{\Delta t}$$

$$\text{Disk Write Speed (B/s)} = \frac{\Delta \text{write bytes}}{\Delta t}$$

where:

$\Delta \text{read bytes} = \sum_{\text{op='read'}} \text{value (current)} - \sum_{\text{op='read'}} \text{value (previous)}$

$\Delta \text{write bytes} = \sum_{\text{op='write'}} \text{value (current)} - \sum_{\text{op='write'}} \text{value (previous)}$

$\Delta t = \text{time difference between 'read' and 'preread'}$

### **Description**

- We compute the difference between the current and previous read/write byte values.
- The values are divided by the time difference to get the speed in bytes per second.

---

## **4. Network Bandwidth Usage Calculation**

**To determine network traffic, we use:**

- `networks['eth0']['rx_bytes']` → Received bytes
- `networks['eth0']['tx_bytes']` → Transmitted bytes

### **Formulas**


$$\text{Network Receive Speed (B/s)} = \frac{\Delta \text{rx_bytes}}{\Delta t}$$

$$\text{Network Transmit Speed (B/s)} = \frac{\Delta \text{tx_bytes}}{\Delta t}$$

where:

$\Delta \text{rx_bytes} = \text{current rx_bytes} - \text{previous rx_bytes}$

$\Delta \text{tx_bytes} = \text{current tx_bytes} - \text{previous tx_bytes}$

$\Delta t = \text{time difference between 'read' and 'preread'}$

### **Description**

- The number of bytes received and transmitted is measured over the time interval.
- The rates are computed in bytes per second.
