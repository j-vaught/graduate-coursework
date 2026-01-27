# NASA Reference Guide for Space Grant Proposal Alignment

**Purpose:** Comprehensive reference for aligning undergraduate research proposals with NASA priorities, programs, and technology needs.

---

## Table of Contents

1. [NASA Mission Directorates Overview](#1-nasa-mission-directorates-overview)
2. [Artemis Program Deep Dive](#2-artemis-program-deep-dive)
3. [Earth Observation & Remote Sensing](#3-earth-observation--remote-sensing)
4. [Autonomous Systems & Robotics](#4-autonomous-systems--robotics)
5. [NASA Technology Taxonomy](#5-nasa-technology-taxonomy)
6. [Technology Readiness Levels](#6-technology-readiness-levels)
7. [Current Technology Gaps & Priorities](#7-current-technology-gaps--priorities)
8. [EPSCoR Research Focus Areas](#8-epscor-research-focus-areas)
9. [Alignment Strategies for Your Proposals](#9-alignment-strategies-for-your-proposals)

---

## 1. NASA Mission Directorates Overview

NASA has **five Mission Directorates**. Your proposal should explicitly connect to at least one.

### 1.1 Science Mission Directorate (SMD)

**Mission:** Explore the secrets of the universe, search for life, and safeguard our home planet.

**Five Divisions:**

| Division | Focus Areas | Keywords |
|----------|-------------|----------|
| **Earth Science** | Climate, weather, natural hazards, ecosystems | Remote sensing, Earth observation, climate monitoring |
| **Planetary Science** | Solar system exploration, Mars, Moon, asteroids | Rovers, landers, sample return |
| **Astrophysics** | Universe origins, black holes, exoplanets | Telescopes, imaging, spectroscopy |
| **Heliophysics** | Sun, solar wind, space weather | Magnetosphere, radiation, solar activity |
| **Biological & Physical Sciences** | Life in space, materials, fluids | Microgravity, life support, human factors |

**2024-2026 Priorities:**
- Open science and data accessibility
- Climate action and disaster response
- Earth System Observatory (ESO) satellite constellation
- Commercial Lunar Payload Services (CLPS)
- Europa Clipper mission

**Undergraduate Contributions:**
- Data analysis from open repositories
- Citizen science participation
- CLPS payload development
- Earth applications research

---

### 1.2 Space Technology Mission Directorate (STMD)

**Mission:** Develop and demonstrate transformative space technologies.

**Key Programs:**

| Program | Focus | TRL Range |
|---------|-------|-----------|
| **NIAC** | Visionary concepts | TRL 1-2 |
| **Game Changing Development** | Revolutionary technologies | TRL 2-5 |
| **Small Spacecraft** | CubeSats, small sats | TRL 4-7 |
| **SBIR/STTR** | Small business innovation | TRL 3-6 |
| **Lunar Surface Innovation Initiative (LSII)** | Moon technologies | TRL 2-6 |

**2024 Priority:** Civil Space Shortfall Ranking identified 187 shortfalls → consolidated to 32 categories

**Top Technology Shortfalls:**
1. Survive and operate through lunar night
2. High-power energy generation on lunar/Mars surfaces
3. High-performance onboard computing

**Undergraduate Contributions:**
- Early TRL (1-3) research
- CubeSat development
- ISRU experiments
- Proof-of-concept demonstrations
- Algorithm development

---

### 1.3 Exploration Systems Development Mission Directorate (ESDMD)

**Mission:** Artemis program and Moon-to-Mars architecture.

**Core Systems:**
- Space Launch System (SLS)
- Orion spacecraft
- Gateway lunar station
- Human Landing Systems
- Lunar Terrain Vehicle

**2024 Focus:** 56 technology gaps identified (5 high-priority)

**Undergraduate Contributions:**
- Technology gap solutions
- CLPS payloads
- Systems engineering
- ISRU research
- Simulation and modeling

---

### 1.4 Space Operations Mission Directorate (SOMD)

**Mission:** ISS operations, commercial crew/cargo, LEO development.

**Key Programs:**
- ISS National Lab (~200 investigations/year)
- Commercial LEO Development
- Deep Space Optical Communications (DSOC)

**Undergraduate Contributions:**
- ISS experiments
- Commercial applications
- Optical communications research
- Operations analysis

---

### 1.5 Aeronautics Research Mission Directorate (ARMD)

**Mission:** Safe, sustainable air transportation; net-zero emissions by 2050.

**Six Strategic Thrusts:**

| Thrust | Focus |
|--------|-------|
| Safe Operations | Operational safety |
| Supersonic Flight | Low-boom supersonic |
| Ultra-Efficient Vehicles | Next-gen aircraft |
| Low-Carbon Propulsion | Electric, hydrogen |
| Safety Assurance | Risk management |
| Assured Autonomy | Autonomous aviation |

**Key Programs:**
- Electrified Propulsion Flight Demonstrator (EPFD)
- Advanced Air Mobility (AAM)
- Sustainable aviation fuels

**Undergraduate Contributions:**
- Electric propulsion
- Sustainable fuels
- AI/ML for safety
- UAM/AAM concepts
- Battery research

---

## 2. Artemis Program Deep Dive

### 2.1 Mission Timeline

| Mission | Date | Type | Key Features |
|---------|------|------|--------------|
| **Artemis I** | Nov 2022 | Uncrewed | Completed - tested SLS and Orion |
| **Artemis II** | Feb 2026 | Crewed flyby | First crew to lunar vicinity since 1972 |
| **Artemis III** | Mid-2027 | Crewed landing | First woman and person of color on Moon |
| **Artemis IV** | Sept 2028 | Crewed + Gateway | First Gateway docking |

### 2.2 Key Technologies

#### Space Launch System (SLS)
- **Payload:** >27 metric tons to lunar orbit
- **Thrust:** ~8.8 million lbs at liftoff
- **Speed:** 24,500 mph in 8 minutes to orbit

#### Orion Spacecraft
- **Crew:** 4 astronauts
- **Duration:** 21 days undocked, 6 months docked
- **Heat Shield:** 5,000°F reentry capability
- **Innovation:** Skip-entry technique for precise landing

#### Human Landing System (SpaceX Starship HLS)
- **Height:** ~165 feet (15-story building)
- **Surface time:** ~7 days
- **EVAs:** Minimum 5 spacewalks
- **Refueling:** Multiple tanker missions in Earth orbit

#### Gateway Lunar Station
- **Orbit:** Near-rectilinear halo orbit (NRHO)
- **Power:** 60 kW solar electric
- **Crew capacity:** 4 astronauts for 90 days
- **First crewed visit:** Artemis IV (2028)

#### Lunar Terrain Vehicle (LTV)
- **Range:** Up to 20 km from landing site
- **Operation:** Crewed and autonomous
- **Navigation:** Crater-based localization, LIDAR, cameras
- **First use:** Artemis V

### 2.3 Surface Operations Challenges

These represent technology gaps your research could address:

#### Navigation & Terrain Sensing
- **Requirement:** Land within 100m of target
- **Technologies:** Terrain Relative Navigation (TRN), Navigation Doppler Lidar, LIDAR hazard detection
- **Challenge:** No GPS on Moon; must use visual landmarks and sensor fusion
- **Maps needed:** 1-meter resolution Digital Terrain Models

#### Autonomous Systems Needs
- Real-time autonomous decision-making
- Multi-robot coordination
- Extreme terrain traversal
- Human-robotic cooperation
- Subsurface exploration (lava tubes)

#### Dust Mitigation
- **Problem:** Electrostatically charged, abrasive lunar dust
- **Impacts:** Equipment damage, health risks, optical degradation
- **Solutions in development:**
  - Electrodynamic Dust Shields (EDS)
  - Advanced coatings
  - Acoustic methods

#### Communications (LunaNet)
- Delay/Disruption Tolerant Networking
- Autonomous navigation services
- Space weather monitoring
- Search and rescue capability

#### Power Systems
- **Fission:** 40+ kW continuous, operates through 14-day lunar night
- **Solar:** Near-continuous at poles, but needs 8+ day storage
- **Challenge:** -173°C during lunar night

### 2.4 Research Priorities for Lunar Exploration

| Priority | Description |
|----------|-------------|
| **Planetary Processes** | Understanding Moon and Earth formation |
| **South Pole Environment** | Risks and resources assessment |
| **Permanently Shadowed Regions** | Water ice detection and extraction |
| **ISRU** | In-situ resource utilization |

---

## 3. Earth Observation & Remote Sensing

### 3.1 Earth Science Division Priorities

**Earth System Observatory (ESO)** - Five core satellite missions:
1. Aerosols
2. Clouds/Precipitation
3. Mass Change
4. Surface Biology
5. Surface Deformation

**Current Fleet:** 20+ satellites operational

### 3.2 Remote Sensing Technologies

#### Synthetic Aperture Radar (SAR)
- **NISAR Mission:** NASA-ISRO partnership, >50 petabytes/year
- **Capabilities:** All-weather, day/night, surface deformation
- **Ocean applications:** Wind retrieval, wave monitoring, vessel detection

#### Lidar
- **GEDI:** Forest structure
- **ICESat-2:** Ice sheets
- **Applications:** Terrain mapping, vegetation height, bathymetry

#### Hyperspectral
- **PACE:** Ocean biology, aerosols (launched Feb 2024)
- **Applications:** Water quality, phytoplankton, atmospheric composition

### 3.3 Maritime & Coastal Monitoring

**NASA-NOAA Partnerships:**
- HF Radar integration at Kennedy Space Center
- Sentinel-6B radar altimeter for sea levels
- SAR wind products for maritime applications

**Applications:**
- Search and rescue
- Oil spill tracking
- Harmful algal blooms
- Coastal erosion monitoring

### 3.4 Adaptive Algorithms for Earth Observation

**NASA AI/ML Priorities:**
- Autonomous event detection (wildfires, storms)
- Real-time onboard processing
- Edge computing on satellites

**Hardware Tested:**
- Snapdragon 855, Myriad X on ISS
- Google Coral Edge TPUs (SpaceCube platform)

**Connection to Maritime Radar:**
- Shared signal processing challenges
- Adaptive algorithms for varying conditions
- Edge computing with power constraints
- Target detection in clutter

---

## 4. Autonomous Systems & Robotics

### 4.1 NASA Autonomous Systems Programs

| Program | Description |
|---------|-------------|
| **Autonomous Systems & Robotics (ASR)** | Novel architectures, algorithms, software |
| **CADRE** | Cooperative mini-rovers for lunar exploration |
| **Fly Foundational Robots** | Robotic arm for orbital operations |
| **OSAM-1** | Autonomous satellite servicing |

### 4.2 Robotics Research Areas

#### Planetary Rovers
- **Perseverance:** 88% of driving is autonomous
- **AI-enabled PIXL:** Autonomous sample targeting
- **CADRE:** Cooperative autonomous rovers (launching soon)

#### Key Capabilities
- Real-time autonomous decision-making
- Multi-robot coordination
- Extreme terrain traversal
- Human-robotic teaming

### 4.3 Machine Learning at NASA

**Applications:**
1. Autonomous decision-making for rovers
2. Exoplanet discovery (ExoMiner found 301 new exoplanets)
3. Sample analysis (PIXL on Perseverance)
4. Science data analysis
5. Space biology (AI4LS)

### 4.4 Sensor Fusion & Perception

**Technologies:**
- Stereo depth fusion with LIDAR
- SLAM algorithms (Wildcat)
- Multi-sensor integration
- Low-cost perception systems

### 4.5 Navigation & Obstacle Detection

**Systems:**
- Positive obstacle detection (elevated hazards)
- Negative obstacle detection (depressions) - most challenging
- Slope detection
- Water hazard detection
- Range density-based detection

**Challenges:**
- GNSS-denied environments
- Nighttime autonomous navigation
- Off-road terrain
- Extreme lighting conditions

### 4.6 Adaptive Algorithms for Space

| Technology | Application |
|------------|-------------|
| **Adaptive Augmenting Control (AAC)** | SLS flight control |
| **HAANA** | Neural algorithms for image processing |
| **Genetic Algorithms** | Real-time control adaptation |

### 4.7 Edge Computing & Embedded Systems

**High Performance Spaceflight Computing (HPSC):**
- Radiation-hardened multicore System-on-Chip
- Advanced edge processing

**Spaceborne AI:**
- 24+ experiments on ISS demonstrating edge computing
- Reduced time-to-insight from months to minutes
- AxDCU-1 Data Processing Unit on ISS (2024)

### 4.8 Point Cloud Processing

**Space Qualified Rover Lidar (SQRLi):**
- Lightweight, space-hardened
- Sub-millimeter resolution 3D maps

**Applications:**
- Terrain traversability analysis
- Rock detection on Mars
- Crater identification
- Surface feature extraction

### 4.9 Object Detection & Classification

**YOLO at NASA:**
- OnAIR Platform integration
- Crater detection applications
- Edge TPU compatibility

**Applications:**
- Crater detection for landing
- Rock classification
- Hazard identification
- Sample targeting

---

## 5. NASA Technology Taxonomy

NASA organizes technology across **17 discipline-based taxonomies (TX)**:

| TX | Area | Relevance to Your Research |
|----|------|---------------------------|
| **TX01** | Propulsion Systems | - |
| **TX02** | Flight Computing & Avionics | Edge computing, embedded systems |
| **TX03** | Power & Energy Storage | - |
| **TX04** | Robotic Systems | Autonomous detection, navigation |
| **TX05** | Communications, Navigation, Debris Tracking | Tracking algorithms, object detection |
| **TX06** | Human Health & Life Support | - |
| **TX07** | Exploration Destination Systems | Surface operations |
| **TX08** | Sensors & Instruments | Radar, remote sensing |
| **TX09** | Entry, Descent & Landing | Terrain sensing, hazard detection |
| **TX10** | Autonomous Systems | Adaptive algorithms, ML |
| **TX11** | Software, Modeling, Simulation | Algorithm development |
| **TX12** | Materials, Structures, Manufacturing | - |
| **TX13** | Ground, Test & Surface Systems | - |
| **TX14** | Thermal Management | - |
| **TX15** | Flight Vehicle Systems | - |
| **TX16** | Air Traffic Management | - |
| **TX17** | Guidance, Navigation & Control | Navigation algorithms |

**Most Relevant to Sensing/Autonomy Research:**
- TX04 (Robotic Systems)
- TX05 (Navigation, Tracking)
- TX08 (Sensors & Instruments)
- TX09 (EDL - terrain sensing)
- TX10 (Autonomous Systems)
- TX11 (Software, Algorithms)
- TX17 (GN&C)

---

## 6. Technology Readiness Levels

| TRL | Name | Description | Undergraduate Fit |
|-----|------|-------------|-------------------|
| **1** | Basic Principles | Scientific research beginning | Research papers, literature review |
| **2** | Concept Formulated | Applied research, invention begins | Concept development |
| **3** | Proof of Concept | Analytical/experimental validation | **Ideal for undergrad** |
| **4** | Lab Validation | Breadboard demonstration | **Ideal for undergrad** |
| **5** | Relevant Environment | Rigorous testing of components | Stretch goal |
| **6** | Prototype Demo | Fully functional prototype | Graduate level |
| **7-9** | Operational | Flight qualified and proven | Industry/NASA |

**Space Grant projects typically target TRL 2-4** - perfect for undergraduate research.

---

## 7. Current Technology Gaps & Priorities

### 7.1 Top 32 Integrated Technology Categories (2024)

**Highest Priority:**
1. Survive and operate through lunar night
2. High-power energy generation (Moon/Mars)
3. High-performance onboard computing

### 7.2 Navigation & Sensing Gaps

| Gap | Description | Your Research Connection |
|-----|-------------|-------------------------|
| **Precision Landing** | <100m accuracy with real-time hazard avoidance | Adaptive detection algorithms |
| **Long-Range Navigation** | Autonomous 20+ km without GPS | Sensor fusion, tracking |
| **PSR Operations** | Navigation without visual cues | Adaptive sensing |
| **Multi-Sensor Fusion** | LIDAR + cameras + IMU integration | Point cloud processing |
| **Crater Recognition** | Robust localization across lighting | Object detection |

### 7.3 Autonomous Systems Gaps

| Gap | Description |
|-----|-------------|
| Real-time decision-making | Operating with communication delays |
| Multi-robot coordination | Minimal human oversight |
| Extreme terrain mobility | Slopes, boulders, loose regolith |
| Opportunistic science | Autonomous target identification |
| Fault detection and recovery | Self-diagnosis and repair |

### 7.4 Data Processing Gaps

| Gap | Description |
|-----|-------------|
| Bandwidth limitations | High-volume data with limited relay |
| Autonomous processing | Onboard data reduction and prioritization |
| Distributed networks | Coordination among multiple assets |
| Edge computing | Processing in harsh environments |

---

## 8. EPSCoR Research Focus Areas

NASA EPSCoR funds university research aligned with mission priorities.

### 8.1 Primary Research Domains

| Domain | Topics |
|--------|--------|
| **Remote Sensing** | Earth observation, optical properties |
| **Artificial Intelligence** | Autonomy systems, data analysis |
| **Astrophysics** | Fundamental physics, quantum sensing |
| **Aeronautics** | Propulsion, hypersonics, UAM |
| **Space Manufacturing** | Additive manufacturing, ISRU |
| **Astronaut Health** | Muscle atrophy, human physiology |
| **Climate Research** | Earth science, space weather |

### 8.2 Funding Opportunities

| Award Type | Amount | Duration |
|------------|--------|----------|
| Rapid Response (R3) | Up to $125,000 | 1 year |
| Research Awards (RA) | Up to $750,000 | 3 years |
| Research Infrastructure | Up to $125,000/year | 3 years |

### 8.3 Connection to Mission Directorates

All EPSCoR proposals must align with at least one directorate:
- ARMD → Aeronautics
- SMD → Science (Earth, planetary, astro, helio)
- ESDMD → Human exploration
- STMD → Technology development

---

## 9. Alignment Strategies for Your Proposals

### 9.1 ST-DBSCAN Maritime Radar Project

**Primary Alignment: Science Mission Directorate (SMD)**

| NASA Priority | Your Research Connection |
|---------------|-------------------------|
| Earth observation | Maritime monitoring complements satellite data |
| Adaptive algorithms | Self-tuning for varying conditions (like spaceborne sensors) |
| NOAA partnership | NASA-NOAA joint maritime/coastal monitoring |
| Edge computing | Jetson benchmarking shows embedded capability |

**Secondary Alignment: Space Technology Mission Directorate (STMD)**

| NASA Priority | Your Research Connection |
|---------------|-------------------------|
| Autonomous systems (TX10) | Adaptive clustering without manual tuning |
| Sensors & instruments (TX08) | Point cloud processing from radar |
| GN&C (TX17) | Tracking and detection algorithms |

**Artemis Connection:**

> "The adaptive clustering techniques developed for maritime radar apply directly to spaceborne sensors and lunar surface operations. Self-tuning algorithms that adapt to varying clutter conditions address a critical need for autonomous systems operating without ground control. Similar point cloud processing could enable lunar rover obstacle detection, orbital debris characterization, or planetary surface analysis."

**Specific Keywords to Use:**
- Adaptive sensing algorithms
- Point cloud processing
- Self-tuning/autonomous operation
- Sensor fusion
- Real-time embedded processing
- Object classification
- Target detection in clutter

### 9.2 General Proposal Alignment Template

**NASA Relevance Section Structure:**

```
1. MISSION DIRECTORATE ALIGNMENT
   "This research directly supports NASA's [Directorate] priority to [specific goal]."

2. SPECIFIC PROGRAM/INITIATIVE
   "As outlined in [NASA document/program], [quote or reference]..."

3. TECHNOLOGY GAP ADDRESSED
   "This work addresses the technology gap in [specific area] by [your approach]."

4. BROADER APPLICATIONS
   "Beyond the immediate application, this research enables [lunar/Mars/space applications]."

5. WORKFORCE DEVELOPMENT
   "This project builds skills in [specific capabilities] that NASA needs for [missions]."
```

### 9.3 Keyword Mapping

| If Your Research Involves... | Use These NASA Keywords... |
|------------------------------|---------------------------|
| Tracking/detection | Object detection, target classification, hazard identification |
| Adaptive algorithms | Self-tuning, autonomous operation, adaptive sensing |
| Point clouds | 3D perception, terrain analysis, LIDAR processing |
| Real-time processing | Edge computing, onboard processing, embedded systems |
| Machine learning | AI/ML, neural networks, pattern recognition |
| Sensor data | Sensor fusion, multi-modal sensing, remote sensing |
| Maritime/environmental | Earth observation, ocean monitoring, coastal sensing |

### 9.4 Documents to Reference

| Document | Use For |
|----------|---------|
| NASA Technology Taxonomy | Identifying TX areas |
| 2025-2026 NASA Science Plan | SMD priorities |
| Artemis Plan | Exploration connections |
| Civil Space Shortfall Ranking | Technology gaps |
| EPSCoR Research Focus Areas | University research priorities |
| NASA SBIR Topics | Specific technology needs |

---

## Quick Reference: Your Proposal Connections

### For Maritime Radar / ST-DBSCAN:

**Mission Directorate:** SMD (primary), STMD (secondary)

**Technology Taxonomy:** TX08, TX10, TX11, TX17

**Artemis Connections:**
- Lunar rover obstacle detection (similar point cloud challenges)
- Autonomous navigation in GPS-denied environments
- Adaptive algorithms for sensors without ground control
- Real-time processing on embedded hardware

**Earth Science Connections:**
- Maritime monitoring (NASA-NOAA partnership)
- SAR and radar data processing
- Adaptive algorithms for spaceborne sensors
- Edge computing for satellite autonomy

**Keywords:**
Adaptive sensing, autonomous detection, point cloud processing, self-tuning algorithms, edge computing, target classification, sensor fusion, real-time processing

---

*Reference compiled January 25, 2026 from NASA official sources, program documentation, and strategic plans.*
