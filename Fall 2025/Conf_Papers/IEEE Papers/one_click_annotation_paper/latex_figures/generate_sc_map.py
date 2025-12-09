#!/usr/bin/env python3
"""
Generate a cropped TikZ/LaTeX map of South Carolina with nearby NC/GA outlines,
major roads/cities/water bodies, and highlighted research/recreation sites.

The script is standalone: it pulls public GeoJSON/OSM data over HTTPS only,
uses no third-party Python packages, and writes sc_sites_map.tex in the
current working directory.
"""

import json
import math
import pathlib
import sys
import textwrap
import urllib.parse
import urllib.request
import re
import tempfile
import subprocess

# Geographic sources
STATE_URL = (
    "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
)
OVERPASS = "https://overpass-api.de/api/interpreter"

# Target area bounds (lat_min, lon_min, lat_max, lon_max)
SC_BBOX = (32.0, -83.5, 35.4, -78.2)

# Projection anchor (roughly Columbia)
LON0 = -81.0
LAT0 = 34.0

# Canvas sizing (larger width for a tighter zoom)
TARGET_WIDTH_CM = 18.5
MARGIN_CM = 0.1  # tighter margin to reduce NC/GA bleed
ZOOM_FACTOR = 1.35

# Simplification tolerances (projected units). Set to 0 for full fidelity.
SIMPLIFY_STATE_EPS = 0.0
SIMPLIFY_HIGHWAY_EPS = 0.0
SIMPLIFY_RIVER_EPS = 0.0
SIMPLIFY_LAKE_EPS = 0.0001

# Maximum number of points per drawn polyline to avoid TeX memory blowups
MAX_POINTS_PER_DRAW = 1200

# Highlighted sites requested by the user
KEY_SITES = {
    "Grice Marine Lab": "Grice Marine Laboratory, Charleston, SC",
    "Demetre Park": "Demetre Park, Charleston, SC",
    "Folly Beach": "Folly Beach, South Carolina",
    "Lake Greenwood SP": "Lake Greenwood State Park, Ninety Six, SC",
    "Lake Murray Dam": "Lake Murray Dam, Lexington, SC",
    "Lake Monticello": "Lake Monticello, South Carolina",
}

# Major city labels to keep the map readable
MAJOR_CITIES = {
    "Columbia": "Columbia, SC",
    "Charleston": "Charleston, SC",
    "Greenville": "Greenville, SC",
    "Spartanburg": "Spartanburg, SC",
    "Rock Hill": "Rock Hill, SC",
    "Florence": "Florence, SC",
    "Myrtle Beach": "Myrtle Beach, SC",
    "Sumter": "Sumter, SC",
    "Hilton Head": "Hilton Head Island, SC",
    "Anderson": "Anderson, SC",
}

# Large lakes to render as polygons
MAJOR_LAKES = [
    "Lake Marion",
    "Lake Moultrie",
    "Lake Hartwell",
    "Lake Keowee",
    "Lake Wylie",
    "Lake Wateree",
    "Lake Greenwood",
    "Lake Murray",
    "Lake Monticello",
    "Lake Jocassee",
]


# --------------------------- helpers ------------------------------------- #

def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "sc-map-generator/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)


def overpass(query: str):
    url = f"{OVERPASS}?data={urllib.parse.quote(query)}"
    return fetch_json(url)


def project(lon: float, lat: float):
    """Simple equirectangular projection centered on South Carolina."""
    rad = math.pi / 180.0
    x = (lon - LON0) * math.cos(LAT0 * rad)
    y = (lat - LAT0)
    return x, y


def bounding_box(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)


def douglas_peucker(points, eps):
    """Classic Douglas-Peucker simplification in projected units."""
    if eps <= 0:
        return points
    if len(points) < 3:
        return points

    def perp_dist(p, a, b):
        ax, ay = a
        bx, by = b
        px, py = p
        dx, dy = bx - ax, by - ay
        if dx == dy == 0:
            return math.hypot(px - ax, py - ay)
        t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
        t = max(0.0, min(1.0, t))
        projx, projy = ax + t * dx, ay + t * dy
        return math.hypot(px - projx, py - projy)

    max_dist = -1.0
    idx = -1
    start, end = points[0], points[-1]
    for i, p in enumerate(points[1:-1], 1):
        d = perp_dist(p, start, end)
        if d > max_dist:
            max_dist = d
            idx = i

    if max_dist > eps:
        left = douglas_peucker(points[: idx + 1], eps)
        right = douglas_peucker(points[idx:], eps)
        return left[:-1] + right
    return [start, end]


def path_length_km(latlon_points):
    def hav(a, b):
        R = 6371.0
        dlat = math.radians(b["lat"] - a["lat"])
        dlon = math.radians(b["lon"] - a["lon"])
        t = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(a["lat"]))
            * math.cos(math.radians(b["lat"]))
            * math.sin(dlon / 2) ** 2
        )
        return 2 * R * math.asin(math.sqrt(t))

    return sum(hav(a, b) for a, b in zip(latlon_points, latlon_points[1:]))


def latlon_to_projected(latlon_points):
    return [project(pt["lon"], pt["lat"]) for pt in latlon_points]


def to_canvas(projected_points, xmin, ymin, scale):
    return [((x - xmin) * scale + MARGIN_CM, (y - ymin) * scale + MARGIN_CM) for x, y in projected_points]


def tikz_path(points):
    # insert newlines to avoid TeX buffer overflows on extremely long paths
    return " --\n".join(f"({x:.3f},{y:.3f})" for x, y in points)


def polygon_path(rings):
    """Return tikz path string for outer + inner rings, each closed."""
    parts = []
    for ring in rings:
        parts.append(f"{tikz_path(ring)} -- cycle")
    return " ".join(parts)


def chunk_polyline(points, max_points):
    r"""Yield overlapping chunks to keep \draw paths small while continuous."""
    n = len(points)
    if n <= max_points:
        yield points
        return
    step = max_points - 1
    start = 0
    while start < n - 1:
        end = min(start + step, n - 1)
        chunk = points[start : end + 1]
        yield chunk
        start = end


# ----------------------- data collection --------------------------------- #


def load_state_polygons():
    data = fetch_json(STATE_URL)
    wanted = {"South Carolina", "North Carolina", "Georgia"}
    polys = {}
    for feat in data["features"]:
        name = feat["properties"]["name"]
        if name not in wanted:
            continue
        geom = feat["geometry"]
        if geom["type"] == "Polygon":
            rings = geom["coordinates"]
        elif geom["type"] == "MultiPolygon":
            rings = [ring for poly in geom["coordinates"] for ring in poly]
        else:
            continue
        projected = [[project(lon, lat) for lon, lat in ring] for ring in rings]
        polys[name] = projected
    return polys


def load_highways():
    lat_min, lon_min, lat_max, lon_max = SC_BBOX
    bbox = f"{lat_min},{lon_min},{lat_max},{lon_max}"
    ways = []

    # Interstates
    q_motor = f"[out:json][timeout:60];(way['highway'='motorway']['ref'~'I']({bbox}););out geom;"
    data = overpass(q_motor)
    for el in data.get("elements", []):
        geom = el.get("geometry", [])
        if len(geom) < 2:
            continue
        if path_length_km(geom) < 2.0:
            continue
        ways.append(geom)

    # Major trunks
    q_trunk = f"[out:json][timeout:60];(way['highway'='trunk']({bbox}););out geom;"
    data = overpass(q_trunk)
    for el in data.get("elements", []):
        geom = el.get("geometry", [])
        if len(geom) < 2:
            continue
        if path_length_km(geom) < 5.0:
            continue
        ways.append(geom)

    return ways


def load_rivers():
    lat_min, lon_min, lat_max, lon_max = SC_BBOX
    bbox = f"{lat_min},{lon_min},{lat_max},{lon_max}"
    q = f"[out:json][timeout:60];(way['waterway'='river']({bbox}););out geom;"
    data = overpass(q)
    rivers = []
    for el in data.get("elements", []):
        geom = el.get("geometry", [])
        if len(geom) < 2:
            continue
        if path_length_km(geom) < 15.0:
            continue
        rivers.append(geom)
    return rivers


def load_lakes():
    lat_min, lon_min, lat_max, lon_max = SC_BBOX
    bbox = f"{lat_min},{lon_min},{lat_max},{lon_max}"
    name_regex = "|".join(MAJOR_LAKES)
    q = (
        f"[out:json][timeout:60];"
        f"(relation['name'~'{name_regex}']({bbox});"
        f"way['name'~'{name_regex}']({bbox}););out geom;"
    )
    data = overpass(q)
    polygons = []

    for el in data.get("elements", []):
        if el["type"] == "relation":
            outers = []
            inners = []
            for mem in el.get("members", []):
                geom = mem.get("geometry")
                if not geom:
                    continue
                role = mem.get("role", "outer")
                if role == "inner":
                    inners.append(geom)
                else:
                    outers.append(geom)
            for outer in outers:
                polygons.append({"outer": outer, "inners": inners})
        elif el["type"] == "way" and "geometry" in el:
            polygons.append({"outer": el["geometry"], "inners": []})
    return polygons


def geocode_many(name_map):
    coords = {}
    missing = []
    for label, query in name_map.items():
        url = (
            "https://nominatim.openstreetmap.org/search?"
            + urllib.parse.urlencode({"q": query, "format": "json", "limit": 1})
        )
        try:
            data = fetch_json(url)
        except Exception as exc:  # pragma: no cover - defensive
            print(f"Geocode failed for {label}: {exc}", file=sys.stderr)
            missing.append((label, query))
            continue
        if not data:
            missing.append((label, query))
            continue
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        coords[label] = (lon, lat)

    for label, query in missing:
        fallback = overpass_centroid(query) or overpass_centroid(label)
        if fallback:
            coords[label] = fallback
        else:
            print(f"No result for {label}", file=sys.stderr)
    return coords


def overpass_centroid(name: str):
    lat_min, lon_min, lat_max, lon_max = SC_BBOX
    bbox = f"{lat_min},{lon_min},{lat_max},{lon_max}"
    base = name.split(",")[0].strip()
    pattern = re.escape(base)
    q = (
        f"[out:json][timeout:25];"
        f"(node['name'~\"{pattern}\"]({bbox});"
        f"way['name'~\"{pattern}\"]({bbox});"
        f"relation['name'~\"{pattern}\"]({bbox}););"
        f"out center 1;"
    )
    try:
        data = overpass(q)
    except Exception:
        return None
    for el in data.get("elements", []):
        if "center" in el:
            return el["center"]["lon"], el["center"]["lat"]
        if "lon" in el and "lat" in el:
            return el["lon"], el["lat"]
    return None


# ----------------------- external preprocessing --------------------------- #


def check_mapshaper():
    try:
        subprocess.run(
            ["npx", "--yes", "mapshaper", "-version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        return False


def write_geojson(features, path):
    obj = {"type": "FeatureCollection", "features": features}
    pathlib.Path(path).write_text(json.dumps(obj), encoding="utf-8")


def preprocess_with_mapshaper(states):
    """Use mapshaper (npx) to clip & simplify with topology preservation."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="scmap_"))
    # Boundary for clipping
    sc_lonlat = states_raw_lonlat("South Carolina")
    geom_type = "Polygon" if len(sc_lonlat) == 1 else "MultiPolygon"
    coords = sc_lonlat if geom_type == "MultiPolygon" else sc_lonlat
    if geom_type == "MultiPolygon":
        coords = [[ring] for ring in sc_lonlat]
    sc_feature = {
        "type": "Feature",
        "properties": {"name": "South Carolina"},
        "geometry": {"type": geom_type, "coordinates": coords},
    }
    write_geojson([sc_feature], tmp / "sc.json")

    # Highways
    hw_features = []
    for geom in load_highways():
        coords = [[p["lon"], p["lat"]] for p in geom]
        hw_features.append({"type": "Feature", "properties": {}, "geometry": {"type": "LineString", "coordinates": coords}})
    write_geojson(hw_features, tmp / "roads_raw.json")

    # Rivers
    rv_features = []
    for geom in load_rivers():
        coords = [[p["lon"], p["lat"]] for p in geom]
        rv_features.append({"type": "Feature", "properties": {}, "geometry": {"type": "LineString", "coordinates": coords}})
    write_geojson(rv_features, tmp / "rivers_raw.json")

    # Lakes
    lk_features = []
    for poly in load_lakes():
        outer = [[pt["lon"], pt["lat"]] for pt in poly["outer"]]
        inners = [[[pt["lon"], pt["lat"]] for pt in ring] for ring in poly["inners"]]
        lk_features.append(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {"type": "Polygon", "coordinates": [outer] + inners},
            }
        )
    write_geojson(lk_features, tmp / "lakes_raw.json")

    # Run mapshaper pipelines
    run_ms(["-i", tmp / "roads_raw.json", "-clip", tmp / "sc.json", "-simplify", "3%", "keep-shapes", "-o", tmp / "roads.json"])
    run_ms(["-i", tmp / "rivers_raw.json", "-clip", tmp / "sc.json", "-simplify", "3%", "keep-shapes", "-o", tmp / "rivers.json"])
    run_ms(["-i", tmp / "lakes_raw.json", "-clip", tmp / "sc.json", "-simplify", "2%", "keep-shapes", "-o", tmp / "lakes.json"])

    roads = read_lines(tmp / "roads.json")
    rivers = read_lines(tmp / "rivers.json")
    lakes = read_polygons(tmp / "lakes.json")
    return roads, rivers, lakes


def run_ms(args):
    cmd = ["npx", "--yes", "mapshaper"] + [str(a) for a in args]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"mapshaper failed: {' '.join(cmd)}\n{e.stderr.decode(errors='ignore')}\n")
        raise


def read_geojson(path):
    return json.loads(pathlib.Path(path).read_text())


def read_lines(path):
    data = read_geojson(path)
    lines = []
    if data.get("type") == "GeometryCollection":
        geoms = data.get("geometries", [])
    else:
        geoms = [feat.get("geometry", {}) for feat in data.get("features", [])]
    for geom in geoms:
        if geom.get("type") == "LineString":
            lines.append(geom["coordinates"])
        elif geom.get("type") == "MultiLineString":
            lines.extend(geom["coordinates"])
    return lines


def read_polygons(path):
    data = read_geojson(path)
    polys = []
    if data.get("type") == "GeometryCollection":
        geoms = data.get("geometries", [])
    else:
        geoms = [feat.get("geometry", {}) for feat in data.get("features", [])]
    for geom in geoms:
        if geom.get("type") == "Polygon":
            coords = geom["coordinates"]
            outer, inners = coords[0], coords[1:]
            polys.append((outer, inners))
        elif geom.get("type") == "MultiPolygon":
            for poly in geom["coordinates"]:
                outer, inners = poly[0], poly[1:]
                polys.append((outer, inners))
    return polys


def states_raw_lonlat(name):
    data = fetch_json(STATE_URL)
    for feat in data["features"]:
        if feat["properties"]["name"] == name:
            geom = feat["geometry"]
            if geom["type"] == "Polygon":
                rings = []
                for ring in geom["coordinates"]:
                    if ring[0] != ring[-1]:
                        ring = ring + [ring[0]]
                    rings.append(ring)
                return rings
            elif geom["type"] == "MultiPolygon":
                rings = []
                for poly in geom["coordinates"]:
                    for ring in poly:
                        if ring[0] != ring[-1]:
                            ring = ring + [ring[0]]
                        rings.append(ring)
                return rings
    raise RuntimeError("State boundary not found")


# ----------------------- rendering pipeline ------------------------------ #


def main():
    mapshaper_ok = check_mapshaper()
    states = load_state_polygons()

    sc_polys = states["South Carolina"]
    sc_points = [pt for ring in sc_polys for pt in ring]
    xmin, xmax, ymin, ymax = bounding_box(sc_points)

    width = xmax - xmin
    scale = TARGET_WIDTH_CM / width * ZOOM_FACTOR
    height_cm = (ymax - ymin) * scale + 2 * MARGIN_CM
    width_cm = TARGET_WIDTH_CM * ZOOM_FACTOR + 2 * MARGIN_CM

    # Clip rectangle for TikZ
    clip_rect = (0, 0, width_cm, height_cm)

    # Transform state outlines
    state_paths = {}
    for name, rings in states.items():
        transformed = []
        for ring in rings:
            ring_closed = ring if ring[0] == ring[-1] else ring + [ring[0]]
            simplified = douglas_peucker(ring_closed, eps=SIMPLIFY_STATE_EPS)
            projected = to_canvas(simplified, xmin, ymin, scale)
            transformed.append(projected)
        state_paths[name] = transformed

    if mapshaper_ok:
        highways_ll, rivers_ll, lakes_ll = preprocess_with_mapshaper(states)
        highways = [to_canvas(latlon_to_projected([{"lon": x, "lat": y} for x, y in line]), xmin, ymin, scale) for line in highways_ll]
        rivers = [to_canvas(latlon_to_projected([{"lon": x, "lat": y} for x, y in line]), xmin, ymin, scale) for line in rivers_ll]
        lakes = []
        for outer, inners in lakes_ll:
            oproj = latlon_to_projected([{"lon": x, "lat": y} for x, y in outer])
            oc = to_canvas(oproj, xmin, ymin, scale)
            inn_canvas = []
            for inner in inners:
                iproj = latlon_to_projected([{"lon": x, "lat": y} for x, y in inner])
                inn_canvas.append(to_canvas(iproj, xmin, ymin, scale))
            lakes.append({"outer": oc, "inners": inn_canvas})
    else:
        # Highways
        highways = []
        for geom in load_highways():
            proj = latlon_to_projected(geom)
            simplified = douglas_peucker(proj, eps=SIMPLIFY_HIGHWAY_EPS)
            highways.append(to_canvas(simplified, xmin, ymin, scale))

        # Rivers
        rivers = []
        for geom in load_rivers():
            proj = latlon_to_projected(geom)
            simplified = douglas_peucker(proj, eps=SIMPLIFY_RIVER_EPS)
            rivers.append(to_canvas(simplified, xmin, ymin, scale))

        # Lakes
        lakes = []
        for poly in load_lakes():
            outer_proj = latlon_to_projected(poly["outer"])
            outer_ring = outer_proj if outer_proj[0] == outer_proj[-1] else outer_proj + [outer_proj[0]]
            outer_simpl = douglas_peucker(outer_ring, eps=SIMPLIFY_LAKE_EPS)
            outer_canvas = to_canvas(outer_simpl, xmin, ymin, scale)

            inner_canvas = []
            for inner in poly["inners"]:
                iproj = latlon_to_projected(inner)
                iring = iproj if iproj[0] == iproj[-1] else iproj + [iproj[0]]
                isimpl = douglas_peucker(iring, eps=SIMPLIFY_LAKE_EPS)
                inner_canvas.append(to_canvas(isimpl, xmin, ymin, scale))

            lakes.append({"outer": outer_canvas, "inners": inner_canvas})

    # Cities and key sites
    city_coords = geocode_many(MAJOR_CITIES)
    key_coords = geocode_many(KEY_SITES)

    cities_canvas = {
        name: to_canvas([project(lon, lat)], xmin, ymin, scale)[0]
        for name, (lon, lat) in city_coords.items()
    }
    keys_canvas = {
        name: to_canvas([project(lon, lat)], xmin, ymin, scale)[0]
        for name, (lon, lat) in key_coords.items()
    }

    # Write LaTeX
    tex = render_tex(
        clip_rect,
        state_paths,
        highways,
        rivers,
        lakes,
        cities_canvas,
        keys_canvas,
    )
    pathlib.Path("sc_sites_map.tex").write_text(tex, encoding="utf-8")


def render_tex(
    clip_rect,
    state_paths,
    highways,
    rivers,
    lakes,
    cities,
    keys,
):
    xmin, ymin, xmax, ymax = clip_rect

    def draw_paths(paths, style, fill=False):
        lines = []
        for path in paths:
            cmd = "\\filldraw" if fill else "\\draw"
            if fill:
                lines.append(f"{cmd}[{style}] {tikz_path(path)};")
            else:
                for seg in chunk_polyline(path, MAX_POINTS_PER_DRAW):
                    lines.append(f"{cmd}[{style}] {tikz_path(seg)};")
        return "\n".join(lines)

    def draw_lakes(polygons):
        lines = []
        for poly in polygons:
            lines.append(f"\\filldraw[fill=white, draw=black, line width=0.2pt] {tikz_path(poly['outer'])} -- cycle;")
            for inner in poly["inners"]:
                lines.append(f"\\filldraw[fill=white, draw=black, line width=0.1pt] {tikz_path(inner)} -- cycle;")
        return "\n".join(lines)

    sc_paths = state_paths["South Carolina"]
    # Choose a clip ring for SC (longest ring)
    sc_clip_ring = max(sc_paths, key=len)

    tex_body = textwrap.dedent(
        f"""
        \\documentclass[tikz,border=2pt]{{standalone}}
        \\usepackage{{tikz}}
        \\usetikzlibrary{{shapes.geometric,positioning}}
        \\definecolor{{river}}{{HTML}}{{1E88E5}}
        \\begin{{document}}
        \\begin{{tikzpicture}}[line join=round, line cap=round, x=1cm, y=1cm]
            % Clip everything else to South Carolina boundary
            \\begin{{scope}}
                \\clip {tikz_path(sc_clip_ring)} -- cycle;
                \\fill[white] ({xmin:.3f},{ymin:.3f}) rectangle ({xmax:.3f},{ymax:.3f});

                % Lakes with islands restored
                {draw_lakes(lakes)}

                % Rivers
                {draw_paths(rivers, "line width=0.35pt, draw=river")}

                % Highways
                {draw_paths(highways, "line width=0.55pt, draw=black")}
            \\end{{scope}}

            % South Carolina border on top
            {draw_paths(sc_paths, "line width=0.8pt, draw=black")}

            % City markers
    """
    )

    # Add city nodes
    city_lines = []
    for name, (x, y) in cities.items():
        city_lines.append(
            f"\\fill[black] ({x:.3f},{y:.3f}) circle (1.4pt);"
            f"\\node[anchor=west, font=\\scriptsize, inner sep=1pt] at ({x+0.08:.3f},{y+0.02:.3f}) {{{name}}};"
        )

    # Key site markers (no labels)
    key_lines = []
    for _, (x, y) in keys.items():
        key_lines.append(
            f"\\draw[black, line width=0.2pt, fill=black] ({x:.3f},{y:.3f}) node[star, star points=5, star point ratio=2.25, draw=black, fill=black, minimum size=0.8pt] {{}};"
        )

    footer = textwrap.dedent(
        """
            % City labels
        """
        + "\n".join(city_lines)
        + "\n            % Highlighted sites\n"
        + "\n".join(key_lines)
        + """
        \\end{tikzpicture}
        \\end{document}
        """
    )
    return tex_body + footer


if __name__ == "__main__":
    main()
