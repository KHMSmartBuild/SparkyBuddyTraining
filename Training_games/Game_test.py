import pybullet as p

# Set up the PyBullet simulation
p.connect(p.GUI)
p.setGravity(0, 0, -10)
p.setTimeStep(1 / 240)

# Define the objects in the simulation
planeId = p.createCollisionShape(p.GEOM_PLANE)
p.createMultiBody(0, planeId)
boxId = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.2, 0.2, 0.2])
batteryId = p.createMultiBody(baseCollisionShapeIndex=boxId, basePosition=[0, 0, 1])
switchId = p.createMultiBody(baseCollisionShapeIndex=boxId, basePosition=[0.5, 0, 1])
bulbId = p.createMultiBody(baseCollisionShapeIndex=boxId, basePosition=[1, 0, 1])

# Define the joints between objects
p.createConstraint(batteryId, -1, switchId, -1, p.JOINT_FIXED, [0.1, 0, 0], [0, 0, 0], [0, 0, 0])
p.createConstraint(switchId, -1, bulbId, -1, p.JOINT_FIXED, [0.1, 0, 0], [-0.1, 0, 0], [0, 0, 0])

# Run the simulation
for i in range(240):
    # Check if the switch is on or off
    switchState = p.getJointState(switchId, 0)[0]
    if switchState > 0:
        # If the switch is on, turn on the light bulb
        p.changeVisualShape(bulbId, -1, rgbaColor=[1, 1, 0, 1])
    else:
        # If the switch is off, turn off the light bulb
        p.changeVisualShape(bulbId, -1, rgbaColor=[0, 0, 0, 1])
    p.stepSimulation()
