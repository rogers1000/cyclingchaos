# cyclingchaos
A cycling data package built by CyclingChaos (CyclingChaos.co.uk) where you will be able to look at:
- Race Calendars
- Race Results
- Team Rosters
- Rider Details

Currently there is a four phase iteration delivery process:
- Phase 1 is basics (done)
- Phase 2 is building basic package functions (done)
- Phase 3 is adding backend data capability (done)
- Phase 4 is adding frontend data capability (done)
- Phase 5 is rebuiling ingestion methodology (started on)
- Phase 6 is adding backend data capability
- Phase 7 is adding frontend data capability

Any questions, please don't hesistate to message me. 

Race Calendar Function:
- `Season`
- `Gender`
- `Category`
- `First Cycling Race ID`
- `Race_Name`
- `First Cycling Race Nationality ID`
- `UCI Race Category`
- `Stage Race Boolean`
- `Start Date`
- `End Date`
- `Race Tags`
- `Stage Profile Category` (for Stage Races)
- `Distance` (for Stage Races)
- `Route` (for Stage Races)

Race Result Function:
- `Season`
- `Gender`
- `Category`
- `First Cycling Race ID`
- `Race Name`
- `Stage`
- `Bib Number`
- `First Cycling Rider ID`
- `First Cycling Team ID`
- `Position`
- `Stage/GC Time`

Team Details Function
- `Season`
- `First Cycling Team ID`
- `Team Name`
- `UCI Division`

Race Results Pivot Table Functionality:
- Dynamic `Season` Filter
- Dyanmic `Gender` Filter
- Dynamic `Pivot Slicer` (Team or Rider)
- Dynamic `Race Filter` (`Race Tags`, `Rider` raced in, `Team` raced in, `Individual Stage Race`) 
- Dynamic `Value Slicer` (`Position`, `GC Time`, `GC Time from Leader`)
- Dynamic `Race Location Filter`
- Dynamic `UCI Race Classification Filter` (World Tour only atm)
- Dynamic `Stage Race Boolean Filter`
- Dynamic Table Sort (`Average Position` and `GC Time`)
- Overview of `Pivot_ID`, `Stage`, `Average Position`, `GC Time`, `GC Time from Leader`, `Races Finished`, `Races Started` as well as values from selected races.

FantasyFives Function:
- CSV Import and Transform capability
- Dynamic `Season` Filter
- Dynamic `Race ID` Filter
- Dynamic Max Score Parameter
