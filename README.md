# VANET Simulation with Secure AODV Routing (PSAODV)

## Project Description
This project implements a simulation environment for Vehicular Ad Hoc Networks (VANETs) focusing on Secure AODV Routing (PSAODV). The PSAODV protocol enhances the standard AODV by introducing pseudonym changes to protect vehicle privacy from eavesdropping attacks. The project uses:

- **SUMO**: For traffic mobility simulation.
- **Python**: To process mobility files and integrate them with the network simulator.
---

## Features
- Generates realistic vehicle mobility traces using SUMO.
- Implements a pseudonym-based secure AODV routing protocol.
- Evaluates performance metrics like privacy, packet delivery ratio, and end-to-end delay.
- Supports integration with Python.

---

## Getting Started

### Prerequisites
Ensure the following software is installed:
- **Python 3.x**
- **SUMO**: [Download](https://www.eclipse.org/sumo/)
- **TraCI Python Library**: `pip install sumolib traci`

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/nicsetty/vanet-psaodv.git
   cd vanet-psaodv
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
---

## Usage

### Step 1: Generate Mobility Traces
Run the SUMO simulation to generate vehicle mobility traces:
```bash
sumo -c sumo/sumo.cfg
```

### Step 2: Run the PSAODV Simulation
Execute the Python script to simulate PSAODV routing:
```bash
python psaodv/psaodv.py
```

### Step 3: Analyze Results
View and analyze the results stored in the `results/` directory.

---

## How PSAODV Works
1. **Pseudonym Changes**:
   - Vehicles frequently change their pseudonyms during route requests (RREQ) and route replies (RREP).
   - This protects against tracking by eavesdroppers.

2. **Integration with SUMO**:
   - Mobility traces from SUMO are used to simulate realistic vehicle movements.

3. **Performance Metrics**:
   - Privacy preservation: Evaluated by pseudonym changes.
   - Packet delivery ratio and end-to-end delay: Measured during simulation.

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add new feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a pull request.

---

## References
This project is based on a research paper titled [Secure AODV Routing Strategies in Smart Cities for Vehicular Communication](https://www.iieta.org/journals/jesa/paper/10.18280/jesa.570325), with a few modifications: instead of using OMNET++, we implemented the simulation using Python.

---

Happy Simulating! 🚗💨
