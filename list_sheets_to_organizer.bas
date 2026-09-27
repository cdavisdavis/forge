Attribute VB_Name = "OrganizerTools"
Option Explicit

' Builds a new "organizing" workbook listing every sheet name in the
' workbook that is active when you run it, one per row down column A.
' The new workbook starts clean: all-white fill, no gridlines.
' Saves the organizer and a copy of the original into OUT_DIR.

Private Const OUT_DIR As String = "C:\Users\chris\a_Claude_Main\___tools\a_  spread_sheet_management_\"

Public Sub ListSheetsToOrganizer()
    Dim src As Workbook
    Dim org As Workbook
    Dim ws As Worksheet
    Dim sh As Object
    Dim r As Long
    Dim stamp As String
    Dim baseName As String
    Dim copyPath As String
    Dim orgPath As String

    Set src = ActiveWorkbook
    stamp = Format(Now, "yyyymmdd_hhnn")
    baseName = Left(src.Name, InStrRev(src.Name, ".") - 1)

    If Dir(OUT_DIR, vbDirectory) = "" Then MkDir OUT_DIR

    ' Copy of the original, untouched (the open file keeps its own path).
    copyPath = OUT_DIR & "orig_copy__" & stamp & "__" & src.Name
    src.SaveCopyAs copyPath

    Set org = Workbooks.Add(xlWBATWorksheet)   ' one blank sheet
    Set ws = org.Worksheets(1)
    ws.Name = "sheet_list"
    CleanSheet ws

    ws.Range("A1").Value = "sheet_name"
    ws.Range("A1").Font.Bold = True

    r = 2
    For Each sh In src.Sheets                  ' includes chart sheets and hidden sheets
        ws.Cells(r, 1).Value = sh.Name
        r = r + 1
    Next sh

    ws.Columns("A").AutoFit
    ws.Range("A2").Select

    ' Never overwrite an organizer you may have already marked up.
    orgPath = OUT_DIR & baseName & "__organizer.xlsx"
    If Dir(orgPath) <> "" Then orgPath = OUT_DIR & baseName & "__organizer__" & stamp & ".xlsx"
    org.SaveAs Filename:=orgPath, FileFormat:=xlOpenXMLWorkbook

    MsgBox (r - 2) & " sheets listed from " & src.Name & "." & vbCrLf & vbCrLf & _
           "Organizer:  " & orgPath & vbCrLf & _
           "Original copy:  " & copyPath, _
           vbInformation, "Organizer"
End Sub

' Start-clean formatting: white fill on every cell, gridlines off.
' Reuse this on any new sheet: CleanSheet ActiveSheet
Public Sub CleanSheet(ByVal ws As Worksheet)
    ws.Cells.Interior.Color = vbWhite
    ws.Activate
    ActiveWindow.DisplayGridlines = False
End Sub

' Run this directly (Alt+F8) to clean whatever sheet you're on.
Public Sub CleanActiveSheet()
    CleanSheet ActiveSheet
End Sub
