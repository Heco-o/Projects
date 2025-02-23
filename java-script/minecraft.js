function getRelativeAngle(playerLocation, playerDirection, targetLocation) {
    targetLocation.x += 1;

    const forwardMagnitude = Math.hypot(playerDirection.x, playerDirection.z);
    const normalizedForward = {
        x: playerDirection.x / forwardMagnitude,
        z: playerDirection.z / forwardMagnitude,
    };

    const toTarget = {
        x: targetLocation.x - playerLocation.x,
        z: targetLocation.z - playerLocation.z,
    };

    const targetMagnitude = Math.hypot(toTarget.x, toTarget.z);
    const normalizedToTarget = {
        x: toTarget.x / targetMagnitude,
        z: toTarget.z / targetMagnitude,
    };

    const forwardDot =
        normalizedToTarget.x * normalizedForward.x +
        normalizedToTarget.z * normalizedForward.z;

    const rightDot =
        normalizedToTarget.x * -normalizedForward.z +
        normalizedToTarget.z * normalizedForward.x;

    const angle = Math.atan2(rightDot, forwardDot) * (180 / Math.PI);

    return angle;
}

players = [];
speedrunners = [];
hunters = [];

system.runInterval(() => {
    players = world.getAllPlayers();
    speedrunners = [];
    hunters = [];
    players.forEach((player) => {
        if (player.hasTag("speed")) {
            speedrunners.push(player);
        } else if (player.hasTag("hunter")) {
            hunters.push(player);
        }
    });
}, 20);

system.runInterval(() => {
    speedrunners.forEach((speedrunner) => {
        let closestDistance = Infinity;
        hunters.forEach((hunter) => {
            const { x: x1, y: y1, z: z1 } = speedrunner.location;
            const { x: x2, y: y2, z: z2 } = hunter.location;

            const distance = Math.hypot(x2 - x1, y2 - y1, z2 - z1);
            if (distance < closestDistance) {
                closestDistance = distance;
            }
        });
        speedrunner.onScreenDisplay.setActionBar(
            `Closest Hunter: ${Math.round(closestDistance)} Blocks`
        );
    });
}, 1);

system.runInterval(() => {
    hunters.forEach((hunter) => {
        let closestSpeedrunner;
        let closestDistance = Infinity;
        speedrunners.forEach((speedrunner) => {
            const {x: x1, y: y1, z: z1} = hunter.location;
            const {x: x2, y: y2, z: z2} = speedrunner.location;

            const distance = Math.hypot(x2 - x1, y2 - y1, z2 - z1);
            if (hunter.dimension.id === speedrunner.dimension.id && distance < closestDistance) {
                closestDistance = distance;
                closestSpeedrunner = speedrunner;
            }
        });
        
        if (closestSpeedrunner !== undefined) {
            hunter.onScreenDisplay.setActionBar(`Closest speedrunner: ${Math.round(getRelativeAngle(hunter.location, hunter.getViewDirection(), closestSpeedrunner.location))} Degrees`);
        } else {
            hunter.onScreenDisplay.setActionBar(`Closest speedrunner: Different Dimension`);
        }
    });
}, 1);