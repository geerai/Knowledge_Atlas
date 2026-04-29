"""bezier_wall_path.py — Track 3 Flagship sub-component.

Owner: <unassigned — claim in OWNERS.md>
Responsibility: parametric Bezier curve definition for the curved-wall floor
plan. Output: ordered (x, z) waypoints to be consumed by wall_extrusion.py.

Cited literature:
    Hillier, B., & Hanson, J. (1984). The social logic of space.
        Cambridge University Press.  (convex-map projection of the curved
        boundary; the worship room's floor plan is one convex region with
        a curved boundary, axially deep.)

Sprint 4 implementation: see README.md "Implementation (Weeks 6–8)".
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class BezierWallPathParams:
    """Inputs to the Bezier wall-path generator."""
    # Floor-plan diameter (metres). Vartanian 2015 cathedral effect peaks at ≥10 m.
    plan_diameter_m: float = 12.0
    # Curvature: 0 = polygonal, 1 = full circle/ellipse
    curvature: float = 0.85
    # Number of sample waypoints around the perimeter
    n_waypoints: int = 64
    # Apse depth (semicircular extension on the deep axis); 0 = no apse
    apse_depth_m: float = 2.0
    # Symmetry: "bilateral" (typical Christian) or "rotational" (typical Islamic)
    symmetry: str = "bilateral"


@dataclass
class BezierWallPathResult:
    """Typed output for downstream wall_extrusion.py consumption."""
    # Ordered list of (x, z) waypoints around the perimeter, closed loop
    waypoints: list[tuple[float, float]] = field(default_factory=list)
    # Per-waypoint outward normal (for wall thickness offset)
    outward_normals: list[tuple[float, float]] = field(default_factory=list)
    # Floor area enclosed (m²)
    floor_area_m2: float = 0.0
    # Apse waypoints subset (for chancel-light positioning)
    apse_waypoints: list[tuple[float, float]] = field(default_factory=list)


def bezier_wall_path(params: BezierWallPathParams) -> BezierWallPathResult:
    """Generate the curved-wall floor-plan waypoints.

    Algorithm sketch (Sprint 4 implementer fills in):
      1. Define a base parametric ellipse with the requested diameter.
      2. Apply Bezier control-point placement to produce smooth curvature
         where curvature > 0; lerp with polygonal vertices for low curvature.
      3. Append apse waypoints if apse_depth_m > 0; ensure smooth joining
         to the main perimeter.
      4. Compute outward normals via finite difference around the perimeter.
      5. Compute enclosed floor area via the shoelace formula.

    Notes:
      - Use scipy.special.bernstein or implement the Bernstein basis directly.
      - Symmetric layouts: bilateral cathedrals have a long axis with the
        apse at one end; rotational mosques are typically dome-on-square or
        dome-on-octagon — extend the symmetry param if needed for your case.
    """
    raise NotImplementedError(
        "Sprint 4: <owner> implements bezier_wall_path. See docstring for "
        "algorithm sketch and sub-component contract."
    )
