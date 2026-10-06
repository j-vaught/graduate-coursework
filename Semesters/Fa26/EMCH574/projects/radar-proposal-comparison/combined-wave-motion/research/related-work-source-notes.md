# Related-work source notes

## Panagopoulos and Soraghan (2004)

Primary record. IEEE Xplore DOI `https://doi.org/10.1109/TGRS.2004.827259`. The indexed abstract states that the paper presents three techniques for suppressing unwanted sea-clutter radar echo and detecting small targets without prior knowledge of ocean and environmental conditions. The techniques are signal averaging, time-frequency representation, and morphological filtering, demonstrated with real marine radar data operating in staring mode. The accessible record supplied the abstract but not page-level full text, so the prose uses only those claims and does not assign a specific physical cause to a missed detection.

## Plant and Farquharson (2012)

Primary full text. Wiley, `https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2012JC007912`. Abstract and Sections 1, 2, and 6 distinguish geometric shadowing from partial shadowing, with partial shadowing involving polarization-dependent diffraction and weak scatterers. Section 6 reports that geometric shadowing is a poor description of low-grazing-angle deep-water microwave-backscatter dropouts, that the concealed fraction depends on incident power, and that significant polarization dependence is mainly associated with steep waves such as those near shorelines. The paper explicitly concludes that geometric shadowing does not play a role in its deep-water low-grazing-angle microwave-backscatter observations. This source does not support saying that Plant demonstrates a target-specific diffraction model.

## Wijaya and van Groesen (2016)

Primary DOI landing record. `https://doi.org/10.1016/j.oceaneng.2016.01.011`. The accessible metadata confirms the article title and its subject, determination of significant wave height from shadowing in synthetic radar images. Page-level passage was not available in the browser session. Claims in the section are therefore limited to the published geometric-shadowing and synthetic-image scope already represented by the title and the existing project citation.

## Wijaya (2017)

Primary institutional copy. `https://ris.utwente.nl/ws/files/13493346/thesis_AP_Wijaya.pdf`. The project bibliography identifies Chapter 3 as reproducing the 2016 shadowing paper, including the obstruction indicator and image-average construction. The PDF was not page-extracted in this pass, so the section avoids quoting equation numbers or numerical parameter values. It uses the dissertation only to support the relationship between geometric visibility, synthetic radar images, and wave reconstruction.

## Janssen et al. (2026)

Primary DOI landing record. `https://doi.org/10.1016/j.apor.2026.105183`. The available metadata confirms the title, “Diffraction effects in RADAR illumination of sea waves,” and the Applied Ocean Research publication. The section states only that the work calculates diffraction effects in radar illumination near and beyond wave-shadow boundaries. It deliberately does not claim that the paper models target backscatter, clutter, detector decisions, or usable observations.

## Lund et al. (2018)

Primary DOI landing record. `https://doi.org/10.1029/2018JC013769`. The current project source notes and bibliography identify the shipboard marine-radar sea-ice-drift application and its pulse-by-pulse position and heading mapping. The section uses that scope to motivate acquisition-time georeferencing and avoids assigning the paper a target-detection objective.

## Burnett, Schoellig, and Barfoot (2021)

Primary open manuscript. arXiv `https://arxiv.org/abs/2011.03512`; published DOI `https://doi.org/10.1109/LRA.2021.3052439`. The abstract states that motion distortion and Doppler effects had been ignored in prior spinning-radar navigation work, and that the paper demonstrates their effects on radar odometry using the Oxford Radar RobotCar Dataset and evaluates a lightweight estimator accounting for both effects. The proposal uses this as an acquisition-time scan-distortion result and explicitly identifies the automotive platform as different from the maritime application.

## McCann and Bell (2018)

Primary repository record with abstract and published DOI. `https://nora.nerc.ac.uk/id/eprint/519997/` and `https://doi.org/10.1109/ACCESS.2018.2814081`. The abstract states that ship-borne X-band imagery requires accurate georegistration, that finite azimuth, range, and timing offsets arise from equipment installation, and that the authors maximize sharpness of time-integrated imagery formed from time-stamped radar images and high-frequency heading and position data. The proposal uses these exact registration implications and does not claim that the method predicts target detectability.

## Integration checks

The integrated section also cites MIT OpenCourseWare's linear wave-body lecture for forcing, damping, restoring terms, response-amplitude operators, and encounter frequency. The corporate bibliography author avoids assigning lecture authorship without evidence. Primary URL. https://ocw.mit.edu/courses/2-24-ocean-wave-interaction-with-ships-and-offshore-energy-systems-13-022-spring-2002/f500bf012ed64ef2cb8e8d6f45a21bfd_lecture9.pdf.

The complete Lund author manuscript was checked during integration. Primary URL. https://faculty.washington.edu/jmt3rd/Publications/Lund_2018JC013769.pdf. Its 1.25 s rotation, 7.5 m Cartesian grid, 5 Hz navigation interpolation, and omission of heave, pitch, and roll explain the scale-dependent horizontal-motion baseline in the final text. These values describe that study, not a selected sensor for this project.

The Janssen publisher record was checked during integration. Primary URL. https://www.sciencedirect.com/science/article/pii/S014111872600266X. Its abstract expressly distinguishes the incident illumination calculation from a calculation of backscatter. The final section uses that distinction when motivating the received-target and detector stages.
