import traci
import random

SUMO_CMD = ["sumo-gui", "-c", "C:/Users/ablt7/Downloads/xml psaodv/sumo.cfg"]

# Eavesdropping station parameters
EAVESDROP_RANGE = 300  # Eavesdropping range in meters
EAVESDROPPERS = [
    {"id": "eav1", "x": 4429.02, "y": 2834.03},
    {"id": "eav2", "x": 4343.50, "y": 2501.99},
]
VEHICLE_TRACKER = {}  # Tracks vehicle trajectory and intercepted packets

def distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def broadcast_rreq(vehicle_id, step):
    """Simulate a vehicle broadcasting an RREQ message."""
    sequence_number = random.randint(1, 10000)  # Generate a random sequence number
    return {"type": "RREQ", "vehicle": vehicle_id, "seq": sequence_number, "step": step}

def send_rrep(vehicle_id, target_id, step):
    """Simulate sending an RREP message."""
    sequence_number = random.randint(1, 10000)  # Generate a random sequence number
    return {"type": "RREP", "source": target_id, "vehicle": vehicle_id, "seq": sequence_number, "step": step}

def track_vehicle(vehicle_id, packet, step):
    """Track intercepted packets for a vehicle."""
    if vehicle_id not in VEHICLE_TRACKER:
        VEHICLE_TRACKER[vehicle_id] = {"trajectory": [], "packets": set()}

    # Track vehicle's trajectory
    position = traci.vehicle.getPosition(vehicle_id)
    if not VEHICLE_TRACKER[vehicle_id]["trajectory"] or VEHICLE_TRACKER[vehicle_id]["trajectory"][-1] != position:
        VEHICLE_TRACKER[vehicle_id]["trajectory"].append(position)

    # Track unique packets
    packet_id = (packet["type"], packet["seq"], step)
    if packet_id not in VEHICLE_TRACKER[vehicle_id]["packets"]:
        VEHICLE_TRACKER[vehicle_id]["packets"].add(packet_id)

def simulate_aodv(step):
    """Simulate AODV routing and eavesdropping."""
    already_intercepted = set()  # To track intercepted packsets for this step

    for veh_id in traci.vehicle.getIDList():
        x, y = traci.vehicle.getPosition(veh_id)

        # Randomly trigger route discovery
        if random.random() < 0.1:  # 10% chance of RREQ
            packet = broadcast_rreq(veh_id, step)
            track_vehicle(veh_id, packet, step)

        # Randomly simulate a route reply
        if random.random() < 0.05:  # 5% chance of RREP
            target_id = random.choice(traci.vehicle.getIDList())
            if target_id != veh_id:
                packet = send_rrep(veh_id, target_id, step)
                track_vehicle(veh_id, packet, step)

        # Check for eavesdropping
        for eav in EAVESDROPPERS:
            eav_pos = (eav["x"], eav["y"])
            if distance((x, y), eav_pos) <= EAVESDROP_RANGE:
                for packet in VEHICLE_TRACKER[veh_id]["packets"]:
                    packet_id = (eav["id"], packet)
                    if packet_id not in already_intercepted:
                        print(f"Step {step}: Eavesdropper {eav['id']} intercepted {packet[0]} from {veh_id}")
                        already_intercepted.add(packet_id)

def run_simulation():
    """Run the SUMO simulation and simulate AODV with tracking."""
    traci.start(SUMO_CMD)
    print("SUMO simulation started.")

    try:
        step = 0
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            simulate_aodv(step)
            step += 1
    finally:
        traci.close()
        print("SUMO simulation ended.")
        # Display the vehicle tracker data
        print("\nTracked Vehicles:")
        for veh_id, data in VEHICLE_TRACKER.items():
            print(f"Vehicle {veh_id}:")
            print(f"  Trajectory: {data['trajectory']}")
            print(f"  Packets: {list(data['packets'])}")

if __name__ == "__main__":
    run_simulation()
