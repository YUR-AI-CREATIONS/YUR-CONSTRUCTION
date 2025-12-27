"""
2D Rendering Engine
Generates 2D plans and layouts with proper scaling
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class Point2D:
    """2D point"""
    x: float
    y: float


@dataclass
class Line2D:
    """2D line"""
    start: Point2D
    end: Point2D
    layer: str
    color: str


class Renderer2D:
    """
    2D rendering engine for construction plans and land layouts.
    Generates scaled drawings similar to AutoCAD output.
    """
    
    def __init__(self, scale: str = "1:100"):
        self.scale = scale
        self.elements: List[Line2D] = []
        self.layers: Dict[str, Dict] = {}
        self.bounds: Optional[Dict] = None
        
    def set_scale(self, scale: str):
        """Set drawing scale (e.g., '1:100', '1:50')"""
        self.scale = scale
    
    def add_layer(self, name: str, color: str = "white", line_weight: float = 0.5):
        """Add a drawing layer"""
        self.layers[name] = {
            "name": name,
            "color": color,
            "line_weight": line_weight,
            "visible": True,
        }
    
    def draw_line(self, start: Tuple[float, float], end: Tuple[float, float], layer: str = "0"):
        """Draw a line"""
        line = Line2D(
            start=Point2D(*start),
            end=Point2D(*end),
            layer=layer,
            color=self.layers.get(layer, {}).get("color", "white"),
        )
        self.elements.append(line)
    
    def draw_polyline(self, points: List[Tuple[float, float]], layer: str = "0", closed: bool = False):
        """Draw a polyline (connected lines)"""
        for i in range(len(points) - 1):
            self.draw_line(points[i], points[i + 1], layer)
        
        if closed and len(points) > 2:
            self.draw_line(points[-1], points[0], layer)
    
    def draw_rectangle(self, corner1: Tuple[float, float], corner2: Tuple[float, float], layer: str = "0"):
        """Draw a rectangle"""
        x1, y1 = corner1
        x2, y2 = corner2
        
        points = [
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
        ]
        
        self.draw_polyline(points, layer, closed=True)
    
    def draw_lot(self, lot_number: int, corners: List[Tuple[float, float]], dimensions: Dict):
        """
        Draw a development lot with dimensions.
        
        Args:
            lot_number: Lot identification number
            corners: List of (x, y) corner coordinates
            dimensions: Dict with 'width', 'depth', 'area'
        """
        # Draw lot boundary
        self.draw_polyline(corners, layer="LOT_LINES", closed=True)
        
        # Calculate centroid for label placement
        centroid_x = sum(p[0] for p in corners) / len(corners)
        centroid_y = sum(p[1] for p in corners) / len(corners)
        
        # Add lot number annotation (stored as metadata)
        self._add_annotation(
            f"LOT {lot_number}",
            (centroid_x, centroid_y),
            layer="LOT_LABELS"
        )
    
    def draw_road(self, centerline: List[Tuple[float, float]], width: float, name: str):
        """
        Draw a road with proper width.
        
        Args:
            centerline: List of centerline points
            width: Road width
            name: Road name
        """
        # Draw centerline
        self.draw_polyline(centerline, layer="ROAD_CENTERLINE")
        
        # Draw road edges (simplified - actual would calculate perpendiculars)
        for point in centerline:
            # Draw road edge indicators
            self.draw_line(
                (point[0] - width/2, point[1]),
                (point[0] + width/2, point[1]),
                layer="ROAD_EDGE"
            )
    
    def draw_utility_line(self, path: List[Tuple[float, float]], utility_type: str):
        """
        Draw utility lines (water, sewer, electric, etc.)
        
        Args:
            path: Line path points
            utility_type: Type of utility (water, sewer, electric, gas, etc.)
        """
        layer_map = {
            "water": "UTILITY_WATER",
            "sewer": "UTILITY_SEWER",
            "electric": "UTILITY_ELECTRIC",
            "gas": "UTILITY_GAS",
            "storm": "UTILITY_STORM",
        }
        
        layer = layer_map.get(utility_type.lower(), "UTILITY_MISC")
        self.draw_polyline(path, layer=layer)
    
    def draw_contour(self, elevation: float, path: List[Tuple[float, float]]):
        """
        Draw contour line.
        
        Args:
            elevation: Elevation of contour
            path: Contour line path
        """
        self.draw_polyline(path, layer="CONTOURS")
        
        # Add elevation label
        if path:
            mid_point = path[len(path) // 2]
            self._add_annotation(f"{elevation}'", mid_point, layer="CONTOUR_LABELS")
    
    def _add_annotation(self, text: str, position: Tuple[float, float], layer: str = "TEXT"):
        """Add text annotation (stored as metadata)"""
        # In a real implementation, this would create text entities
        pass
    
    def generate_site_plan(
        self,
        site_boundary: List[Tuple[float, float]],
        lots: List[Dict],
        roads: List[Dict],
        utilities: List[Dict]
    ) -> Dict:
        """
        Generate complete 2D site plan.
        
        Args:
            site_boundary: Site boundary coordinates
            lots: List of lot definitions
            roads: List of road definitions
            utilities: List of utility line definitions
            
        Returns:
            Dict with drawing data
        """
        # Set up layers
        self.add_layer("SITE_BOUNDARY", color="red", line_weight=1.0)
        self.add_layer("LOT_LINES", color="cyan", line_weight=0.5)
        self.add_layer("LOT_LABELS", color="white", line_weight=0.3)
        self.add_layer("ROAD_CENTERLINE", color="yellow", line_weight=0.7)
        self.add_layer("ROAD_EDGE", color="white", line_weight=0.5)
        self.add_layer("UTILITY_WATER", color="blue", line_weight=0.4)
        self.add_layer("UTILITY_SEWER", color="green", line_weight=0.4)
        self.add_layer("UTILITY_STORM", color="cyan", line_weight=0.4)
        
        # Draw site boundary
        self.draw_polyline(site_boundary, layer="SITE_BOUNDARY", closed=True)
        
        # Draw lots
        for lot in lots:
            self.draw_lot(
                lot["lot_number"],
                lot["corners"],
                lot["dimensions"]
            )
        
        # Draw roads
        for road in roads:
            self.draw_road(
                road["centerline"],
                road["width"],
                road["name"]
            )
        
        # Draw utilities
        for utility in utilities:
            self.draw_utility_line(
                utility["path"],
                utility["type"]
            )
        
        return self.export_drawing()
    
    def export_drawing(self) -> Dict:
        """
        Export drawing data.
        
        Returns:
            Dict containing all drawing elements
        """
        return {
            "scale": self.scale,
            "layers": self.layers,
            "element_count": len(self.elements),
            "elements": [
                {
                    "type": "line",
                    "start": {"x": elem.start.x, "y": elem.start.y},
                    "end": {"x": elem.end.x, "y": elem.end.y},
                    "layer": elem.layer,
                    "color": elem.color,
                }
                for elem in self.elements
            ],
            "bounds": self._calculate_bounds(),
        }
    
    def _calculate_bounds(self) -> Dict:
        """Calculate drawing bounds"""
        if not self.elements:
            return {"min_x": 0, "min_y": 0, "max_x": 0, "max_y": 0}
        
        all_x = [elem.start.x for elem in self.elements] + [elem.end.x for elem in self.elements]
        all_y = [elem.start.y for elem in self.elements] + [elem.end.y for elem in self.elements]
        
        return {
            "min_x": min(all_x),
            "min_y": min(all_y),
            "max_x": max(all_x),
            "max_y": max(all_y),
        }
    
    def export_to_dxf(self, filename: str) -> str:
        """
        Export drawing to DXF format (placeholder).
        
        Args:
            filename: Output filename
            
        Returns:
            Success message
        """
        # In production, this would use ezdxf library
        data = self.export_drawing()
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return f"Drawing exported to {filename}"
    
    def export_to_svg(self, filename: str) -> str:
        """
        Export drawing to SVG format.
        
        Args:
            filename: Output filename
            
        Returns:
            Success message
        """
        bounds = self._calculate_bounds()
        width = bounds["max_x"] - bounds["min_x"]
        height = bounds["max_y"] - bounds["min_y"]
        
        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
"""
        
        # Add lines
        for elem in self.elements:
            svg += f'  <line x1="{elem.start.x}" y1="{elem.start.y}" '
            svg += f'x2="{elem.end.x}" y2="{elem.end.y}" '
            svg += f'stroke="{elem.color}" stroke-width="1" />\n'
        
        svg += "</svg>"
        
        with open(filename, 'w') as f:
            f.write(svg)
        
        return f"Drawing exported to {filename}"
