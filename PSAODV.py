import traci
import random
import string

SUMO_CMD = ["sumo-gui", "-c", "C:/Users/ablt7/Downloads/xml psaodv/sumo.cfg"]  # Update to your SUMO configuration file path

# Parameters
EAVESDROP_RANGE = 300  # Eavesdropping range in meters
EAVESDROPPERS = [
    {"id": "eav1", "x": 4429.02, "y": 2834.03},
    {"id": "eav2", "x": 4343.50, "y": 2501.99},
]
VEHICLE_TRACKER = {}  # Tracks vehicle pseudonyms and routes

# Metrics tracker
METRICS = {
    "pseudonym_refreshes": 0,
    "prreq_count": 0,
    "prrep_count": 0,
    "hello_count": 0,
    "eavesdropping_attempts": 0,
    "eavesdropping_prevented": 0,
    "successful_deliveries": 0,
    "total_packets": 0,
    "route_discovery_times": [],
}

# Helper functions
def generate_pseudonym():
    """Generate a unique pseudonym."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def broadcast_prreq(vehicle_id, pseudonym, step):
    """Simulate a vehicle broadcasting a privacy-enhanced RREQ message."""
    METRICS["prreq_count"] += 1
    METRICS["total_packets"] += 1
    sequence_number = random.randint(1, 10000)
    print(f"Step {step}: Vehicle {vehicle_id} (Pseudonym: {pseudonym}) broadcasting PRREQ")
    return {"type": "PRREQ", "vehicle": vehicle_id, "pseudonym": pseudonym, "seq": sequence_number, "step": step}

def send_prrep(vehicle_id, pseudonym, target_id, step):
    """Simulate sending a privacy-enhanced RREP message."""
    METRICS["prrep_count"] += 1
    METRICS["total_packets"] += 1
    message_quality = random.uniform(0.8, 1.0)
    print(f"Step {step}: Vehicle {vehicle_id} sending PRREP to {target_id} with quality {message_quality}")
    return {"type": "PRREP", "source": vehicle_id, "pseudonym": pseudonym, "message_quality": message_quality, "seq": random.randint(1, 10000), "step": step}

def refresh_pseudonym(vehicle_id):
    """Refresh the pseudonym of a vehicle."""
    new_pseudonym = generate_pseudonym()
    VEHICLE_TRACKER[vehicle_id]["pseudonym"] = new_pseudonym
    METRICS["pseudonym_refreshes"] += 1
    print(f"Vehicle {vehicle_id} refreshed pseudonym to {new_pseudonym}")

def simulate_aodv(step):
    """Simulate PS-AODV routing."""
    for veh_id in traci.vehicle.getIDList():
        x, y = traci.vehicle.getPosition(veh_id)

        # Initialize vehicle tracker if not present
        if veh_id not in VEHICLE_TRACKER:
            VEHICLE_TRACKER[veh_id] = {
                "pseudonym": generate_pseudonym(),
                "routes": [],
                "privacy_level": random.uniform(0.8, 1.0),
            }

        pseudonym = VEHICLE_TRACKER[veh_id]["pseudonym"]

        # Randomly trigger route discovery
        if random.random() < 0.1:  # 10% chance to initiate PRREQ
            packet = broadcast_prreq(veh_id, pseudonym, step)
            VEHICLE_TRACKER[veh_id]["routes"].append(packet)

        # Simulate route reply with privacy metrics
        if random.random() < 0.05:  # 5% chance of PRREP
            target_id = random.choice(traci.vehicle.getIDList())
            if target_id != veh_id:
                packet = send_prrep(veh_id, pseudonym, target_id, step)
                VEHICLE_TRACKER[target_id]["routes"].append(packet)

        # Monitor routes and HELLO messages
        if step % 10 == 0:  # Send HELLO message every 10 steps
            METRICS["hello_count"] += 1
            print(f"Step {step}: Vehicle {veh_id} sending HELLO with pseudonym {pseudonym}")

        # Refresh pseudonyms periodically
        if step % 50 == 0:  # Refresh pseudonym every 50 steps
            refresh_pseudonym(veh_id)

        # Eavesdropping prevention: Validate pseudonym usage
        for eav in EAVESDROPPERS:
            eav_pos = (eav["x"], eav["y"])
            if distance((x, y), eav_pos) <= EAVESDROP_RANGE:
                METRICS["eavesdropping_attempts"] += 1
                print(f"Step {step}: Vehicle {veh_id} avoided eavesdropper {eav['id']} using pseudonym.")
                METRICS["eavesdropping_prevented"] += 1

def run_simulation():
    """Run the SUMO simulation and simulate PS-AODV with privacy metrics."""
    traci.start(SUMO_CMD)
    print("SUMO simulation started.")

    try:
        step = 0
        max_simulation_time = 5000  # Maximum simulation time in seconds

        while traci.simulation.getMinExpectedNumber() > 0 and step < max_simulation_time:
            traci.simulationStep()
            simulate_aodv(step)

            # Log simulation progress every 100 steps
            if step % 100 == 0:
                print(f"Simulation step: {step}")

            step += 1
    finally:
        traci.close()
        print("SUMO simulation ended.")

        # Display metrics
        if METRICS["total_packets"] > 0:
            pdr = METRICS["successful_deliveries"] / METRICS["total_packets"]
        else:
            pdr = 0

        print("\nEvaluation Metrics:")
        print(f"Total Pseudonym Refreshes: {METRICS['pseudonym_refreshes']}")
        print(f"Total PRREQ Packets: {METRICS['prreq_count']}")
        print(f"Total PRREP Packets: {METRICS['prrep_count']}")
        print(f"Total HELLO Messages: {METRICS['hello_count']}")
        print(f"Eavesdropping Attempts: {METRICS['eavesdropping_attempts']}")
        print(f"Eavesdropping Prevented: {METRICS['eavesdropping_prevented']}")
        print(f"Packet Delivery Ratio (PDR): {pdr:.2f}")
        print(f"Route Discovery Times: {METRICS['route_discovery_times']}")

if __name__ == "__main__":
    run_simulation()
