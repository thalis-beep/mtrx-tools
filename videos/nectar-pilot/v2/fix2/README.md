# Nectar V2 — review round 2 fixes

Replacement clips for the editor's cut (`MTRX_DNCR5_Al_SA_RSANM4_Th_V1_9-16_2`), answering the
Frame.io comments of 2026-10-21. Each clip is 1080x1920, 30 fps, like the original media, so it
drops straight onto V1 in place of the old clip. Timeline positions below are from that project.

| Comment (TC) | Replace on V1 | Slot (sequence time) | New clip | Suggested in-point |
|---|---|---|---|---|
| 0:03 lift the bag a bit and struggle | shot02.mp4 | 2.867–6.733 | shot02_fix.mp4 | 0.3 s |
| 0:12 slowly lift the weight, struggle | shot04.mp4 | 10.733–13.667 | shot04_fix.mp4 | 0.6 s |
| 0:27 / 0:29 no smile; angry + disappointed | Grok clip (walk + jogger) | 26.400–32.833 | shot0910_fix.mp4 | 0.5 s |
| 0:57 not leaning in so much | shot17.mp4 | 55.500–58.233 | shot17_fix.mp4 | 1.0 s |
| 1:14 small bag slightly torn | shot22.mp4 | 73.333–76.867 | shot22_fix.mp4 | 0.0 s |
| 1:22 arms going into each other | shot24.mp4 | 80.567–84.533 | shot24_fix.mp4 | 0.6 s |
| 1:36 not how the product looks | shot28.mp4 | 95.633–97.633 | shot28_fix.mp4 | 0.5 s |
| 1:43 have him looking at himself | shot31.mp4 | 102.333–105.767 | shot31_fix.mp4 | 1.5 s |
| 1:59 looks not really correct | shot35.mp4 | 116.733–120.133 | shot35_fix.mp4 | 0.0 s |
| 2:01 show the release; ball too big | shot36.mp4 | 120.133–123.300 | shot36_fix.mp4 | 0.0 s |
| 2:03 / 2:05 clutch beers, throw out; hand gesture | shot37.mp4 | 123.300–127.867 | shot37_fix.mp4 | 0.6 s |
| 2:09 this looks off | shot38.mp4 | 127.867–130.800 | shot38_fix.mp4 | 0.5 s |

Remove the old Motion scale on 35 and 38 (129 %): the new frames are already framed tight.

Not animation (left for the edit / song):
- 0:06 "start showing this text on next scene only": "THEN CREATINE'S" (cap_008) starts at 6.500,
  the cut is at 6.733 — start it at 6.733 and extend "GIVING OUT" (cap_007) to meet it.
- 0:45 "get through to bedtime sounds off": the line "just to get through to bedtime" is sung in
  ~0.8 s and sounds rushed; only a re-sung section of the song (Suno replace section) fixes it.

Stills and job ids: `jobs.txt`.
