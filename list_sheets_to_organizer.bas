Attribute VB_Name = "OrganizerTools"
Option Explicit

' Builds a new "organizing" workbook listing every sheet name in the
' workbook that is active when you run it, one per row down column A.
' The new workbook starts clean: all-white fill, no gridlines.

Public Sub ListSheetsToOrganizer()
    Dim src As Workbook
    Dim org As Workbook
    Dim ws As Worksheet
    Dim sh As Object
    Dim r As Long

    Set src = ActiveWorkbook

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

    MsgBox (r - 2) & " sheets listed from " & src.Name & "." & vbCrLf & _
           "The organizer is open and unsaved - save it wherever you like.", _
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
