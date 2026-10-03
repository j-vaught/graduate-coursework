#import "figures/src/acquisition.typ": schematic
#import "figures/src/plots.typ": response, error
#let teal=rgb("#006D75")
#let ink=rgb("#25282A")
#let pale=rgb("#EAF3F4")
#set document(title:"Limits of Whole-Scan Attitude Correction in High-Resolution Marine Radar",author:"J.C. Vaught",date:datetime(year:2026,month:10,day:2))
#set page(paper:"us-letter",margin:(top:0.62in,bottom:0.58in,left:0.72in,right:0.72in),footer:context[
  #line(length:100%,stroke:0.4pt+rgb("#B5B5B5"))
  #v(2pt)
  #text(size:8pt,fill:ink)[J.C. Vaught · EMCH 574 · 2 October 2026 #h(1fr) #counter(page).display()]
])
#set text(font:"Libertinus Serif",size:10.7pt,fill:ink)
#set par(justify:true,leading:0.52em,spacing:0.6em)
#set heading(numbering:none)
#show heading: it => block(above:8pt,below:4pt,text(font:"Arial",size:11.5pt,weight:"bold",fill:teal,it.body))
#show link: set text(fill:teal)
#let lead(title,body)=[#text(weight:"bold",title) #body]
#let apptitle(k,title)=[#text(font:"Arial",size:9pt,fill:teal)[TECHNICAL APPENDIX #k] #v(3pt) #text(font:"Arial",size:17pt,weight:"bold",fill:ink,title) #v(9pt)]
#let cap(body)=block(above:4pt,below:7pt,text(size:9pt,body))
#let tbl(..body)=table(stroke:0.4pt+rgb("#B8B8B8"),inset:5pt,align:left,fill:(x,y)=>if y==0 {pale}else{white},..body)
#text(font:"Arial",size:9pt,fill:teal)[EMCH 574 PROJECT PROPOSAL · J.C. VAUGHT]
#v(5pt)
#text(font:"Arial",size:21pt,weight:"bold",fill:ink)[Limits of Whole-Scan Attitude Correction in High-Resolution Marine Radar]
#v(7pt)
#rect(width:100%,fill:pale,stroke:none,inset:7pt)[#text(size:10pt)[A decision rule for when one vessel pose per rotating scan is sufficient, when time-resolved correction helps, and when radar coverage limits the result.]]
#v(7pt)

#lead[Decision problem.][A rotating radar image samples different directions at different times. Applying one vessel pose to the complete scan therefore mixes platform motion with scene geometry. For small autonomous surface vessels, oscillatory roll and pitch also change which targets enter the vertical beam. A sharper corrected image cannot restore a target that was never illuminated. The sponsor needs a defensible operating envelope before investing in more elaborate motion compensation.]

#lead[Proposed test.][I will test whether scan duration relative to the vessel’s oscillation period, angular rate, target range, and sensor lever arm predict when midpoint correction exceeds the mapping tolerance. MATLAB will solve damped, forced roll and pitch oscillators and a heave sensitivity model, then propagate each radar ray through its acquisition-time pose. Controlled sweeps will compare one midpoint pose, time-resolved horizontal motion, and time-resolved attitude with lever-arm translation. Known target planes will support exact synthetic geometry; unknown elevation will be reported as uncertainty. The contribution is a correction-limit map, rather than a claim to invent marine radar motion compensation. #link("https://doi.org/10.1029/2018JC013769")[Lund et al. (2018)] already corrected horizontal motion pulse by pulse and omitted vertical motions at their coarser resolution.]

#lead[Validation and scope.][A selective CANOE pilot will use per-azimuth timestamps, raw inertial measurements, calibration, and repeated-route radar observations. Its Navtech RAS6 operates at 76–77 GHz, so the pilot tests scan geometry without establishing X-band sea-clutter performance. One traversal will set processing choices; a second will remain held out. Frozen shoreline targets will measure relative landmark consistency, with median and 95th-percentile errors, radial and cross-range residuals, target persistence, and runtime. Independent surveyed targets will support absolute accuracy only if available. Post-processed navigation poses will define a separately labeled oracle comparison, never validate themselves. I will flag midpoint correction when its 95th-percentile error exceeds one range bin or a declared mission tolerance and exceeds reference and feature uncertainty. Range-bin size will remain distinct from angular resolving power.]

#lead[Sponsor value and delivery.][The result will tell the sponsor whether added pose processing improves usable imagery, whether a wider beam or faster scan is needed, or whether the present method already meets the requirement. By October 7, I will freeze the model and benchmark protocol. By October 30, I will complete the MATLAB sensitivity study and data audit. By November 20, I will complete the held-out pilot; by December 2, I will deliver the report, reproducible MATLAB source, correction-limit plots, and a sensor-selection rule. Simulation remains a complete course endpoint if the lake data lack strong motion. A later publication would add independently surveyed targets, characterized antenna patterns, and rough-water X-band trials.]

#pagebreak()
#apptitle[A][Mechanics and acquisition geometry]
The proposal’s operating envelope starts with a mechanical response, because platform attitude depends on both forcing and vessel dynamics. Each uncoupled roll or pitch mode $theta_j$ obeys the rotational oscillator below. Its inertia $I_j$, damping $c_j$, restoring stiffness $k_j$, and forcing moment $M_j$ determine the natural frequency $omega_(n,j)$ and damping ratio $zeta_j$. A translational heave mode uses mass in place of inertia. These are controlled model parameters, not identified CANOE hull properties.
$ I_j (d^2 theta_j)/(d t^2) + c_j (d theta_j)/(d t) + k_j theta_j = M_(0,j) sin(omega t + phi_j), quad omega_(n,j)=sqrt(k_j/I_j), quad zeta_j=c_j/(2 sqrt(k_j I_j)). $
The steady response links forcing frequency to acquisition distortion through its gain and lag. With $u=omega/omega_n$, the response amplitude $A_j$ is governed by
$ A_j/(M_(0,j)/k_j)=1/sqrt((1-u^2)^2+(2 zeta_j u)^2), quad delta_j="atan2"(2 zeta_j u,1-u^2). $
#align(center,schematic())
#cap[Figure A1. Original acquisition schematic. Mechanical forcing changes ray-time attitude and the radar origin through the lever arm. The dashed midpoint boresight represents the approximation under test. Beam motion occurs before coordinate correction. The schematic is not to scale.]

The preceding response provides poses at ray times $t_i$. Let $bold(R)_i$ rotate radar-frame vectors into world coordinates, $bold(s)_i$ be the radar origin, $rho_i$ the measured slant range, and $alpha_i$ the measured azimuth. The inertial origin $bold(p)_i$, vessel rotation $bold(R)_(b,i)$, and inertial-to-radar lever arm $bold(ell)$ give $bold(s)_i=bold(p)_i+bold(R)_(b,i)bold(ell)$. A radar return belongs to the family
$ bold(q)_i(epsilon)=bold(s)_i+rho_i bold(R)_i (cos epsilon cos alpha_i, cos epsilon sin alpha_i, sin epsilon)^T. $
The return does not measure elevation $epsilon$. A known target plane supplies a conditional solution; otherwise the finite beam defines a set of possible locations. The model will reject missing illumination rather than fill it with corrected intensities. Roll and pitch generally create first-order elevation changes, while near-horizontal map error can be second order or depend on target height. Consequently, the general ray-displacement bound $rho_i Delta theta+norm(bold(ell))Delta theta+abs(Delta h)$ will never be reported as measured horizontal error.

#pagebreak()
#apptitle[B][Computed sensitivity example]
The mechanics above already yields a reproducible stress calculation. The assumed natural frequency is $f_n=0.6$ Hz, damping ratio is $zeta=0.15$, static pitch deflection is $M_0/k=2 degree$, and roll forcing is 60% of pitch with a $60 degree$ phase offset. A 0.25 s scan samples 400 ray directions. The inertial origin is 1.2 m above a flat target plane, with $bold(ell)=(0.6,0,0.8)$ m. Translation, yaw, and independent heave are zero. Pitch forcing is $sin(2 pi f t)$ with the scan midpoint at $t=0$; roll forcing leads by $60 degree$. The proposed benchmark will also sweep scan phase.
#align(center,response())
#cap[Figure B1. Computed forced-response gain. Resonance amplifies the angular response and changes its phase relative to forcing. The parameters are illustrative and have not been fitted to a measured vessel.]
#align(center,error())
#cap[Figure B2. Computed maximum horizontal error over one configured 400-ray scan at the specified forcing phase. Each ray’s true point is obtained from its slant range, azimuth, true pose, and the known plane. Reconstructing the same observation with the midpoint pose produces the displayed error. The dotted line is one range bin. This is a sampling-normalized diagnostic, not the radar’s two-dimensional resolving power. No beam mask is applied to this geometric envelope.]

At $f/f_n=1$, the maximum midpoint error is 0.405 m at 100 m and 1.138 m at 300 m. Exact per-ray reconstruction of the same known plane gives zero error by construction; it is an algebra check, not experimental validation. In a separate idealized hard beam gate at 100 m, only 18.5% of sampled plane intersections fall within a $3.6 degree$ vertical beam, versus 100% within $21.8 degree$. These illustrative widths are manufacturer-listed options; the dataset’s actual antenna pattern is unverified. A hard gate omits gain, clutter, sidelobes, and thresholding, so this fraction is geometric availability, not measured detection probability. @Navtech2024RAS6

#pagebreak()
#apptitle[C][Benchmark and delivery protocol]
The controlled study must first establish where geometry causes error. Its parameter grid will vary roll and pitch amplitude, phase, forcing frequency, scan duration, heave, range, target height, timing offset, lever arm, and vertical beam width. Synthetic truth will contain fixed shoreline and plane targets with an explicit visibility gate. A single target set and intensity rule will serve every correction method so resampling and detection changes cannot masquerade as geometric improvement.
#text(size:9.4pt)[
#tbl(columns:(1.2fr,2.1fr,2.1fr),
 [Method],[Information used],[Purpose and boundary],
 [Midpoint],[One pose for the complete scan.],[Practical baseline. Same gridding and target extraction.],
 [Per-ray horizontal],[Ray-time horizontal translation and yaw. Roll, pitch, height remain fixed.],[Established deskew control. Isolates the added attitude contribution.],
 [Per-ray attitude],[Raw inertial attitude change and calibrated lever arm. Same horizontal-motion input.],[Operational candidate. Bias, interpolation, and target-elevation assumptions remain visible.],
 [Full-pose oracle],[Post-processed ray-time reference trajectory.],[Geometric upper bound under the same target model. Not an independently validated operational result.],
)]

The CANOE data reference documents a 4 Hz RAS6, 400 azimuths per scan, ray timestamps and encoder values, 100 Hz raw inertial measurements without bias correction, and per-sensor post-processed poses. Long-range and short-range modes use 0.292 and 0.0438 m/bin; each sequence’s configuration must be checked before processing. The radar range offset is −0.408 m. The radar-to-lidar transform combines CAD translation with calibrated yaw; pitch and roll extrinsic uncertainty must be tested. @UTIAS2026CANOE

This public metadata establishes feasibility, while the radar payload remains a planned selective download. A development traversal will set target extraction, bias treatment, calibration, and thresholds. The held-out repeated traversal will receive frozen settings. Gravity-aided attitude estimation will be tested under acceleration; over each scan, gyro interpolation will respect rotation geometry and the actual timestamps. Raw inertial data alone do not provide reliable absolute position or unconstrained heave, so the first real-data test isolates attitude on a common horizontal trajectory. That reference-assisted test will be labeled separately from any later operational navigation system.

Performance will be reported in meters, range-bin units, and cross-range angular-sample units, with errors conditioned on range and angular rate. Scan-level bootstrap intervals will accompany median and 95th-percentile landmark residuals. A separate-traversal landmark map measures relative consistency; an independently surveyed map is required for absolute accuracy. Visibility and persistence will be reported alongside residuals so dropping difficult returns cannot appear to improve correction. Clock-offset, extrinsic, beam-width, and elevation sweeps will expose error floors.
#text(size:9.4pt)[
#tbl(columns:(1fr,4fr),
 [Completion],[Reviewable course output],
 [October 7],[Proposal, oscillator equations, explicit target geometry, frozen benchmark plan.],
 [October 30],[MATLAB model, convergence and inverse-geometry checks, sensitivity plots, selective-data audit.],
 [November 20],[Development/held-out pilot, uncertainty and visibility results, practical decision thresholds.],
 [December 2],[Final PDF, MATLAB reproduction scripts, data manifest, figures, and correction-limit decision map.],
)]

The sponsor receives an engineering decision even if all measured lake motion lies below the threshold. The report will then bound the demonstrated operating range and preserve the stronger synthetic stress cases as predictions requiring later rough-water validation.

#pagebreak()
#apptitle[D][Prior work and defensible contribution]
The benchmark follows established motion correction and asks a narrower question about its operating limits. The sources below prevent broad novelty claims while defining a useful course-scale contribution.
#text(size:9.1pt)[
#tbl(columns:(1.1fr,2.2fr,2.3fr),
 [Prior work],[Established contribution],[Implication for this proposal],
 [McCann and Bell, 2018. @McCann2018Calibration],[Calibrates azimuth, range, and time offsets through sharpness of integrated X-band images. Acknowledges lever arm, pitch, roll, and heave errors.],[Attitude-induced map error is established. This project quantifies when a whole-scan approximation is adequate.],
 [Lund et al., 2018. @Lund2018Arctic],[Georeferences X-band echoes pulse by pulse using heading and position. Omits vertical motions under a 7.5 m range-resolution rationale.],[Per-ray horizontal correction is a required baseline. Test the resolution-dependent omission assumption.],
 [Burnett et al., 2021. @Burnett2021Motion],[Studies motion distortion and Doppler compensation in planar spinning-radar vehicle navigation.],[Scan-time distortion is established. Marine vertical geometry and coverage constrain the extension.],
 [Xie et al., 2019. @Xie2019Vertical],[Conference title and authors establish a study of vertical motion and X-band significant-wave-height estimation.],[Full text was unavailable. Do not infer methods, results, or claim a resolved gap against this work.],
 [CN106772285A, 2017. @Wang2017Preprocessing],[Patent describes roll/pitch/heave/surge-informed echo shifting and interpolation; it also models ship response.],[Strong prior art against generic attitude correction novelty. Patent translation is not peer-reviewed validation.],
)]

The proposed contribution is a reproducible adequacy test combining mechanical response, ray-time geometry, elevation ambiguity, and lost illumination. It will establish a bounded correction regime on controlled targets and test observable parts of that regime on held-out public data. Radio-frequency backscatter inversion, sea-state estimation, and claims of a first six-degree-of-freedom correction are outside the course endpoint. Publication would require an expanded full-text review and independent rough-water measurements.

#set text(size:8.7pt)
#set par(leading:0.4em,spacing:0.3em)
#bibliography("references.bib",style:"ieee",title:[References])
