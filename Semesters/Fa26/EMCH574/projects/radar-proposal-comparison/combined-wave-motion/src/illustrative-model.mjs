import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const cfg = JSON.parse(fs.readFileSync(path.join(root, 'data/config.json'), 'utf8'));
const rad = Math.PI / 180;
const tau = 2 * Math.PI;
const norm = (a) => Math.hypot(...a);
const add = (a, b) => a.map((x, i) => x + b[i]);
const sub = (a, b) => a.map((x, i) => x - b[i]);
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const mv = (a, b) => a.map((row) => dot(row, b));
const tr = (a) => a[0].map((_, i) => a.map((row) => row[i]));
const rx = (a) => [[1, 0, 0], [0, Math.cos(a), -Math.sin(a)], [0, Math.sin(a), Math.cos(a)]];
const ry = (a) => [[Math.cos(a), 0, Math.sin(a)], [0, 1, 0], [-Math.sin(a), 0, Math.cos(a)]];
const mm = (a, b) => a.map((row) => b[0].map((_, j) => row.reduce((s, x, k) => s + x * b[k][j], 0)));
const naturalResponse = (f, fn, zeta) => {
  const u = f / fn;
  return { gain: 1 / Math.hypot(1 - u * u, 2 * zeta * u), lag: Math.atan2(2 * zeta * u, 1 - u * u) };
};
const k = (tau * cfg.wave_frequency_hz) ** 2 / cfg.gravity_m_s2;
const kd = [k * Math.cos(cfg.wave_heading_deg * rad), k * Math.sin(cfg.wave_heading_deg * rad)];
function wave(x, y, t) { return cfg.wave_amplitude_m * Math.cos(kd[0] * x + kd[1] * y - tau * cfg.wave_frequency_hz * t); }
function state(t, pitchScale = 1, phaseOffset = 0) {
  const f = cfg.wave_frequency_hz;
  const pr = naturalResponse(f, cfg.vessel_pitch_natural_hz, cfg.vessel_pitch_damping);
  const hr = naturalResponse(f, cfg.vessel_heave_natural_hz, cfg.vessel_heave_damping);
  const th = naturalResponse(f, cfg.target_heave_natural_hz, cfg.target_heave_damping);
  const pitch = cfg.static_pitch_deg * rad * pitchScale * pr.gain * Math.cos(tau * f * t - pr.lag + phaseOffset);
  const roll = cfg.roll_to_pitch_ratio * cfg.static_pitch_deg * rad * pitchScale * pr.gain * Math.cos(tau * f * t - pr.lag + cfg.roll_phase_deg * rad + phaseOffset);
  const heave = cfg.wave_amplitude_m * hr.gain * Math.cos(-tau * f * t + hr.lag);
  const targetHeave = cfg.wave_amplitude_m * th.gain * Math.cos(kd[0] * cfg.target_range_m - tau * f * t + th.lag);
  const rotation = mm(ry(pitch), rx(roll));
  const reference = [0, 0, cfg.radar_reference_height_m - cfg.lever_arm_m[2] + heave];
  const origin = add(reference, mv(rotation, cfg.lever_arm_m));
  const target = [cfg.target_range_m, 0, cfg.target_reference_height_m + targetHeave];
  return { pitch, roll, heave, rotation, origin, target };
}
const nominalOrigin = [cfg.lever_arm_m[0], 0, cfg.radar_reference_height_m];
const eye = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
function beamPower(origin, target, rotation, beta = cfg.vertical_beamwidth_deg) {
  const v = mv(tr(rotation), sub(target, origin));
  const epsilon = Math.atan2(v[2], Math.hypot(v[0], v[1]));
  return { power: Math.exp(-4 * Math.log(2) * (epsilon / (beta * rad)) ** 2), epsilon };
}
function diffraction(origin, target, t, samples = cfg.wave_path_samples) {
  const v = sub(target, origin);
  const range = norm(v);
  let maxNu = -Infinity;
  let minClearance = Infinity;
  for (let j = 1; j < samples; j++) {
    const r = j / samples;
    const p = add(origin, v.map((x) => r * x));
    const h = wave(p[0], p[1], t) - p[2];
    minClearance = Math.min(minClearance, -h);
    const nu = h * Math.sqrt(2 / (cfg.radio_wavelength_m * range * r * (1 - r)));
    maxNu = Math.max(maxNu, nu);
  }
  const lossDb = maxNu <= -0.78 ? 0 : 6.9 + 20 * Math.log10(Math.hypot(maxNu - 0.1, 1) + maxNu - 0.1);
  return { power: 10 ** (-lossDb / 10), maxNu, minClearance, lossDb };
}
function sample(t, pitchScale = 1, beta = cfg.vertical_beamwidth_deg, samples = cfg.wave_path_samples, phaseOffset = 0) {
  const s = state(t, pitchScale, phaseOffset);
  const b = beamPower(s.origin, s.target, s.rotation, beta);
  const bn = beamPower(nominalOrigin, s.target, eye, beta);
  const g = diffraction(s.origin, s.target, t, samples);
  const gn = diffraction(nominalOrigin, s.target, t, samples);
  const factors = { reference: bn.power ** 2, motion: b.power ** 2, wave: (bn.power * gn.power) ** 2, coupled: (b.power * g.power) ** 2 };
  return { ...s, beam: b.power, beamAngle: b.epsilon / rad, transmission: g.power, clearance: g.minClearance, maxNu: g.maxNu, factors };
}
// Conditional range/azimuth inversion uses a declared target plane, not measured elevation.
function reconstruct(rho, alpha, origin, rotation, planeHeight) {
  const a = mv(rotation, [Math.cos(alpha), Math.sin(alpha), 0]);
  const b = mv(rotation, [0, 0, 1]);
  const L = Math.hypot(a[2], b[2]);
  const q = (planeHeight - origin[2]) / (rho * L);
  if (Math.abs(q) > 1) return null;
  const epsilon = Math.asin(q) - Math.atan2(a[2], b[2]);
  return add(origin, a.map((x, i) => rho * (Math.cos(epsilon) * x + Math.sin(epsilon) * b[i])));
}
const n = Math.round(cfg.time_duration_s / cfg.time_step_s) + 1;
const trace = { t: [], waveAtVessel: [], targetHeight: [], pitch: [], roll: [], beam: [], transmission: [], referenceDb: [], motionDb: [], waveDb: [], coupledDb: [], midpointError: [] };
let inverseError = 0;
let minExposure = Infinity;
const midpoint = { maxErrorM: 0, medianErrorM: 0, description: 'Known target-height plane. Midpoint is the nearest scan midpoint. Error evaluated even if the power gate would reject the return.' };
for (let i = 0; i < n; i++) {
  const t = i * cfg.time_step_s;
  const s = sample(t);
  const v = mv(tr(s.rotation), sub(s.target, s.origin));
  const rho = norm(v);
  const alpha = Math.atan2(v[1], v[0]);
  const p = reconstruct(rho, alpha, s.origin, s.rotation, s.target[2]);
  inverseError = Math.max(inverseError, norm(sub(p, s.target)));
  const midTime = Math.round(t / cfg.scan_period_s) * cfg.scan_period_s;
  const sm = state(midTime);
  const pm = reconstruct(rho, alpha, sm.origin, sm.rotation, s.target[2]);
  const eh = Math.hypot(pm[0] - s.target[0], pm[1] - s.target[1]);
  trace.t.push(t); trace.waveAtVessel.push(wave(0, 0, t)); trace.targetHeight.push(s.target[2]);
  trace.pitch.push(s.pitch / rad); trace.roll.push(s.roll / rad);
  trace.beam.push(s.beam); trace.transmission.push(s.transmission);
  for (const name of ['reference', 'motion', 'wave', 'coupled']) trace[name + 'Db'].push(cfg.baseline_target_snr_db + 10 * Math.log10(Math.max(1e-12, s.factors[name])));
  trace.midpointError.push(eh);
  minExposure = Math.min(minExposure, s.target[2] - wave(s.target[0], s.target[1], t));
}
const sortedError = [...trace.midpointError].sort((a, b) => a - b);
midpoint.maxErrorM = Math.max(...trace.midpointError);
midpoint.medianErrorM = sortedError[Math.floor(sortedError.length / 2)];
// Uniform mechanical phase samples avoid conflating rotating-scan temporal aliasing with the power illustration.
const keys = ['reference', 'motion', 'wave', 'coupled'];
function availability(pitchScale, beta, samples = cfg.wave_path_samples, phaseOffset = 0) {
  const counts = Object.fromEntries(keys.map((key) => [key, 0]));
  for (let i = 0; i < cfg.phase_samples; i++) {
    const s = sample(i / (cfg.phase_samples * cfg.wave_frequency_hz), pitchScale, beta, samples, phaseOffset);
    for (const key of keys) {
      const snr = cfg.baseline_target_snr_db + 10 * Math.log10(Math.max(1e-12, s.factors[key]));
      if (snr >= cfg.power_threshold_snr_db) counts[key]++;
    }
  }
  return Object.fromEntries(keys.map((key) => [key, counts[key] / cfg.phase_samples]));
}
const amplitudeSweep = { staticPitch: [], reference: [], motion: [], wave: [], coupled: [] };
for (let i = 0; i <= 30; i++) {
  const a = i * 0.1;
  amplitudeSweep.staticPitch.push(a);
  const result = availability(a / cfg.static_pitch_deg, cfg.vertical_beamwidth_deg);
  for (const key of keys) amplitudeSweep[key].push(result[key]);
}
const beamSweep = { beamwidth: [], motion: [], coupled: [] };
for (let i = 0; i <= 24; i++) {
  const beta = 2 + i * 0.5;
  beamSweep.beamwidth.push(beta);
  const result = availability(1, beta);
  beamSweep.motion.push(result.motion); beamSweep.coupled.push(result.coupled);
}
const defaultAvailability = availability(1, cfg.vertical_beamwidth_deg);
const phaseSweep = { offsetDeg: [], motion: [], wave: [], coupled: [], independentProduct: [] };
for (let i = 0; i <= 36; i++) {
  const offset = -180 + i * 10;
  const result = availability(1, cfg.vertical_beamwidth_deg, cfg.wave_path_samples, offset * rad);
  phaseSweep.offsetDeg.push(offset);
  for (const key of ['motion', 'wave', 'coupled']) phaseSweep[key].push(result[key]);
  phaseSweep.independentProduct.push(result.motion * result.wave);
}
const refinedAvailability = availability(1, cfg.vertical_beamwidth_deg, cfg.wave_path_samples * 2);
const pathRefinementDelta = Math.max(...keys.map((key) => Math.abs(defaultAvailability[key] - refinedAvailability[key])));
const oscillator = naturalResponse(cfg.wave_frequency_hz, cfg.vessel_pitch_natural_hz, cfg.vessel_pitch_damping);
const checks = { status: cfg.status, waveWavelengthM: tau / k, waveSteepness: k * cfg.wave_amplitude_m, pitchGain: oscillator.gain, pitchAmplitudeDeg: cfg.static_pitch_deg * oscillator.gain, targetMinimumExposureM: minExposure, inverseConsistencyMaxErrorM: inverseError, availability: defaultAvailability, phaseCoupledMinimum: Math.min(...phaseSweep.coupled), phaseCoupledMaximum: Math.max(...phaseSweep.coupled), phaseLargestProductDifference: Math.max(...phaseSweep.coupled.map((v, i) => Math.abs(v - phaseSweep.independentProduct[i]))), refinedAvailability, pathRefinementFractionDelta: pathRefinementDelta, midpoint, timeSamples: n, phaseSamples: cfg.phase_samples };
const finite = [...trace.t, ...trace.pitch, ...trace.beam, ...trace.transmission, ...trace.coupledDb, ...trace.midpointError].every(Number.isFinite);
if (!finite || inverseError > 1e-8 || minExposure <= 0 || pathRefinementDelta > 0.025) throw new Error('Illustrative model numerical checks failed.');
fs.writeFileSync(path.join(root, 'data/illustrative.json'), JSON.stringify({ config: cfg, trace, amplitudeSweep, beamSweep, phaseSweep }, null, 2) + '\n');
fs.writeFileSync(path.join(root, 'data/checks.json'), JSON.stringify(checks, null, 2) + '\n');
console.log(JSON.stringify(checks, null, 2));
