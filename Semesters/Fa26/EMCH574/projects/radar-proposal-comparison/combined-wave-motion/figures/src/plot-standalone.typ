#import "plots.typ": motion, power, amplitude, beam, phase, mapping
#set page(width:auto,height:auto,margin:7mm)
#set text(font:"Arial",size:8.8pt)
#let choices=(motion:motion,power:power,amplitude:amplitude,beam:beam,phase:phase,mapping:mapping)
#let selected=choices.at(sys.inputs.at("plot",default:"motion"))
#selected()
