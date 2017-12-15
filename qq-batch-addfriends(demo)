#include <File.au3>

Global $filename = "my.txt"  

HotKeySet("h", "ExitProgram")

AutoItSetOption('MouseCoordMode',0)


; 先点击 "+" 按钮 ，弹出查找好友的gui界面，
;后运行程序

LoopTXT()

Func LoopTXT()
	$file = FileOpen($filename ,0)
	If $file = -1 Then
		MsgBox(48, "Error", "Unable to open file.")
		Exit
	EndIf


	For $i = 1 to _FileCountLines($filename)
		$line = FileReadLine($filename ,$i)
		ConsoleWrite($line & @CRLF)
		Sleep(2000)
		AddFriend($line)
	Next

	FileClose($file)
EndFunc


Func AddFriend($qq)

WinActivate("查找")
MouseClick("primary",464,101,1,0)

MouseClick("primary",360,101 ,1,0)
ClipPut($qq)
Send("^v")
Sleep(1000)

MouseClick("primary",630,119,1,0) ; search button

Sleep(2000)

$color = PixelGetColor(117,309)


If Hex($color,6) == 'FFFFF' Then
	Return
EndIF

MouseClick("primary",117,309,1,0)  ;add  button
Sleep(1000)
MouseClick("primary",349,345,1,0) ;next   add auth  info
Sleep(1000)
MouseClick("primary",349,345,1,0) ;  choose the team
Sleep(2000)
WinClose("[REGEXPTITLE:添加好友]")

Sleep(1000)

EndFunc

Func ExitProgram()
	ConsoleWrite(" go to finsh" & @CRLF)
	Exit
EndFunc
