#import "plots.typ": axes, curve, blue, orange, green, ink
#let pub=json("../../data/published-model.json")
#let ipix=json("../../data/measured-ipix.json")

#let visibility()=axes(4,20,0,0.5,(4,8,12,16,20),(0,0.1,0.2,0.3,0.4,0.5),[Normalized range $r/lambda$],[Visibility],(
  curve(pub.rho,pub.visibility_h5,blue,[$H_r/A=5$]),
  curve(pub.rho,pub.visibility_h10,orange,[$H_r/A=10$],dash:"dashed"),
),height:37)

#let raytime()=axes(0,1,0,4,(0,0.25,0.5,0.75,1),(0,1,2,3,4),[Fraction of one 1.25 s rotation],[$E_h$ (m)],(
  curve(pub.lund.scan_fraction,pub.lund.midpoint_error_m,blue,[Midpoint pose]),
  curve(pub.lund.scan_fraction,pub.lund.per_ray_ideal_error_m,orange,[Ray-time pose],dash:"dashed"),
  curve((0,1),(0.5,0.5),green,[0.5 m tolerance],dash:"dotted"),
),height:32)

#let measured()=axes(32,132,-15,40,(40,60,80,100,120),(-10,0,10,20,30,40),[Sweep index ($times 10^3$)],[Power (dB)],(
  curve(ipix.sweep_index_thousands,ipix.primary_power_db,blue,[Target bin 9]),
  curve(ipix.sweep_index_thousands,ipix.clutter_bin4_power_db,orange,[Clutter bin 4],dash:"dashed"),
  curve((32,132),(ipix.processing.threshold_reference_db,ipix.processing.threshold_reference_db),ink,[Fixed gate],dash:"dotted"),
),height:36)

#let survival()=axes(-10,15,0,1,(-10,-5,0,5,10,15),(0,0.25,0.5,0.75,1),[Power threshold (dB relative to development clutter)],[Fraction],(
  curve(ipix.power_axis_db,ipix.primary_ccdf,blue,[Target above threshold]),
  curve(ipix.power_axis_db,ipix.clutter_ccdf,orange,[Clutter above threshold],dash:"dashed"),
  curve((ipix.processing.threshold_reference_db,ipix.processing.threshold_reference_db),(0,1),ink,[Fixed gate],dash:"dotted"),
),height:33)
