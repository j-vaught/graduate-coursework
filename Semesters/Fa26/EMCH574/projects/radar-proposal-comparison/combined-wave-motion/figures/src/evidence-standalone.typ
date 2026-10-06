#import "evidence-plots.typ": visibility, raytime, measured, survival
#set page(width:auto,height:auto,margin:2mm)
#show math.equation: set text(font: "Latin Modern Math")
#set text(font:"Latin Modern Roman",size:8.8pt)
#let choices=(visibility:visibility,raytime:raytime,measured:measured,survival:survival)
#let selected=choices.at(sys.inputs.at("plot",default:"visibility"))
#selected()
