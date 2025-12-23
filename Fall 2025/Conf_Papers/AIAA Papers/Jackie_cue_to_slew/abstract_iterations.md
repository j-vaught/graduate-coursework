# Abstract Iterations

Based on the user's answers to the reviewer feedback, here are three variations of the abstract.

## Information Integration
*   **System Limits:** Daylight only, PT 180deg/1.5s, slow zoom/focus.
*   **Compute:** Jetson Orin (GPU+DLA), 30fps, YOLOv8 (but architecture agnostic).
*   **Control:** Hybrid Open-Loop (initial pointing) + Closed-Loop (visual servoing/zoom).
*   **Calibration:** Static lab calibration.
*   **Impact:** Hypothetical 95% reduction in labeling costs.

---

## Option 1: The "Systems & Control" Approach (Balanced)
*Focuses on the hybrid control strategy and the hardware-software integration. Good for general AIAA audience.*

Small objects in wide-field video streams suffer from extreme pixel scarcity, leading to low detector confidence and unstable localization. This paper describes an automated active acquisition system that couples a fixed wide-angle camera with a pan--tilt--zoom (PTZ) camera to construct high-quality datasets for small aerial targets. The system employs a hybrid control strategy: an initial open-loop slew commands the PTZ to the target's predicted bearing, followed by a closed-loop visual servoing phase where a secondary detector refines pointing and zoom. Running on an NVIDIA Jetson Orin at 30 Hz, the architecture-agnostic pipeline utilizes parallel YOLOv8 instances to maintain real-time tracking. High-confidence detections from the zoomed view are transferred back to the wide view using static laboratory calibration and time-synchronized telemetry, effectively amplifying label quality. A concrete test case is presented for airplanes in daylight conditions, managing targets with angular rates up to $120^\circ$/s. We provide system design, control formulations, and a theoretical evaluation protocol, estimating that this sensor-driven approach can reduce manual labeling effort by up to 95\% (20x) while capturing hard negatives and diverse viewing angles unavailable to passive systems.

## Option 2: The "Data-Centric" Approach (Impact Focused)
*Highlights the dataset construction aspect and the 95% cost reduction. Best if the main contribution is the resulting data quality.*

Deep learning performance on small objects is frequently bottlenecked by the quality and quantity of training data rather than model architecture. To address this, we present a fully automated "active labeling" pipeline that uses a secondary PTZ camera to perform resolution-enhanced verification of candidate targets detected by a fixed wide-angle sensor. By mechanically zooming in on uncertain targets, the system resolves ambiguity that is impossible to solve in the wide view alone. The pipeline integrates a greedy scheduling algorithm with a hybrid open-loop/closed-loop control scheme to harvest training examples and hard negatives continuously without human intervention. We demonstrate the system's theoretical performance using a daylight airplane tracking scenario, supported by a dual-stream YOLOv8 implementation on edge hardware (Jetson Orin). The proposed method replaces manual annotation with sensor-derived "ground truth," offering a projected 95\% reduction in labeling costs. We detail the static calibration and synchronization requirements necessary to achieve robust cross-view label transfer and provide a protocol for quantifying confidence uplift in deployed environments.

## Option 3: The "Experimental & Architecture" Approach (Detail Heavy)
* more specific about the hardware constraints and the specific implementation details.*

Deep learning performance on small objects is frequently bottlenecked by the quality and quantity of training data rather than model architecture. To address this, we propose an active dual-camera system for automated small-object dataset generation, specifically designed to overcome the resolution limits of static wide-angle surveillance. The system leverages a fixed wide-angle camera for target discovery and a PTZ unit for detailed interrogation. The control framework transitions from open-loop predictive slewing to closed-loop visual tracking, compensating for mechanical latencies and slow zoom mechanics. Implemented on an NVIDIA Jetson Orin, the system runs concurrent detector instances, one on the GPU and one on the Deep Learning Accelerator (DLA)to achieve 30 fps throughput. High-resolution object verifications are projected back into the wide frame using a static homography-based calibration, creating high-confidence labels for targets that appear as only a few pixels in the wide view. We validate the system design against a test case of distant aircraft in daylight, analyzing the trade-offs between slew speed ($120^\circ$/s) and zoom settling time. Preliminary analysis suggests this active acquisition paradigm can improve label precision significantly and reduce the human effort required for small-object dataset curation.
