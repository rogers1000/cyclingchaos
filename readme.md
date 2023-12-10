# cyclingchaos
A cycling data package built by CyclingChaos (CyclingChaos.co.uk) where you will be able to look at:
- Race Calendars
- Race Results
- Team Rosters
- Rider Details

Currently there is a four phase iteration delivery process:
- Phase 1 is basics (done)
- Phase 2 is building basic package functions (done)
- Phase 3 is adding backend data capability
- Phase 4 is adding frontend data capability
- Phase 5 is rebuiling ingestion methodology
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
- `Race Time`

Team Details Function
- `Season`
- `First Cycling Team ID`
- `Team Name`
- `UCI Division`

Race Results Pivot Table Functionality:
- Dynamic `Season` Filter
- Dyanmic `Gender` Filter
- Dynamic `Pivot Slicer` (Team or Rider)
- Dynamic `Race Filter` (Race Tags, Rider raced in, Team raced in) 
- Dynamic `Value Slicer` (Position, GC Time, GC Time from Leader)
- Dynamic Table Sort (Average Position and Time)
- Overview of ID, Stage, Average Position, GC Time, GC Time from Leader, Races Finished, Races Started as well as values from selected races.
