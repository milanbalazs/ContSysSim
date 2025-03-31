# Configuration-Based Container Simulation

This guide explains how to set up and run the simulation using a YAML configuration file.
The configuration file allows you to define the entire simulation environment,
including Nodes, Containers, Workloads, and an optional Load Balancer.

---

## Running the Simulation

1. Prepare a YAML configuration file that describes your simulation environment (see example below).
2. Run the simulation by specifying the configuration file as an argument:

   ```bash
   python cli_starter.py --config path/to/config.yml
   ```

---

## Configuration File Structure

The YAML configuration file contains the following sections:

### 1. **Simulation Duration**
Defines the total duration of the simulation in time units.

```yaml
simulation:
  duration: 15  # Total simulation time in units
```

---

### 2. **Data Center**
Defines the data center, including its Nodes and their associated Containers.

#### Example:

```yaml
datacenter:
  name: Datacenter-1
  nodes:
    - name: Node-1
      cpu: 16                # Total CPU cores
      ram: 32768             # RAM in MB
      disk: 40960            # Disk in MB
      bandwidth: 20000       # Bandwidth in Mbps
      start_up_delay: 0.1    # Node startup delay
      cpu_fluctuation_percent: 4.0  # CPU fluctuation percentage
      ram_fluctuation_percent: 9.0
      disk_fluctuation_percent: 2.0
      bandwidth_fluctuation_percent: 12.0
      stop_lack_of_resource: false  # Whether Node stops when resources are insufficient
      containers:
        - name: Container-1
          cpu: 4                # CPU allocation
          ram: 2048             # RAM in MB
          disk: 4096            # Disk in MB
          bandwidth: 2000       # Bandwidth in Mbps
          start_up_delay: 0.2   # Container startup delay
          cpu_fluctuation_percent: 2.0  # CPU fluctuation percentage
          ram_fluctuation_percent: 4.0
          disk_fluctuation_percent: 1.0
          bandwidth_fluctuation_percent: 3.0
          workloads:
            - cpu: 2.0
              ram: 1024
              disk: 2048
              bandwidth: 800
              delay: 1.0        # Delay before workload starts
              duration: 8.0     # Duration of the workload
              cpu_fluctuation_percent: 5.0
              ram_fluctuation_percent: 10.0
              disk_fluctuation_percent: 2.0
              bandwidth_fluctuation_percent: 6.0
              priority: 2       # Priority level of workload
              type: Backend Job # Workload type
```

#### Key Parameters:
- **Nodes**:
  - `cpu`, `ram`, `disk`, `bandwidth`: Resource capacities for the Node.
  - `start_up_delay`: Startup delay for the Node.
  - `*_fluctuation_percent`: Fluctuation percentages for resources.
  - `stop_lack_of_resource`: Whether the Node stops when resources are insufficient.

- **Containers**:
  - `cpu`, `ram`, `disk`, `bandwidth`: Resource allocations for the container.
  - `start_up_delay`: Startup delay for the container.
  - `*_fluctuation_percent`: Fluctuation percentages for container resources.

- **Workloads**:
  - `cpu`, `ram`, `disk`, `bandwidth`: Resource requirements of the workload.
  - `delay`: Delay before the workload starts.
  - `duration`: Duration the workload runs.
  - `priority`: Priority level for scheduling workloads.
  - `type`: Descriptive label for the workload.

---

### 3. **Load Balancer**
Defines an optional load balancer for distributing workloads across containers.

#### Example:

```yaml
load_balancer:
  enabled: true                       # Enable or disable the load balancer
  type: first-fit-with-reservations   # Options: 'first-fit-with-reservations', 'classic-first-fit'
  reservation_enabled: true           # Enable or disable reservation-based scheduling
  target_containers:
    - Container-1
    - Container-3
  workloads:
    - cpu: 1.0
      ram: 512
      disk: 1024
      bandwidth: 500
      delay: 3.0
      duration: 4.0
      cpu_fluctuation_percent: 5.0
      ram_fluctuation_percent: 8.0
      disk_fluctuation_percent: 1.5
      bandwidth_fluctuation_percent: 4.5
      priority: 1
      type: API Request
```

#### Key Parameters:
- **Load Balancer**:
  - `enabled`: Whether the load balancer is active.
  - `type`: The load balancing strategy (`first-fit-with-reservations` or `classic-first-fit`).
  - `reservation_enabled`: Enables reservation-based scheduling (optional).
  - `target_containers`: List of containers the load balancer targets.
  - `workloads`: List of workloads to be distributed by the load balancer.

---

## Example Configuration

Below is a complete example configuration file:

```yaml
simulation:
  duration: 15

datacenter:
  name: Datacenter-1
  nodes:
    - name: Node-1
      cpu: 16
      ram: 32768
      disk: 40960
      bandwidth: 20000
      start_up_delay: 0.1
      cpu_fluctuation_percent: 4.0
      ram_fluctuation_percent: 9.0
      disk_fluctuation_percent: 2.0
      bandwidth_fluctuation_percent: 12.0
      stop_lack_of_resource: false
      containers:
        - name: Container-1
          cpu: 4
          ram: 2048
          disk: 4096
          bandwidth: 2000
          start_up_delay: 0.2
          cpu_fluctuation_percent: 2.0
          ram_fluctuation_percent: 4.0
          disk_fluctuation_percent: 1.0
          bandwidth_fluctuation_percent: 3.0
          workloads:
            - cpu: 2.0
              ram: 1024
              disk: 2048
              bandwidth: 800
              delay: 1.0
              duration: 8.0
              cpu_fluctuation_percent: 5.0
              ram_fluctuation_percent: 10.0
              disk_fluctuation_percent: 2.0
              bandwidth_fluctuation_percent: 6.0
              priority: 2
              type: Backend Job

load_balancer:
  enabled: true
  type: first-fit-with-reservations
  reservation_enabled: true
  target_containers:
    - Container-1
  workloads:
    - cpu: 1.0
      ram: 512
      disk: 1024
      bandwidth: 500
      delay: 3.0
      duration: 4.0
      cpu_fluctuation_percent: 5.0
      ram_fluctuation_percent: 8.0
      disk_fluctuation_percent: 1.5
      bandwidth_fluctuation_percent: 4.5
      priority: 1
      type: API Request
```

---

## Output

When the simulation runs, the following information will be logged:
- **Resource usage summary** for Nodes and Containers.
- **Workload execution status**, including delays, start times, and completion.
- Optionally, **visualizations** of resource usage over time.

---

## Notes

- Use the `--config` option to specify the path to your YAML configuration file.
- Ensure that the YAML file adheres to the structure provided above.
- Log files and optional visualizations will be generated in the current directory.
