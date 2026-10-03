import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const c=JSON.parse(fs.readFileSync(path.join(root,'data/config.json'),'utf8'));
const deg=Math.PI/180;
const rx=a=>[[1,0,0],[0,Math.cos(a),-Math.sin(a)],[0,Math.sin(a),Math.cos(a)]];
const ry=a=>[[Math.cos(a),0,Math.sin(a)],[0,1,0],[-Math.sin(a),0,Math.cos(a)]];
const mv=(a,v)=>a.map(row=>row.reduce((s,x,i)=>s+x*v[i],0));
const mm=(a,b)=>a.map(row=>b[0].map((_,j)=>row.reduce((s,x,k)=>s+x*b[k][j],0)));
const add=(a,b)=>a.map((x,i)=>x+b[i]);
const trans=a=>a[0].map((_,i)=>a.map(row=>row[i]));
function pose(t, ratio){
  const gain=1/Math.hypot(1-ratio*ratio,2*c.damping_ratio*ratio);
  const lag=Math.atan2(2*c.damping_ratio*ratio,1-ratio*ratio);
  const ph=2*Math.PI*c.natural_frequency_hz*ratio*t-lag;
  const pitch=c.static_pitch_deflection_deg*deg*gain*Math.sin(ph);
  const roll=c.static_pitch_deflection_deg*deg*gain*c.roll_to_pitch_forcing_ratio*Math.sin(ph+c.roll_phase_offset_rad);
  const R=mm(ry(pitch),rx(roll));
  const s=add([0,0,c.imu_origin_height_m],mv(R,c.imu_to_radar_lever_arm_m));
  return {R,s,pitch,roll,gain};
}
// Solve range sphere + radar azimuth half-plane + known z=0 target plane.
// Select the near-horizontal elevation branch. Never treat this as measured elevation.
function pointOnPlane(rho,alpha,p){
  const a=mv(p.R,[Math.cos(alpha),Math.sin(alpha),0]);
  const b=mv(p.R,[0,0,1]);
  const L=Math.hypot(a[2],b[2]);
  const q=-p.s[2]/rho/L;
  if(Math.abs(q)>1) return null;
  const epsilon=Math.asin(q)-Math.atan2(a[2],b[2]);
  const u=a.map((x,i)=>Math.cos(epsilon)*x+Math.sin(epsilon)*b[i]);
  return {xyz:add(p.s,u.map(x=>rho*x)),epsilon};
}
const ratio=[],gain=[],error100=[],error300=[],coverageNarrow=[],coverageWide=[];
let inverseError=0;
for(let k=0;k<c.frequency_ratio_samples;k++){
  const q=c.frequency_ratio_min+(c.frequency_ratio_max-c.frequency_ratio_min)*k/(c.frequency_ratio_samples-1);
  const midpoint=pose(0,q);
  ratio.push(q); gain.push(midpoint.gain);
  const errs=[];
  for(const rho of c.illustrative_ranges_m){
    let worst=0;
    for(let j=0;j<c.azimuths_per_scan;j++){
      const alpha=2*Math.PI*j/c.azimuths_per_scan;
      const t=(j/(c.azimuths_per_scan-1)-0.5)*c.scan_period_s;
      const truth=pointOnPlane(rho,alpha,pose(t,q));
      const estimate=pointOnPlane(rho,alpha,midpoint);
      if(!truth||!estimate) throw new Error('Non-intersecting plane for configured stress study');
      worst=Math.max(worst,Math.hypot(truth.xyz[0]-estimate.xyz[0],truth.xyz[1]-estimate.xyz[1]));
      const sensor=mv(trans(pose(t,q).R),truth.xyz.map((x,i)=>x-pose(t,q).s[i]));
      inverseError=Math.max(inverseError,Math.abs(Math.hypot(...sensor)-rho),Math.abs(Math.atan2(sensor[1],sensor[0])-Math.atan2(Math.sin(alpha),Math.cos(alpha)))*rho,Math.abs(truth.xyz[2]));
    }
    errs.push(worst);
  }
  error100.push(errs[0]/c.radar_range_bins_m[0]);
  error300.push(errs[1]/c.radar_range_bins_m[1]);
  const visible=c.illustrative_elevation_beamwidths_deg.map(beta=>{
    let seen=0;
    for(let j=0;j<c.azimuths_per_scan;j++){
      const alpha=2*Math.PI*j/c.azimuths_per_scan;
      const t=(j/(c.azimuths_per_scan-1)-0.5)*c.scan_period_s;
      const truth=pointOnPlane(100,alpha,pose(t,q));
      if(Math.abs(truth.epsilon)<=beta*deg/2) seen++;
    }
    return seen/c.azimuths_per_scan;
  });
  coverageNarrow.push(visible[0]);coverageWide.push(visible[1]);
}
if(inverseError>1e-9)throw new Error(`Inverse consistency failure ${inverseError}`);
const output={config:c,ratio,gain,error100,error300,coverageNarrow,coverageWide};
fs.writeFileSync(path.join(root,'data/analytical.json'),JSON.stringify(output,null,2)+'\n');
const selected=[0.5,1.0,1.5].map(q=>{
  const i=ratio.reduce((best,x,k)=>Math.abs(x-q)<Math.abs(ratio[best]-q)?k:best,0);
  return {frequency_ratio:ratio[i],gain:gain[i],max_horizontal_error_m_100:error100[i]*c.radar_range_bins_m[0],max_horizontal_error_m_300:error300[i]*c.radar_range_bins_m[1],visible_fraction_3_6_deg:coverageNarrow[i],visible_fraction_21_8_deg:coverageWide[i]};
});
const checks={status:c.status,inverse_consistency_max_error:inverseError,per_ray_known_plane_error_m:0,selected,max_gain:Math.max(...gain),max_error_ratio_100:Math.max(...error100),max_error_ratio_300:Math.max(...error300)};
fs.writeFileSync(path.join(root,'data/checks.json'),JSON.stringify(checks,null,2)+'\n');
console.log(JSON.stringify(checks,null,2));
