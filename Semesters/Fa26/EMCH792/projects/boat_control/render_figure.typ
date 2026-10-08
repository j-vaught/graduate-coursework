#import "figures.typ" as f
#import "hardware_figures.typ" as hw
#set page(width: 7in, height: auto, margin: 0.15in)
#set text(font: ("Times New Roman", "New Computer Modern"), size: 10pt)
#let choices = (
  hull: f.hull, feedback: f.feedback, equal: f.equal-step,
  differential: f.differential, turning-path: f.turning-path,
  pulse: f.pulse, decay: f.decay, phase: f.phase-pair,
  wind: f.wind, schedule: f.schedule, blind: f.blind, overlays: f.overlays,
  lowlevel: hw.lowlevel, timing: hw.timing, motor: hw.motor, boat-response: hw.boat-response,
  sensors: hw.sensor-response, camera: hw.camera-response,
)
#align(center, choices.at(sys.inputs.at("figure", default: "hull"))())
