"""
3D Rendering Engine
Generates 3D models and visualizations with proper scaling
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class Point3D:
    """3D point"""
    x: float
    y: float
    z: float


@dataclass
class Face3D:
    """3D triangular face"""
    vertices: List[Point3D]
    normal: Optional[Point3D] = None
    color: Tuple[int, int, int] = (200, 200, 200)


class Renderer3D:
    """
    3D rendering engine for terrain models, buildings, and infrastructure.
    Generates scaled 3D models for visualization.
    """
    
    def __init__(self):
        self.vertices: List[Point3D] = []
        self.faces: List[Face3D] = []
        self.meshes: Dict[str, List] = {}
        
    def add_vertex(self, x: float, y: float, z: float) -> int:
        """
        Add a vertex and return its index.
        
        Args:
            x, y, z: Coordinates
            
        Returns:
            Index of the added vertex
        """
        vertex = Point3D(x, y, z)
        self.vertices.append(vertex)
        return len(self.vertices) - 1
    
    def add_face(self, vertex_indices: List[int], color: Tuple[int, int, int] = (200, 200, 200)):
        """
        Add a triangular face.
        
        Args:
            vertex_indices: List of 3 vertex indices
            color: RGB color tuple
        """
        if len(vertex_indices) != 3:
            raise ValueError("Face must have exactly 3 vertices")
        
        vertices = [self.vertices[i] for i in vertex_indices]
        face = Face3D(vertices=vertices, color=color)
        face.normal = self._calculate_normal(vertices)
        self.faces.append(face)
    
    def _calculate_normal(self, vertices: List[Point3D]) -> Point3D:
        """Calculate face normal vector"""
        if len(vertices) < 3:
            return Point3D(0, 0, 1)
        
        v1 = vertices[1]
        v0 = vertices[0]
        v2 = vertices[2]
        
        # Calculate vectors
        u = Point3D(v1.x - v0.x, v1.y - v0.y, v1.z - v0.z)
        v = Point3D(v2.x - v0.x, v2.y - v0.y, v2.z - v0.z)
        
        # Cross product
        normal = Point3D(
            u.y * v.z - u.z * v.y,
            u.z * v.x - u.x * v.z,
            u.x * v.y - u.y * v.x,
        )
        
        # Normalize
        length = (normal.x**2 + normal.y**2 + normal.z**2)**0.5
        if length > 0:
            normal = Point3D(
                normal.x / length,
                normal.y / length,
                normal.z / length,
            )
        
        return normal
    
    def create_terrain_from_elevation_grid(
        self,
        elevation_grid: List[List[float]],
        grid_spacing: float = 10.0,
        base_elevation: float = 0.0
    ) -> str:
        """
        Create 3D terrain mesh from elevation grid.
        
        Args:
            elevation_grid: 2D array of elevation values
            grid_spacing: Distance between grid points
            base_elevation: Base elevation offset
            
        Returns:
            Mesh identifier
        """
        mesh_id = "terrain"
        mesh_vertices = []
        
        rows = len(elevation_grid)
        cols = len(elevation_grid[0]) if rows > 0 else 0
        
        # Create vertices
        vertex_map = {}
        for i in range(rows):
            for j in range(cols):
                x = j * grid_spacing
                y = i * grid_spacing
                z = elevation_grid[i][j] + base_elevation
                
                idx = self.add_vertex(x, y, z)
                vertex_map[(i, j)] = idx
                mesh_vertices.append(idx)
        
        # Create faces (two triangles per grid cell)
        for i in range(rows - 1):
            for j in range(cols - 1):
                # Get vertex indices for the four corners of this cell
                v1 = vertex_map[(i, j)]
                v2 = vertex_map[(i, j + 1)]
                v3 = vertex_map[(i + 1, j + 1)]
                v4 = vertex_map[(i + 1, j)]
                
                # Create two triangles
                self.add_face([v1, v2, v3], color=(139, 90, 43))  # Brown for terrain
                self.add_face([v1, v3, v4], color=(139, 90, 43))
        
        self.meshes[mesh_id] = mesh_vertices
        return mesh_id
    
    def create_building(
        self,
        footprint: List[Tuple[float, float]],
        base_elevation: float,
        height: float,
        color: Tuple[int, int, int] = (200, 200, 200)
    ) -> str:
        """
        Create 3D building from footprint.
        
        Args:
            footprint: List of (x, y) coordinates for building footprint
            base_elevation: Ground elevation
            height: Building height
            color: RGB color
            
        Returns:
            Mesh identifier
        """
        mesh_id = f"building_{len(self.meshes)}"
        mesh_vertices = []
        
        # Create bottom vertices
        bottom_indices = []
        for x, y in footprint:
            idx = self.add_vertex(x, y, base_elevation)
            bottom_indices.append(idx)
            mesh_vertices.append(idx)
        
        # Create top vertices
        top_indices = []
        for x, y in footprint:
            idx = self.add_vertex(x, y, base_elevation + height)
            top_indices.append(idx)
            mesh_vertices.append(idx)
        
        # Create wall faces
        n = len(footprint)
        for i in range(n):
            next_i = (i + 1) % n
            
            # Two triangles for each wall segment
            self.add_face(
                [bottom_indices[i], bottom_indices[next_i], top_indices[next_i]],
                color=color
            )
            self.add_face(
                [bottom_indices[i], top_indices[next_i], top_indices[i]],
                color=color
            )
        
        # Create roof (simplified flat roof)
        if n >= 3:
            # Triangulate roof
            for i in range(1, n - 1):
                self.add_face(
                    [top_indices[0], top_indices[i], top_indices[i + 1]],
                    color=color
                )
        
        self.meshes[mesh_id] = mesh_vertices
        return mesh_id
    
    def create_lot_boundary(
        self,
        corners: List[Tuple[float, float]],
        elevation: float,
        height: float = 1.0
    ) -> str:
        """
        Create 3D lot boundary markers.
        
        Args:
            corners: Lot corner coordinates
            elevation: Ground elevation
            height: Marker height
            
        Returns:
            Mesh identifier
        """
        mesh_id = f"lot_boundary_{len(self.meshes)}"
        
        # Create vertical posts at each corner
        for x, y in corners:
            # Simple post (small square)
            post_size = 0.5
            footprint = [
                (x - post_size, y - post_size),
                (x + post_size, y - post_size),
                (x + post_size, y + post_size),
                (x - post_size, y + post_size),
            ]
            
            self.create_building(
                footprint,
                elevation,
                height,
                color=(255, 255, 0)  # Yellow markers
            )
        
        self.meshes[mesh_id] = []
        return mesh_id
    
    def create_road(
        self,
        centerline: List[Tuple[float, float]],
        elevation_profile: List[float],
        width: float,
        thickness: float = 0.5
    ) -> str:
        """
        Create 3D road model.
        
        Args:
            centerline: Road centerline points
            elevation_profile: Elevation at each centerline point
            width: Road width
            thickness: Pavement thickness
            
        Returns:
            Mesh identifier
        """
        mesh_id = f"road_{len(self.meshes)}"
        mesh_vertices = []
        
        # Create road surface vertices
        for i, ((x, y), elev) in enumerate(zip(centerline, elevation_profile)):
            # Left edge
            idx1 = self.add_vertex(x - width/2, y, elev)
            # Right edge
            idx2 = self.add_vertex(x + width/2, y, elev)
            mesh_vertices.extend([idx1, idx2])
            
            # Create faces connecting to previous segment
            if i > 0:
                prev_left = mesh_vertices[(i-1) * 2]
                prev_right = mesh_vertices[(i-1) * 2 + 1]
                curr_left = idx1
                curr_right = idx2
                
                # Top surface (two triangles)
                self.add_face(
                    [prev_left, curr_left, curr_right],
                    color=(50, 50, 50)  # Dark gray asphalt
                )
                self.add_face(
                    [prev_left, curr_right, prev_right],
                    color=(50, 50, 50)
                )
        
        self.meshes[mesh_id] = mesh_vertices
        return mesh_id
    
    def export_to_obj(self, filename: str) -> str:
        """
        Export model to OBJ format.
        
        Args:
            filename: Output filename
            
        Returns:
            Success message
        """
        with open(filename, 'w') as f:
            f.write("# BID-ZONE 3D Model Export\n\n")
            
            # Write vertices
            for v in self.vertices:
                f.write(f"v {v.x} {v.y} {v.z}\n")
            
            f.write("\n")
            
            # Write faces (OBJ uses 1-based indexing)
            for face in self.faces:
                indices = [self.vertices.index(v) + 1 for v in face.vertices]
                f.write(f"f {' '.join(map(str, indices))}\n")
        
        return f"3D model exported to {filename}"
    
    def export_to_json(self, filename: str) -> str:
        """
        Export model to JSON format.
        
        Args:
            filename: Output filename
            
        Returns:
            Success message
        """
        data = {
            "vertices": [
                {"x": v.x, "y": v.y, "z": v.z}
                for v in self.vertices
            ],
            "faces": [
                {
                    "vertices": [
                        {"x": v.x, "y": v.y, "z": v.z}
                        for v in face.vertices
                    ],
                    "color": face.color,
                }
                for face in self.faces
            ],
            "meshes": {
                name: indices
                for name, indices in self.meshes.items()
            },
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return f"3D model exported to {filename}"
    
    def get_statistics(self) -> Dict:
        """Get model statistics"""
        return {
            "vertex_count": len(self.vertices),
            "face_count": len(self.faces),
            "mesh_count": len(self.meshes),
            "bounds": self._calculate_bounds(),
        }
    
    def _calculate_bounds(self) -> Dict:
        """Calculate model bounding box"""
        if not self.vertices:
            return {
                "min": {"x": 0, "y": 0, "z": 0},
                "max": {"x": 0, "y": 0, "z": 0},
            }
        
        min_x = min(v.x for v in self.vertices)
        max_x = max(v.x for v in self.vertices)
        min_y = min(v.y for v in self.vertices)
        max_y = max(v.y for v in self.vertices)
        min_z = min(v.z for v in self.vertices)
        max_z = max(v.z for v in self.vertices)
        
        return {
            "min": {"x": min_x, "y": min_y, "z": min_z},
            "max": {"x": max_x, "y": max_y, "z": max_z},
        }
