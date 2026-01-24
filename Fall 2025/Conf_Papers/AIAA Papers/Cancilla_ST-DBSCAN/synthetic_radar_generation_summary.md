# Synthetic Radar Data Generation for ST-DBSCAN Paper

## Repository Comparison

### 1. SyntheticRadarGeneration_Training (YOLO-focused)
**Primary Purpose**: YOLO object detection training with synthetic radar data

**Key Capabilities**:
- Generates synthetic radar CSV files by placing extracted objects on clean backgrounds
- Exports YOLO bounding box labels for object detection training
- Supports echo trail visualization for motion analysis
- Two placement modes: random and tracks (curved trajectories)

**Data Generation Process**:
```
annotation.json + land_frames/ + object_library/
    ↓
augmenter (Rust binary)
    ↓
synthetic CSVs + YOLO labels (.txt)
    ↓
generate_dataset.py
    ↓
YOLO dataset (train/val/test splits)
    ↓
PNG images + training
```

### 2. radar-sim-platform (Radar simulation-focused)
**Primary Purpose**: Portable radar simulation without raw data dependencies

**Key Capabilities**:
- Same core augmentation engine as SyntheticRadarGeneration_Training
- Pre-packaged portable data (164 land frames, 1847 objects)
- No YOLO label export in current version (missing --export-labels flag)
- Focus on visualization and video generation
- More extensive Python visualization scripts

**Data Generation Process**:
```
portable_data/
    ├── annotation.json
    ├── land_frames/ (164 CSV backgrounds)
    └── object_library/ (1847 extracted objects)
    ↓
augmenter (Rust binary)
    ↓
synthetic CSV files
    ↓
visualization scripts
    ↓
PNG images + videos
```

## Repository Structure Comparison

| Feature | SyntheticRadarGeneration_Training | radar-sim-platform |
|---------|-----------------------------------|---------------------|
| YOLO label export | ✅ Yes (--export-labels) | ❌ No |
| Track mode | ✅ Yes (curved paths) | ✅ Yes (curved paths) |
| Random mode | ✅ Yes | ✅ Yes |
| Portable data | ✅ Yes (in data/) | ✅ Yes (in portable_data/) |
| Echo trails | ✅ Yes | ✅ Yes |
| Video generation | ✅ Limited | ✅ Extensive |
| Object count | 1847 | 1847 |
| Land frames | 164 | 164 |

## Augmenter Parameters (Common to Both)

### Core Parameters
```bash
--annotation <FILE>         # Water/land region mask (JSON)
--land-frames <DIR>         # Clean background CSV files
--library <DIR>             # Extracted radar objects
--output <DIR>              # Output directory
--count <N>                 # Number of frames to generate
--seed <N>                  # Random seed for reproducibility
--mode <random|tracks>      # Placement strategy
```

### Random Mode Parameters
```bash
--objects-per-frame <N>     # Objects per frame (default: 3)
--margin <PIXELS>           # Min distance from boundary (default: 50)
```

### Tracks Mode Parameters
```bash
--num-tracks <N>            # Number of concurrent tracks (default: 3)
--curvature <0.0-1.0>       # Path curvature (default: 0.3)
--size-tolerance <0.0-1.0>  # Object size matching tolerance (default: 0.3)
```

### YOLO Label Export (SyntheticRadarGeneration_Training only)
```bash
--export-labels             # Enable YOLO label export
--label-class <ID>          # YOLO class ID: 0=buoy, 1=boat
```

## Output Formats

### 1. CSV Format (Both repositories)
- Raw radar data in FURUNO format
- Each CSV contains one radar sweep
- Format: `timestamp,unknown1,unknown2,unknown3,angle_ticks,echo1,echo2,...`
- Polar coordinates: angle_ticks (0-8191) + range bins (intensity 0-255)

### 2. YOLO Labels (.txt) (SyntheticRadarGeneration_Training only)
- Format: `<class_id> <x_center> <y_center> <width> <height>`
- Normalized coordinates (0-1)
- One line per object
- Example:
  ```
  1 0.5208 0.2880 0.0097 0.0058  # boat at x=52%, y=29%
  1 0.5417 0.2419 0.0153 0.0092  # boat at x=54%, y=24%
  ```

### 3. PNG Images (via conversion scripts)
- Polar-to-Cartesian conversion
- Colormap visualization (turbo, viridis, etc.)
- Echo trail overlays (motion history)
- Size: configurable (default 1735x1735)

### 4. Object Library Format (JSON)
```json
{
  "id": "uuid-string",
  "category": "water_object",
  "echo_data": [[...], [...], ...],  // 2D intensity array (pulse × range)
  "angular_extent": 0.0524,            // radians
  "range_extent": 10,                  // bins
  "area": 34,                          // non-zero pixels
  "mean_intensity": 68.3,
  "max_intensity": 212,
  "source_timestamp": "...",
  "created_at": "...",
  "tags": []
}
```

## Ground Truth Tracking Data

### Current Status
**❌ Neither repository currently exports ground truth trajectories**

### What's Available
- Track positions are generated internally in `Track` struct:
  ```rust
  struct Track {
      object_ids: Vec<String>,        // Objects used per frame
      positions: Vec<(usize, usize)>, // (pulse_idx, bin_idx) per frame
      start_frame: usize,             // When track starts
      end_frame: usize,               // When track ends
      is_stationary: bool             // Stationary vs moving
  }
  ```

- Track generation includes:
  - Staggered start/end times (objects enter/exit mid-sequence)
  - 70% stationary objects, 30% moving objects
  - Curved Bezier paths for moving objects
  - Slow movement option (max_distance = 150 pixels)
  - Edge-based entry/exit points

### What Would Need to Be Added
To export ground truth for ST-DBSCAN evaluation:

1. **Add trajectory export function** (in Rust augmenter):
   ```rust
   fn write_track_ground_truth(
       tracks: &[Track],
       output_path: &Path,
       converter: &RadarConverter,  // For polar-to-Cartesian conversion
   ) -> Result<()>
   ```

2. **Export format options**:
   - **JSON** (best for complex scenarios):
     ```json
     {
       "tracks": [
         {
           "track_id": 0,
           "start_frame": 0,
           "end_frame": 100,
           "is_stationary": false,
           "positions": [
             {"frame": 0, "pulse_idx": 1200, "bin_idx": 450, "x": 512.3, "y": 768.1},
             {"frame": 1, "pulse_idx": 1203, "bin_idx": 452, "x": 515.7, "y": 770.8},
             ...
           ]
         }
       ]
     }
     ```

   - **CSV** (simpler, easier for analysis):
     ```
     track_id,frame,pulse_idx,bin_idx,x,y,is_stationary
     0,0,1200,450,512.3,768.1,false
     0,1,1203,452,515.7,770.8,false
     1,0,800,300,350.2,420.5,true
     ```

3. **Add CLI flag**:
   ```bash
   --export-ground-truth  # Enable ground truth trajectory export
   ```

## Simulation Parameters for ST-DBSCAN Paper

### Paper Requirements (Section 5.1 - Synthetic Dataset)

#### Scenario A (Easy)
- **Vessels**: 3
- **Trajectories**: Parallel linear, well-separated (>100 px)
- **Velocity**: Constant 5 px/frame
- **Duration**: 100 sweeps
- **Noise**: Gaussian position noise σ = 2 px
- **Clutter**: 50 points per frame
- **Features**: No crossings, no dropouts

#### Scenario B (Medium)
- **Vessels**: 5
- **Trajectories**: 2 crossing paths, 1 with 90° turn
- **Velocity**: Variable 3-8 px/frame
- **Duration**: 150 sweeps
- **Noise**: Gaussian position noise σ = 3 px
- **Clutter**: 100 points per frame
- **Features**: Path crossings, maneuvers

#### Scenario C (Hard)
- **Vessels**: 8
- **Trajectories**: Close convoy (3 vessels within 30 px), multiple crossings, 1 reversal
- **Velocity**: Variable
- **Duration**: 200 sweeps
- **Noise**: Gaussian position noise σ = 4 px
- **Clutter**: 200 points per frame
- **Dropouts**: 10% random detection dropouts
- **Features**: Dense traffic, close proximity, maneuvers, intermittent detections

### Current Augmenter Limitations

❌ **Missing Features** (would need to be added):
1. **Gaussian position noise**: Not currently applied to object placements
2. **Random detection dropouts**: No mechanism to randomly skip objects
3. **Precise velocity control**: Track speeds not explicitly controlled
4. **Linear trajectories**: Only curved (Bezier) paths available
5. **Random clutter generation**: No built-in clutter point generation
6. **Convoy/proximity constraints**: No mechanism to force vessels to stay close

✅ **Available Features**:
1. **Multiple tracks**: `--num-tracks` parameter
2. **Curved paths**: `--curvature` parameter
3. **Varying speeds**: Staggered tracks with different durations
4. **Reproducibility**: `--seed` parameter
5. **Frame count**: `--count` parameter

## Recommended Approach for ST-DBSCAN Scenarios

### Option 1: Extend Current Augmenter (More Work)

Add to Rust augmenter:
```rust
// New parameters needed
--noise-sigma <F32>           // Gaussian position noise (px)
--dropout-rate <F32>          // Random detection dropout probability (0-1)
--clutter-points <N>          // Random clutter points per frame
--trajectory-type <TYPE>      // linear|curved|mixed
--min-separation <PIXELS>     // Minimum vessel separation
--velocity-range <MIN-MAX>    // Velocity range (px/frame)
```

**Pros**:
- Full control over all parameters
- Integrated workflow
- Could be reused for other projects

**Cons**:
- Requires Rust programming
- Time-intensive for paper deadline
- May over-engineer for one-time use

### Option 2: Post-Process Augmenter Output (Easier)

Generate base synthetic data with augmenter, then post-process:

```python
# Python script to add noise, dropouts, and clutter
import numpy as np
import csv
from pathlib import Path

def add_noise_and_dropouts(
    input_csv: Path,
    output_csv: Path,
    noise_sigma: float = 2.0,
    dropout_rate: float = 0.0,
    clutter_points: int = 50
):
    # Read CSV
    pulses = read_radar_csv(input_csv)

    # Add Gaussian noise to object positions
    pulses = add_gaussian_noise(pulses, noise_sigma)

    # Random dropouts (remove objects)
    pulses = apply_dropouts(pulses, dropout_rate)

    # Add random clutter
    pulses = add_clutter(pulses, clutter_points)

    # Write modified CSV
    write_radar_csv(pulses, output_csv)
```

**Pros**:
- Faster to implement (Python)
- Flexible for experiments
- Can iterate quickly on parameters

**Cons**:
- Two-step workflow
- Noise/clutter may not look realistic
- Harder to guarantee reproducibility

### Option 3: Custom Python Generator (Most Control)

Build complete scenario generator in Python:

```python
# Generate scenarios from scratch with full control
def generate_scenario_a():
    tracks = [
        LinearTrack(start=(100, 200), velocity=(5, 0), duration=100),
        LinearTrack(start=(100, 400), velocity=(5, 0), duration=100),
        LinearTrack(start=(100, 600), velocity=(5, 0), duration=100),
    ]

    for frame in range(100):
        # Place objects on background
        # Add noise
        # Add clutter
        # Export CSV + ground truth
```

**Pros**:
- Complete control
- Easy to add ground truth export
- Can exactly match paper specifications

**Cons**:
- Most work
- Doesn't leverage existing object library
- Need to handle polar coordinates

## Recommended Implementation Strategy

### For Paper Deadline (Fastest Path)

1. **Use SyntheticRadarGeneration_Training** (has YOLO label export infrastructure)

2. **Modify augmenter** minimally to add ground truth export:
   ```rust
   // Add to main.rs around line 240
   if args.export_ground_truth {
       write_track_ground_truth(&tracks, &args.output.join("ground_truth.json"))?;
   }
   ```

3. **Generate base scenarios** with augmenter:
   ```bash
   # Scenario A (3 parallel tracks)
   cargo run --release -p augmenter -- \
     -a data/annotation.json \
     --land-frames data/land_frames/ \
     --library data/object_library/ \
     -o scenarios/scenario_a_base \
     --count 100 \
     --mode tracks \
     --num-tracks 3 \
     --curvature 0.0 \
     --seed 42 \
     --export-ground-truth

   # Scenario B (5 tracks, more curved)
   cargo run --release -p augmenter -- \
     -a data/annotation.json \
     --land-frames data/land_frames/ \
     --library data/object_library/ \
     -o scenarios/scenario_b_base \
     --count 150 \
     --mode tracks \
     --num-tracks 5 \
     --curvature 0.5 \
     --seed 43 \
     --export-ground-truth

   # Scenario C (8 tracks, high curvature)
   cargo run --release -p augmenter -- \
     -a data/annotation.json \
     --land-frames data/land_frames/ \
     --library data/object_library/ \
     -o scenarios/scenario_c_base \
     --count 200 \
     --mode tracks \
     --num-tracks 8 \
     --curvature 0.7 \
     --seed 44 \
     --export-ground-truth
   ```

4. **Post-process** with Python script to add:
   - Gaussian position noise
   - Random dropouts (Scenario C only)
   - Random clutter points
   - Export modified ground truth

5. **Convert to point clouds** for ST-DBSCAN input:
   ```python
   # CSV → Point Cloud
   # Extract intensity > threshold
   # Convert polar → Cartesian
   # Export as NumPy array or CSV
   ```

### Detailed Post-Processing Script Structure

```python
import numpy as np
import json
from pathlib import Path
from typing import List, Tuple
import csv

class RadarScenarioProcessor:
    def __init__(self, config: dict):
        self.noise_sigma = config.get('noise_sigma', 0.0)
        self.dropout_rate = config.get('dropout_rate', 0.0)
        self.clutter_points = config.get('clutter_points', 0)
        self.intensity_threshold = config.get('intensity_threshold', 20)

    def load_ground_truth(self, gt_path: Path) -> dict:
        """Load ground truth trajectories."""
        with open(gt_path) as f:
            return json.load(f)

    def read_radar_csv(self, csv_path: Path) -> List[Tuple[float, List[int]]]:
        """Read radar CSV file."""
        pulses = []
        with open(csv_path) as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 6:
                    continue
                angle_ticks = int(row[4])
                angle_rad = (angle_ticks / 8192.0) * 2 * np.pi
                echoes = [int(x) for x in row[5:]]
                pulses.append((angle_rad, echoes))
        return pulses

    def add_gaussian_noise(self, pulses, sigma):
        """Add Gaussian position noise to detections."""
        # Identify object pixels (intensity > threshold)
        # Add noise to their positions
        # Re-quantize to pulse/bin indices
        pass

    def apply_dropouts(self, pulses, dropout_rate):
        """Randomly remove detections."""
        pass

    def add_clutter(self, pulses, num_points):
        """Add random clutter points in water regions."""
        pass

    def to_point_cloud(self, pulses) -> np.ndarray:
        """Convert polar radar data to Cartesian point cloud."""
        points = []
        for angle, echoes in pulses:
            for bin_idx, intensity in enumerate(echoes):
                if intensity > self.intensity_threshold:
                    # Polar to Cartesian
                    r = bin_idx  # or scale to meters
                    x = r * np.sin(angle)
                    y = r * np.cos(angle)
                    points.append([x, y, intensity])
        return np.array(points)

    def process_scenario(self, input_dir: Path, output_dir: Path):
        """Process entire scenario."""
        gt = self.load_ground_truth(input_dir / "ground_truth.json")

        for csv_file in sorted(input_dir.glob("augmented_*.csv")):
            # Read
            pulses = self.read_radar_csv(csv_file)

            # Add noise
            pulses = self.add_gaussian_noise(pulses, self.noise_sigma)

            # Apply dropouts
            pulses = self.apply_dropouts(pulses, self.dropout_rate)

            # Add clutter
            pulses = self.add_clutter(pulses, self.clutter_points)

            # Convert to point cloud
            point_cloud = self.to_point_cloud(pulses)

            # Save
            output_dir.mkdir(exist_ok=True, parents=True)
            np.save(output_dir / f"{csv_file.stem}.npy", point_cloud)

        # Export modified ground truth
        self.export_modified_ground_truth(gt, output_dir / "ground_truth.json")

# Usage
configs = {
    'scenario_a': {
        'noise_sigma': 2.0,
        'dropout_rate': 0.0,
        'clutter_points': 50,
    },
    'scenario_b': {
        'noise_sigma': 3.0,
        'dropout_rate': 0.0,
        'clutter_points': 100,
    },
    'scenario_c': {
        'noise_sigma': 4.0,
        'dropout_rate': 0.10,
        'clutter_points': 200,
    },
}

for scenario, config in configs.items():
    processor = RadarScenarioProcessor(config)
    processor.process_scenario(
        Path(f"scenarios/{scenario}_base"),
        Path(f"scenarios/{scenario}_processed")
    )
```

## Running the Generation Scripts

### SyntheticRadarGeneration_Training

```bash
# Build
cd SyntheticRadarGeneration_Training/radar_augmentation
cargo build --release

# Generate with tracks (current capability)
./target/release/augmenter \
  -a ../data/annotation.json \
  --land-frames ../data/land_frames/ \
  --library ../data/object_library/ \
  -o ../results/scenario_a \
  -c 100 \
  --mode tracks \
  --num-tracks 3 \
  --curvature 0.2 \
  --seed 42 \
  --export-labels \
  --label-class 1

# Convert to PNG images
cd ..
python radar_augmentation/scripts/generate_images.py \
  --synthetic-input results/scenario_a/ \
  --output-dir results/scenario_a_images/ \
  --max-frames 100

# Apply echo trails
python src/utils/apply_echo_trails.py \
  --input results/scenario_a_images/ \
  --output results/scenario_a_trails/ \
  --history 5 \
  --batch-mode
```

### radar-sim-platform

```bash
# Build
cd radar-sim-platform/radar_augmentation
cargo build --release

# Generate synthetic data
cargo run --release -p augmenter -- \
  --annotation ../portable_data/annotation.json \
  --land-frames ../portable_data/land_frames/ \
  --library ../portable_data/object_library/ \
  --output ../output/scenario_test \
  --count 100 \
  --mode tracks \
  --num-tracks 5 \
  --seed 42

# Visualize tracks
python scripts/visualize_tracks.py \
  --input ../output/scenario_test \
  --output-dir ../output/visualizations

# Create video
python scripts/create_video.py \
  --input ../output/scenario_test \
  --output ../output/scenario_test.mp4 \
  --fps 10
```

## Key Files and Locations

### SyntheticRadarGeneration_Training
```
/Users/jvaught/Downloads/Code/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Cancilla_ST-DBSCAN/SyntheticRadarGeneration_Training/
├── radar_augmentation/
│   ├── src/augmenter/src/main.rs          # Main augmenter logic
│   ├── src/radar_core/                     # Shared library
│   └── scripts/
│       ├── generate_images.py              # CSV → PNG
│       └── echo_trails.py                  # Motion trails
├── src/
│   ├── data_generation/generate_dataset.py # YOLO dataset creation
│   └── utils/apply_echo_trails.py          # Echo trail batch processing
├── data/
│   ├── annotation.json                     # Water/land mask
│   ├── land_frames/                        # 164 background CSVs
│   └── object_library/                     # 1847 objects
│       ├── metadata.json
│       └── objects/                        # UUID.json files
└── scripts/
    └── generate_synthetic_data.sh          # Wrapper script
```

### radar-sim-platform
```
/Users/jvaught/Downloads/Code/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Cancilla_ST-DBSCAN/radar-sim-platform/
├── radar_augmentation/
│   ├── src/augmenter/src/main.rs          # Main augmenter logic (no labels)
│   └── scripts/
│       ├── visualize_tracks.py             # Track visualization
│       ├── create_video.py                 # Video generation
│       └── generate_images.py              # CSV → PNG
└── portable_data/
    ├── annotation.json                     # Water/land mask
    ├── land_frames/                        # 164 background CSVs
    └── object_library/                     # 1847 objects
```

## Summary and Recommendation

### Which Repository to Use?

**Use SyntheticRadarGeneration_Training** for the ST-DBSCAN paper because:
1. ✅ Has YOLO label export infrastructure (shows it can export metadata)
2. ✅ Easier to extend for ground truth export
3. ✅ More complete pipeline for dataset generation
4. ✅ Already has batch processing scripts

### Implementation Priority for Paper

1. **Critical** (Must have):
   - Add ground truth trajectory export to augmenter
   - Python post-processing for noise/dropout/clutter
   - CSV-to-point-cloud converter

2. **Important** (Should have):
   - Scenario configuration files (JSON/YAML)
   - Automated scenario generation scripts
   - Ground truth format validation

3. **Nice to have** (Could have):
   - Linear trajectory mode in augmenter
   - Convoy/proximity constraints
   - Real-time visualization during generation

### Estimated Implementation Time

- **Minimal approach** (Option 2): 1-2 days
  - Add basic ground truth export: 4-6 hours
  - Post-processing script: 4-6 hours
  - Testing and validation: 4 hours

- **Full approach** (Option 1): 3-5 days
  - Extend Rust augmenter: 1-2 days
  - Integration and testing: 1-2 days
  - Documentation: 0.5 day

**Recommendation**: Start with Option 2 (post-processing) to meet paper deadline, then enhance with Option 1 features if time allows.

## Next Steps

1. Choose repository (recommend SyntheticRadarGeneration_Training)
2. Add ground truth export to augmenter (minimal Rust changes)
3. Create Python post-processing script for noise/dropout/clutter
4. Generate three scenarios A, B, C
5. Validate ground truth matches paper specifications
6. Convert to point cloud format for ST-DBSCAN input
7. Run ST-DBSCAN experiments
8. Generate figures for paper (Section 5.1)
