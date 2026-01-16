# Daily Gamecock Marketing Flyers

## Reference Code Schema

Each flyer includes a small reference code in the corner for tracking and collection purposes.

### Format
```
LOC.TOP##.MAJ.YR.x#.SEM
```

### Example
```
SWGN.REG03.ENG.JR.x1.SP26
│    │     │   │  │  └── Semester: Spring 2026
│    │     │   │  └── Quantity: 1 copy printed
│    │     │   └── Target Year: Juniors
│    │     └── Target Major: Engineering
│    └── Topic: Registration, flyer #03
└── Location: Swearingen Engineering Center
```

---

## Code Reference Tables

### Location Codes (where posted)

| Code | Building |
|------|----------|
| `GAMBRL` | Gambrell Hall |
| `LCONTE` | LeConte College |
| `CLLCTT` | Callcott (Social Sciences) |
| `SWGN` | Swearingen Engineering Center |
| `DMSB` | Darla Moore School of Business |
| `CLHIPP` | Close-Hipp (HRSM) |
| `HUMCB` | Humanities Classroom Building |
| `COKER` | Coker Life Sciences |
| `JONES` | Jones Physical Sciences |
| `WRDLAW` | Wardlaw College (Education) |
| `WMBB` | Williams Brice Nursing |
| `PHRC` | Public Health Research Center |
| `SJMC` | School of Journalism & Mass Comm |
| `SMWALT` | Sumwalt College |
| `SLOAN` | Sloan College |
| `DAVIS` | Davis College (Info Science) |
| `HAMLTN` | Hamilton (Social Work) |
| `MCMSTR` | McMaster (Art & Design) |
| `PETIGR` | Petigru College |
| `CRRELL` | Currell College |
| `COL` | Carolina Coliseum |
| `BLATT` | Blatt PE Center |
| `BTWASH` | Booker T. Washington |
| `LIBR` | Thomas Cooper Library |
| `RH` | Russell House |
| `FLINN` | Flinn Hall |
| `HONORS` | Honors Residence Hall |
| `BANDDF` | Band/Dance Building |
| `TV` | Digital Signage / TV Screen |

---

### Topic Codes

#### Academic
| Code | Topic |
|------|-------|
| `FRE` | Freshman Experience |
| `REG` | Registration / Scheduling |
| `ADV` | Advising / Major Selection |
| `GRD` | Grades / Academic Pressure |
| `PRF` | Professors / Teaching Quality |
| `ONL` | Online Classes |

#### Campus Life
| Code | Topic |
|------|-------|
| `HOU` | Housing / Dorms |
| `DIN` | Dining / Meal Plans |
| `TRN` | Transportation / Parking |
| `FAC` | Facilities / Buildings |
| `CLB` | Clubs / Organizations |
| `EVT` | Events / Programming |
| `REC` | Recreation / Intramurals |
| `SGA` | Student Government |
| `GRK` | Greek Life |
| `NIT` | Nightlife / Five Points |

#### Support & Services
| Code | Topic |
|------|-------|
| `FIN` | Financial Aid / Tuition |
| `MNH` | Mental Health / Wellness |
| `CRR` | Career Services / Jobs |
| `DIV` | Diversity / Inclusion |
| `SAF` | Safety / Security |

#### Athletics
| Code | Topic |
|------|-------|
| `ATH` | Athletics / Sports / Gameday |
| `FTB` | Football |
| `BBL` | Basketball |
| `BSB` | Baseball |
| `TGT` | Tailgating |

#### Graduation & Career
| Code | Topic |
|------|-------|
| `GRA` | Graduation / Commencement |
| `ALM` | Alumni / Networking |
| `JOB` | Job Market / Post-Grad |

#### General
| Code | Topic |
|------|-------|
| `GEN` | General / Hot Takes |
| `ADM` | Administration / Policies |

---

### Target Major Codes

| Code | Major/College |
|------|---------------|
| `UNI` | Universal (all majors) |
| `BUS` | Business |
| `ENG` | Engineering |
| `HRSM` | Hospitality, Retail & Sport Management |
| `NUR` | Nursing |
| `MUS` | Music |
| `EDU` | Education |
| `JIMC` | Journalism & Mass Communications |
| `PH` | Public Health |
| `CAS` | Arts & Sciences |
| `LAW` | Law |
| `SW` | Social Work |
| `PHARM` | Pharmacy |

---

### Target Year Codes

| Code | Year |
|------|------|
| `FR` | Freshman |
| `SO` | Sophomore |
| `JR` | Junior |
| `SR` | Senior |
| `GR` | Graduate |
| `ALL` | All years |

---

### Semester Codes

| Code | Semester |
|------|----------|
| `SP26` | Spring 2026 |
| `SU26` | Summer 2026 |
| `FA26` | Fall 2026 |
| `SP27` | Spring 2027 |
| ... | etc. |

---

### Quantity

Format: `x#` where `#` is the number of copies printed of this specific flyer.

- `x1` = 1 copy printed
- `x2` = 2 copies printed
- `x5` = 5 copies printed

---

## File Overview

| File | Description | Pages |
|------|-------------|-------|
| `Marketing_Sample_Test.tex` | Print flyer sandbox (3 pages) | 3 |
| `Marketing_TV_Sample.tex` | TV/digital signage sandbox (16:9) | 3 |
| `Marketing_Universal.tex` | Universal campus flyers | 44 |
| `Marketing_[College].tex` | College-specific flyers | varies |
| `Marketing_Main.tex` | Master compilation | all |

---

## Compiling

Requires LuaLaTeX:
```bash
lualatex Marketing_Sample_Test.tex
lualatex Marketing_TV_Sample.tex
```

Run twice to resolve references.
