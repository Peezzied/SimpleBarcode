Sub receiveSub()
    Dim barcode As String
    Dim rng As Range
    Dim rown, lrow As Long
    Dim colNum As Long
    Dim qty As Long
    Dim ws As Worksheet
    Dim combinedRow As Long
    
    ' Sheet8 is Scan (panel)
    ' Sheet2 is inv (where barcodes are listed)
    ' Sheet3 is outgoing (records from panel)
    
    barcode = ExtractNumberFromOriginalString(Sheet8.Cells(31, 2), 2)
    qty = ExtractNumberFromOriginalString(Sheet8.Cells(31, 2), 1)
    
    
    ' Is there a barcode?
    If barcode = "" Then Exit Sub
    'Is there a qty
    If qty < 1 Then Exit Sub
    
    Sheet8.Activate
    Application.ScreenUpdating = False
    
    If barcode <> "" Then
        ' Search for the barcode on the inventory sheet.
        Call Clear
        For Each ws In ThisWorkbook.Worksheets
            If ws.Name <> "scan" Then
                Set rng = ws.Columns("A:A").Find(what:=barcode, LookIn:=xlFormulas, LookAt:=xlWhole, SearchOrder:=xlByRows, SearchDirection:=xlNext, MatchCase:=False, SearchFormat:=False)
                
                If Not rng Is Nothing Then
                    ' The barcode was found in the current worksheet
                    ' Perform further operations with the found cell
                    
                    ' Example: Print the sheet name and address of the found cell
                    Debug.Print "Sheet Name: " & ws.Name
                    Debug.Print "Found Cell Address: " & rng.Address
                    Debug.Print "qty: " & qty
                    
                    ' Exit the loop since the barcode was found
                    Exit For
                End If
            End If
        Next ws
        
        ' Send an error message if you do not find it.
        If rng Is Nothing Then
            MsgBox "number not found"
            GoTo ende
        Else
            ' Determine which row has the barcode.
            rown = rng.Row
            
            If qty >= 1 Then
                ' Add the qty to the columns.
                '4 is D

                If ws.Name = "MEDICAL SUPPLY" Or ws.Name = "BRANDED-SYRUP SUSPENSION" Then
                    ' Change the cell reference to Column 5 (E)
                    colNum = 5
                ElseIf ws.Name = "GALENICALS" Or ws.Name = "BRANDED MED" Then
                    ' Change the cell reference to Column 6 (F)
                    colNum = 6
                Else
                    ' Keep the original code (D)
                    colNum = 4
                End If
                
                ' Check if the record already exists (same sheet, barcode, qty, date, and time)
                combinedRow = FindCombinedRow(ws.Name, barcode, qty)
                Sheets(ws.Name).Cells(rown, colNum).Value = Sheets(ws.Name).Cells(rown, colNum).Value + qty
                If combinedRow = 0 Then ' Record not found, create a new one
                    lrow = Sheet8.Cells(Rows.Count, 4).End(xlUp).Row + 1
                
                    
                    
                    ' Copy the description information.
                    Sheet8.Activate
                    Sheet8.Cells(lrow, 4).Value = ws.Name
                    Sheet8.Hyperlinks.Add Anchor:=Sheet8.Cells(lrow, 5), Address:="", _
                        SubAddress:=ws.Name & "!" & rng.Address, TextToDisplay:=Sheets(ws.Name).Cells(rown, 2).Value

                    ' Enter the barcode and the qty information.
                    Sheet8.Cells(lrow, 6).Value = barcode
                    Sheet8.Cells(lrow, 7).Value = qty

                    ' Enter the date and time for when this happened.
                    Sheet8.Cells(lrow, 8) = Date & " " & Time
                    Sheet8.Cells(lrow, 8).NumberFormat = "h:mm:ss AM/PM"

                    ' Enter price
                    Sheet8.Cells(lrow, 9).Value = Sheets(ws.Name).Cells(rown, 18).Value
                Else ' Record found, update the existing row
                    Debug.Print combinedRow
                    Sheet8.Cells(combinedRow, 7).Value = Sheet8.Cells(combinedRow, 7).Value + qty
                End If

            End If
        End If
    End If
            
    
ende:
    ' Turn off the marching ants.
    Application.CutCopyMode = False
    Sheet8.Activate
    
    ' Clear the cells on the scan sheet.
    Sheet8.Cells(31, 2).ClearContents
    Sheet8.Cells(31, 3).ClearContents
    
    ' Select the qty cell on the scan sheet.
    ActiveWorkbook.Sheets("SALES HUB").Activate
    Sheets("SALES HUB").Range("B31").Select '(and activate)
    
End Sub

Function FindCombinedRow(sheetName As String, barcode As String, qty As Long) As Long
    Dim ws As Worksheet
    Dim i As Long
    
    i = Sheet8.Cells(Rows.Count, 4).End(xlUp).Row
    Debug.Print "lrow is " & i
    
    If Sheet8.Cells(i, 6).Value = barcode Then

        FindCombinedRow = i ' Return the row number where the record is found
           
        Exit Function
    End If
    
    FindCombinedRow = 0 ' If record not found, return 0
End Function
Function ExtractNumberFromOriginalString(originalString As Variant, optionAs As Integer) As Variant
    Dim output As Variant
    Dim plusPosition As Variant

    ' Find the position of the "+" sign
    plusPosition = InStr(originalString, "+")

    If plusPosition > 0 Then
        ' Extract the number part after the "+" sign
        If optionAs = 1 Then
            output = Mid(originalString, plusPosition + 1)
        End If
        If optionAs = 2 Then
            output = Left(originalString, plusPosition - 1)
        End If
        Debug.Print "original " & originalString
        Debug.Print "numberPart " & output
    Else
        ' If "+" sign is not found, set 'result' to -1 to indicate an error or not found
        output = -1
    End If

    ' Return the extracted number or -1 if "+" sign is not found
    ExtractNumberFromOriginalString = output
    Debug.Print "the result is " & output
End Function




