\ Model workforce5
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize multi-objectives
  TotalSlack: Priority=2 Weight=1 AbsTol=2 RelTol=0.1
   totSlack
  Fairness: Priority=1 Weight=1 AbsTol=0 RelTol=0
   - minShift + maxShift
Subject To
 shiftRequirement[Mon1]: x[Amy,Mon1] + x[Bob,Mon1] + x[Cathy,Mon1]
   + x[Dan,Mon1] + x[Ed,Mon1] + x[Fred,Mon1] + x[Gu,Mon1] + x[Tobi,Mon1]
   + Slack[Mon1] = 3
 shiftRequirement[Tue2]: x[Amy,Tue2] + x[Bob,Tue2] + x[Cathy,Tue2]
   + x[Dan,Tue2] + x[Ed,Tue2] + x[Fred,Tue2] + x[Gu,Tue2] + x[Tobi,Tue2]
   + Slack[Tue2] = 2
 shiftRequirement[Wed3]: x[Amy,Wed3] + x[Bob,Wed3] + x[Cathy,Wed3]
   + x[Dan,Wed3] + x[Ed,Wed3] + x[Fred,Wed3] + x[Gu,Wed3] + x[Tobi,Wed3]
   + Slack[Wed3] = 4
 shiftRequirement[Thu4]: x[Amy,Thu4] + x[Bob,Thu4] + x[Cathy,Thu4]
   + x[Dan,Thu4] + x[Ed,Thu4] + x[Fred,Thu4] + x[Gu,Thu4] + x[Tobi,Thu4]
   + Slack[Thu4] = 4
 shiftRequirement[Fri5]: x[Amy,Fri5] + x[Bob,Fri5] + x[Cathy,Fri5]
   + x[Dan,Fri5] + x[Ed,Fri5] + x[Fred,Fri5] + x[Gu,Fri5] + x[Tobi,Fri5]
   + Slack[Fri5] = 5
 shiftRequirement[Sat6]: x[Amy,Sat6] + x[Bob,Sat6] + x[Cathy,Sat6]
   + x[Dan,Sat6] + x[Ed,Sat6] + x[Fred,Sat6] + x[Gu,Sat6] + x[Tobi,Sat6]
   + Slack[Sat6] = 6
 shiftRequirement[Sun7]: x[Amy,Sun7] + x[Bob,Sun7] + x[Cathy,Sun7]
   + x[Dan,Sun7] + x[Ed,Sun7] + x[Fred,Sun7] + x[Gu,Sun7] + x[Tobi,Sun7]
   + Slack[Sun7] = 5
 shiftRequirement[Mon8]: x[Amy,Mon8] + x[Bob,Mon8] + x[Cathy,Mon8]
   + x[Dan,Mon8] + x[Ed,Mon8] + x[Fred,Mon8] + x[Gu,Mon8] + x[Tobi,Mon8]
   + Slack[Mon8] = 2
 shiftRequirement[Tue9]: x[Amy,Tue9] + x[Bob,Tue9] + x[Cathy,Tue9]
   + x[Dan,Tue9] + x[Ed,Tue9] + x[Fred,Tue9] + x[Gu,Tue9] + x[Tobi,Tue9]
   + Slack[Tue9] = 2
 shiftRequirement[Wed10]: x[Amy,Wed10] + x[Bob,Wed10] + x[Cathy,Wed10]
   + x[Dan,Wed10] + x[Ed,Wed10] + x[Fred,Wed10] + x[Gu,Wed10]
   + x[Tobi,Wed10] + Slack[Wed10] = 3
 shiftRequirement[Thu11]: x[Amy,Thu11] + x[Bob,Thu11] + x[Cathy,Thu11]
   + x[Dan,Thu11] + x[Ed,Thu11] + x[Fred,Thu11] + x[Gu,Thu11]
   + x[Tobi,Thu11] + Slack[Thu11] = 4
 shiftRequirement[Fri12]: x[Amy,Fri12] + x[Bob,Fri12] + x[Cathy,Fri12]
   + x[Dan,Fri12] + x[Ed,Fri12] + x[Fred,Fri12] + x[Gu,Fri12]
   + x[Tobi,Fri12] + Slack[Fri12] = 6
 shiftRequirement[Sat13]: x[Amy,Sat13] + x[Bob,Sat13] + x[Cathy,Sat13]
   + x[Dan,Sat13] + x[Ed,Sat13] + x[Fred,Sat13] + x[Gu,Sat13]
   + x[Tobi,Sat13] + Slack[Sat13] = 7
 shiftRequirement[Sun14]: x[Amy,Sun14] + x[Bob,Sun14] + x[Cathy,Sun14]
   + x[Dan,Sun14] + x[Ed,Sun14] + x[Fred,Sun14] + x[Gu,Sun14]
   + x[Tobi,Sun14] + Slack[Sun14] = 5
 totSlack: - Slack[Mon1] - Slack[Tue2] - Slack[Wed3] - Slack[Thu4]
   - Slack[Fri5] - Slack[Sat6] - Slack[Sun7] - Slack[Mon8] - Slack[Tue9]
   - Slack[Wed10] - Slack[Thu11] - Slack[Fri12] - Slack[Sat13]
   - Slack[Sun14] + totSlack = 0
 totShifts[Amy]: - x[Amy,Mon1] - x[Amy,Tue2] - x[Amy,Wed3] - x[Amy,Thu4]
   - x[Amy,Fri5] - x[Amy,Sat6] - x[Amy,Sun7] - x[Amy,Mon8] - x[Amy,Tue9]
   - x[Amy,Wed10] - x[Amy,Thu11] - x[Amy,Fri12] - x[Amy,Sat13]
   - x[Amy,Sun14] + TotShifts[Amy] = 0
 totShifts[Bob]: - x[Bob,Mon1] - x[Bob,Tue2] - x[Bob,Wed3] - x[Bob,Thu4]
   - x[Bob,Fri5] - x[Bob,Sat6] - x[Bob,Sun7] - x[Bob,Mon8] - x[Bob,Tue9]
   - x[Bob,Wed10] - x[Bob,Thu11] - x[Bob,Fri12] - x[Bob,Sat13]
   - x[Bob,Sun14] + TotShifts[Bob] = 0
 totShifts[Cathy]: - x[Cathy,Mon1] - x[Cathy,Tue2] - x[Cathy,Wed3]
   - x[Cathy,Thu4] - x[Cathy,Fri5] - x[Cathy,Sat6] - x[Cathy,Sun7]
   - x[Cathy,Mon8] - x[Cathy,Tue9] - x[Cathy,Wed10] - x[Cathy,Thu11]
   - x[Cathy,Fri12] - x[Cathy,Sat13] - x[Cathy,Sun14] + TotShifts[Cathy]
   = 0
 totShifts[Dan]: - x[Dan,Mon1] - x[Dan,Tue2] - x[Dan,Wed3] - x[Dan,Thu4]
   - x[Dan,Fri5] - x[Dan,Sat6] - x[Dan,Sun7] - x[Dan,Mon8] - x[Dan,Tue9]
   - x[Dan,Wed10] - x[Dan,Thu11] - x[Dan,Fri12] - x[Dan,Sat13]
   - x[Dan,Sun14] + TotShifts[Dan] = 0
 totShifts[Ed]: - x[Ed,Mon1] - x[Ed,Tue2] - x[Ed,Wed3] - x[Ed,Thu4]
   - x[Ed,Fri5] - x[Ed,Sat6] - x[Ed,Sun7] - x[Ed,Mon8] - x[Ed,Tue9]
   - x[Ed,Wed10] - x[Ed,Thu11] - x[Ed,Fri12] - x[Ed,Sat13] - x[Ed,Sun14]
   + TotShifts[Ed] = 0
 totShifts[Fred]: - x[Fred,Mon1] - x[Fred,Tue2] - x[Fred,Wed3]
   - x[Fred,Thu4] - x[Fred,Fri5] - x[Fred,Sat6] - x[Fred,Sun7]
   - x[Fred,Mon8] - x[Fred,Tue9] - x[Fred,Wed10] - x[Fred,Thu11]
   - x[Fred,Fri12] - x[Fred,Sat13] - x[Fred,Sun14] + TotShifts[Fred] = 0
 totShifts[Gu]: - x[Gu,Mon1] - x[Gu,Tue2] - x[Gu,Wed3] - x[Gu,Thu4]
   - x[Gu,Fri5] - x[Gu,Sat6] - x[Gu,Sun7] - x[Gu,Mon8] - x[Gu,Tue9]
   - x[Gu,Wed10] - x[Gu,Thu11] - x[Gu,Fri12] - x[Gu,Sat13] - x[Gu,Sun14]
   + TotShifts[Gu] = 0
 totShifts[Tobi]: - x[Tobi,Mon1] - x[Tobi,Tue2] - x[Tobi,Wed3]
   - x[Tobi,Thu4] - x[Tobi,Fri5] - x[Tobi,Sat6] - x[Tobi,Sun7]
   - x[Tobi,Mon8] - x[Tobi,Tue9] - x[Tobi,Wed10] - x[Tobi,Thu11]
   - x[Tobi,Fri12] - x[Tobi,Sat13] - x[Tobi,Sun14] + TotShifts[Tobi] = 0
Bounds
 x[Amy,Mon1] = 0
 x[Cathy,Mon1] = 0
 x[Dan,Mon1] = 0
 x[Gu,Mon1] = 0
 x[Cathy,Tue2] = 0
 x[Bob,Wed3] = 0
 x[Amy,Thu4] = 0
 x[Bob,Thu4] = 0
 x[Dan,Thu4] = 0
 x[Fred,Thu4] = 0
 x[Tobi,Thu4] = 0
 x[Fred,Fri5] = 0
 x[Gu,Fri5] = 0
 x[Amy,Sat6] = 0
 x[Cathy,Sat6] = 0
 x[Ed,Sat6] = 0
 x[Bob,Sun7] = 0
 x[Dan,Sun7] = 0
 x[Fred,Sun7] = 0
 x[Amy,Mon8] = 0
 x[Gu,Mon8] = 0
 x[Bob,Tue9] = 0
 x[Bob,Wed10] = 0
 x[Ed,Wed10] = 0
 x[Fred,Wed10] = 0
 x[Fred,Thu11] = 0
 x[Bob,Fri12] = 0
 x[Ed,Fri12] = 0
 x[Gu,Fri12] = 0
 x[Bob,Sun14] = 0
Binaries
 x[Amy,Mon1] x[Bob,Mon1] x[Cathy,Mon1] x[Dan,Mon1] x[Ed,Mon1] x[Fred,Mon1]
 x[Gu,Mon1] x[Tobi,Mon1] x[Amy,Tue2] x[Bob,Tue2] x[Cathy,Tue2] x[Dan,Tue2]
 x[Ed,Tue2] x[Fred,Tue2] x[Gu,Tue2] x[Tobi,Tue2] x[Amy,Wed3] x[Bob,Wed3]
 x[Cathy,Wed3] x[Dan,Wed3] x[Ed,Wed3] x[Fred,Wed3] x[Gu,Wed3] x[Tobi,Wed3]
 x[Amy,Thu4] x[Bob,Thu4] x[Cathy,Thu4] x[Dan,Thu4] x[Ed,Thu4] x[Fred,Thu4]
 x[Gu,Thu4] x[Tobi,Thu4] x[Amy,Fri5] x[Bob,Fri5] x[Cathy,Fri5] x[Dan,Fri5]
 x[Ed,Fri5] x[Fred,Fri5] x[Gu,Fri5] x[Tobi,Fri5] x[Amy,Sat6] x[Bob,Sat6]
 x[Cathy,Sat6] x[Dan,Sat6] x[Ed,Sat6] x[Fred,Sat6] x[Gu,Sat6] x[Tobi,Sat6]
 x[Amy,Sun7] x[Bob,Sun7] x[Cathy,Sun7] x[Dan,Sun7] x[Ed,Sun7] x[Fred,Sun7]
 x[Gu,Sun7] x[Tobi,Sun7] x[Amy,Mon8] x[Bob,Mon8] x[Cathy,Mon8] x[Dan,Mon8]
 x[Ed,Mon8] x[Fred,Mon8] x[Gu,Mon8] x[Tobi,Mon8] x[Amy,Tue9] x[Bob,Tue9]
 x[Cathy,Tue9] x[Dan,Tue9] x[Ed,Tue9] x[Fred,Tue9] x[Gu,Tue9] x[Tobi,Tue9]
 x[Amy,Wed10] x[Bob,Wed10] x[Cathy,Wed10] x[Dan,Wed10] x[Ed,Wed10]
 x[Fred,Wed10] x[Gu,Wed10] x[Tobi,Wed10] x[Amy,Thu11] x[Bob,Thu11]
 x[Cathy,Thu11] x[Dan,Thu11] x[Ed,Thu11] x[Fred,Thu11] x[Gu,Thu11]
 x[Tobi,Thu11] x[Amy,Fri12] x[Bob,Fri12] x[Cathy,Fri12] x[Dan,Fri12]
 x[Ed,Fri12] x[Fred,Fri12] x[Gu,Fri12] x[Tobi,Fri12] x[Amy,Sat13]
 x[Bob,Sat13] x[Cathy,Sat13] x[Dan,Sat13] x[Ed,Sat13] x[Fred,Sat13]
 x[Gu,Sat13] x[Tobi,Sat13] x[Amy,Sun14] x[Bob,Sun14] x[Cathy,Sun14]
 x[Dan,Sun14] x[Ed,Sun14] x[Fred,Sun14] x[Gu,Sun14] x[Tobi,Sun14]
General Constraints
 minShift: minShift = MIN ( TotShifts[Amy] , TotShifts[Bob] ,
   TotShifts[Cathy] , TotShifts[Dan] , TotShifts[Ed] , TotShifts[Fred] ,
   TotShifts[Gu] , TotShifts[Tobi] )
 maxShift: maxShift = MAX ( TotShifts[Amy] , TotShifts[Bob] ,
   TotShifts[Cathy] , TotShifts[Dan] , TotShifts[Ed] , TotShifts[Fred] ,
   TotShifts[Gu] , TotShifts[Tobi] )
End
