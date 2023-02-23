Option Explicit
Public Function countHits(results, expected As String, VCIDs As Range, SFRs As Range) ' 'SFRS, RelSFRS)
Dim varArray() As String
Dim R1, R2 As Range
Dim NumberOfValues, VCIDsSize As Integer
Dim i, j As Integer
Dim tmpSTR As String
Dim hits As Integer
Dim sstring As String
VCIDsSize = VCIDs.Cells().Count
hits = 0

varArray = Split(results, ";")

NumberOfValues = UBound(varArray) + 1
For i = 0 To NumberOfValues - 1
sstring = getSFRSfromIds(varArray(i), VCIDs, SFRs)
'Debug.Print varArray(i); " ->"; sstring
'Debug.Print "is "; expected; " in "; sstring
If (InStr(1, sstring, Trim(expected)) <> 0) Then
Debug.Print expected; " found in "; sstring
hits = hits + 1
End If
Next i

countHits = hits

End Function

Private Function getSFRSfromIds(VCID As String, VCIDs As Range, SFRs As Range)
Dim i, VCIDsSize As Integer
Dim tmp As String
tmp = ""
VCIDsSize = VCIDs.Cells().Count
For i = 1 To VCIDsSize
If VCID = VCIDs.Cells(i, 1) Then
tmp = SFRs.Cells(i, 1)
Exit For
End If
Next i
getSFRSfromIds = tmp
End Function
