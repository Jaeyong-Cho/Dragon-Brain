# Computer Graphics

Computer graphics creates and manipulates visual content using computers.

## Graphics Pipeline

The process of rendering 3D scenes to 2D images:

### 1. Application Stage

CPU-based processing:

- **Scene management**: Object culling
- **Animation**: Update transformations
- **Physics**: Collision detection
- **AI**: Behavior logic

### 2. Geometry Stage

Transform 3D objects to screen space:

#### Vertex Processing

Transform vertices using matrices:

- **Model Matrix**: Object to world space
- **View Matrix**: World to camera space
- **Projection Matrix**: 3D to 2D

```glsl
// Vertex shader
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(position, 1.0);
}
```

#### Primitive Assembly

Connect vertices into primitives:

- Triangles
- Lines
- Points

#### Clipping

Remove geometry outside view frustum.

### 3. Rasterization Stage

Convert primitives to pixels:

- **Fragment Generation**: Create fragments
- **Interpolation**: Interpolate vertex attributes
- **Depth Testing**: Determine visibility

### 4. Fragment/Pixel Stage

Determine final pixel colors:

```glsl
// Fragment shader
void main() {
    vec3 color = texture(diffuseMap, texCoord).rgb;
    vec3 normal = normalize(fragNormal);
    vec3 lightDir = normalize(lightPos - fragPos);
    
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor * color;
    
    FragColor = vec4(diffuse, 1.0);
}
```

## Lighting Models

### Phong Reflection Model

**Three components**:

- **Ambient**: Constant base illumination
- **Diffuse**: Matte surface reflection
- **Specular**: Shiny highlights

### Physically Based Rendering (PBR)

More realistic lighting:

- **Metallic**: Metal vs dielectric
- **Roughness**: Surface smoothness
- **Energy conservation**
- **Fresnel effect**

### Global Illumination

Account for indirect lighting:

- **Ray Tracing**: Simulate light paths
- **Path Tracing**: Monte Carlo sampling
- **Radiosity**: Surface-to-surface

## Texturing

### Texture Mapping

Apply 2D images to 3D surfaces:

- **UV Coordinates**: 2D mapping
- **Mipmapping**: Level of detail
- **Filtering**: Bilinear, trilinear, anisotropic

### Advanced Texturing

- **Normal Mapping**: Fake surface detail
- **Displacement Mapping**: Actual geometry
- **Ambient Occlusion**: Crevice darkening
- **Roughness Maps**: Surface variation

## Shaders

Programs running on GPU:

### Shader Types

- **Vertex Shader**: Process vertices
- **Fragment/Pixel Shader**: Process pixels
- **Geometry Shader**: Generate geometry
- **Compute Shader**: General computation
- **Tessellation Shader**: Subdivide geometry

### Shading Languages

- **GLSL**: OpenGL Shading Language
- **HLSL**: DirectX High-Level Shading Language
- **MSL**: Metal Shading Language

## 3D Transformations

### Translation

Move objects in space:

```
T = [1  0  0  tx]
    [0  1  0  ty]
    [0  0  1  tz]
    [0  0  0   1]
```

### Rotation

Rotate around axes:

- Euler angles
- **Quaternions**: Avoid gimbal lock

### Scaling

Change object size:

- Uniform scaling
- Non-uniform scaling

## Rendering Techniques

### Forward Rendering

Render each object with all lights:

- Simple
- **Multiple light passes**
- Good for few lights

### Deferred Rendering

Separate geometry and lighting:

- **G-Buffer**: Store geometry data
- Lighting in screen space
- Efficient for many lights

### Real-Time Ray Tracing

Hardware-accelerated ray tracing:

- **NVIDIA RTX**: Ray tracing cores
- Accurate reflections
- Realistic shadows
- Global illumination

## Anti-Aliasing

Reduce jagged edges:

### MSAA (Multi-Sample Anti-Aliasing)

Sample multiple points per pixel.

### FXAA (Fast Approximate Anti-Aliasing)

**Post-processing** technique.

### TAA (Temporal Anti-Aliasing)

Use previous frames for smoothing.

## Optimization Techniques

### Level of Detail (LOD)

Use simpler models at distance:

- **Fewer polygons**
- Lower resolution textures
- Simplified shaders

### Culling

Remove invisible objects:

- **Frustum Culling**: Outside view
- **Occlusion Culling**: Behind objects
- **Backface Culling**: Facing away

### Batching

Reduce draw calls:

- Static batching
- **Dynamic batching**
- Instancing

## Computer Vision

### Image Processing

- **Filtering**: Blur, sharpen
- **Edge Detection**: Sobel, Canny
- **Morphological Operations**: Dilation, erosion
- **Color Space Conversion**: RGB, HSV

### Feature Detection

- **SIFT**: Scale-Invariant Feature Transform
- **SURF**: Speeded Up Robust Features
- **ORB**: Oriented FAST and Rotated BRIEF

### Object Recognition

- Template matching
- **Deep learning**: CNNs
- YOLO: Real-time detection

## Animation

### Keyframe Animation

Define key poses, interpolate between:

- Linear interpolation
- **Bezier curves**
- Spline interpolation

### Skeletal Animation

Bones and skinning:

- **Rigging**: Create skeleton
- **Skinning**: Attach mesh to bones
- Inverse Kinematics (IK)

### Procedural Animation

Generate motion algorithmically:

- Particle systems
- **Physics simulation**
- Crowd simulation

## Graphics APIs

### OpenGL

Cross-platform graphics API:

- Widely supported
- **Open standard**
- Modern: OpenGL 4.x

### DirectX

Microsoft's graphics API:

- Windows exclusive
- **DirectX 12**: Low-level control
- Ray tracing support

### Vulkan

Modern low-level API:

- **Explicit control**
- Better multi-threading
- Cross-platform

### Metal

Apple's graphics API:

- macOS and iOS
- Low overhead
- **Optimized for Apple hardware**

## Applications

- Video games
- **Film and animation**
- Virtual reality
- Augmented reality
- Scientific visualization
- Medical imaging
- CAD/CAM
