# V4 Physics Model

V4 is a robust research-oriented OpenFOAM study for hydrogen leak monitoring in a ventilated room.

## Room

- Size: 8 m × 6 m × 3 m
- Inlet at x = 0
- Outlet at x = 8
- Conceptual room includes door/window/cabinet/equipment for the realistic study narrative.

## Solver

`scalarTransportFoam` is used for stability on OpenFOAM v2412.

The scalar field `T` is interpreted as hydrogen concentration proxy.

## Buoyancy approximation

Hydrogen is lighter than air. Instead of using a full multi-species buoyant solver, V4 uses an upward drift component in the velocity field:

- Mean ventilation: along +x
- Buoyancy drift: +z
- Leak injection velocity: upward from the floor patch

This lets the H2 plume rise toward the ceiling and be transported toward the outlet.

## What is realistic?

Included:

- gravity file `constant/g`
- upward H2 movement
- ventilation transport
- turbulent effective diffusivity
- long animation time, 300 s
- many leak positions and leak strengths
- fixed vs mobile sensing dataset

Approximated:

- density coupling is not solved dynamically
- air/H2 mixture is not solved as a full multi-component gas
- obstacles are part of the study design and visualization plan, but not blocking flow in the V4 mesh

## Next physics upgrade

The next rigorous model should use:

- `buoyantPimpleFoam` or a multi-component solver
- density depending on H2 mass fraction
- turbulence model such as kOmegaSST
- real obstacles meshed with snappyHexMesh
