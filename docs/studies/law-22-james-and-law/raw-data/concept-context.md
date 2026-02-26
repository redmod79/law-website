# Raw Concept Context Data

## Note
The concept_context.py tool returned "No theological concepts found" for all James verses tested:
- JAS 1:25 -- No theological concepts found
- JAS 2:8 -- No theological concepts found
- JAS 4:11 -- No theological concepts found
- JAS 4:12 -- No theological concepts found

This is because the concept_context tool relies on Strong's number mappings to theological concepts, and the James verses in the database may not have these mappings populated.

## Alternative: Cross-Testament Parallels Used Instead
The cross_testament_parallels_v2.py tool provided the conceptual connections needed. Key findings from parallel analysis:

### Strongest NT Parallels by Verse
- **JAS 1:25** --> ROM 2:13 (0.464) -- doer/hearer/law shared vocabulary
- **JAS 2:8** --> GAL 5:14 (0.514) -- love/law/neighbor/yourself shared content
- **JAS 2:10** --> GAL 5:4 (0.398) -- law/whoever shared theme
- **JAS 2:11** --> ROM 13:9 (0.476) -- adultery/murder Decalogue citation
- **JAS 2:12** --> JAS 1:25 (0.409) -- freedom/law internal cross-reference
- **JAS 4:11** --> JAS 5:9 (0.489) -- brother/judge internal cross-reference
- **JAS 4:12** --> ACT 7:27 (0.446) -- judge/neighbor shared theme

### Internal James Cross-References (within the epistle)
The parallels tool confirms that James' law passages form an internally coherent network:
- 1:25 <--> 2:12 (freedom + law)
- 1:25 <--> 4:11 (doer + law)
- 2:11 <--> 2:9 (transgressor + law)
- 4:11 <--> 4:12 (judge + law)
- 4:11 <--> 5:9 (brother + judge)
