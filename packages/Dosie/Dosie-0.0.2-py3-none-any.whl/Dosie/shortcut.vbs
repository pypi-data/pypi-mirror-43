Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "C:\\Users\\user\\Desktop\\Dosie.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "C:\\Python34\\lib\\site-packages\\Dosie\\Dosie.pyw"
oLink.IconLocation = "C:\\Python34\\lib\\site-packages\\Dosie\\icon.ico, 0"
oLink.Description = "Search Engine"
oLink.Save