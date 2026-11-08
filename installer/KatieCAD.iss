; Inno Setup script - Windows installer for KatieCAD
; Build:  iscc /DAppVersion=1.1.5 installer\KatieCAD.iss
#ifndef AppVersion
  #define AppVersion "1.1.5"
#endif

[Setup]
AppId={{6F3B8E1A-4C2D-4F6B-9A57-0A1B2C3D4E5F}
AppName=KatieCAD
AppVersion={#AppVersion}
AppPublisher=KatieCAD
AppPublisherURL=https://github.com/Merecete/KatieCAD
AppSupportURL=https://github.com/Merecete/KatieCAD/issues
AppUpdatesURL=https://github.com/Merecete/KatieCAD/releases
AppCopyright=MIT License
DefaultDirName={autopf}\KatieCAD
DefaultGroupName=KatieCAD
UninstallDisplayIcon={app}\KatieCAD.exe
OutputDir=..\release
OutputBaseFilename=KatieCAD-{#AppVersion}-Windows-Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern
SetupIconFile=..\KatieCAD.ico
; Banner images (made by tools\make_installer_images.py from KatieCAD_Setup_Banner.png);
; several sizes for the Windows scaling steps 100 % to 250 %
WizardImageFile=wizard_large_164.bmp,wizard_large_192.bmp,wizard_large_246.bmp,wizard_large_328.bmp,wizard_large_410.bmp
WizardSmallImageFile=wizard_small_55.bmp,wizard_small_64.bmp,wizard_small_83.bmp,wizard_small_110.bmp,wizard_small_138.bmp
LicenseFile=..\LICENSE

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Messages]
german.WelcomeLabel2=Dieser Assistent installiert [name/ver] auf Ihrem Computer.%n%nKatieCAD ist ein 2D-CAD-Programm mit Elektro-CAD, Schaltschrank-Planung und einfachem 3D – kostenlos und quelloffen (MIT-Lizenz).%n%nSchließen Sie vor dem Fortfahren bitte alle anderen Anwendungen.
spanish.WelcomeLabel2=Este asistente instalará [name/ver] en su equipo.%n%nKatieCAD es un programa de CAD 2D con CAD eléctrico, planificación de armarios y 3D sencillo: gratuito y de código abierto (licencia MIT).%n%nAntes de continuar, cierre las demás aplicaciones.
english.WelcomeLabel2=This wizard installs [name/ver] on your computer.%n%nKatieCAD is a 2D CAD program with electrical CAD, cabinet planning and simple 3D - free and open source (MIT license).%n%nPlease close all other applications before you continue.

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; Flags: unchecked

[Files]
Source: "..\dist\KatieCAD\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\KatieCAD"; Filename: "{app}\KatieCAD.exe"
Name: "{autodesktop}\KatieCAD"; Filename: "{app}\KatieCAD.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\KatieCAD.exe"; Description: "{cm:LaunchProgram,KatieCAD}"; Flags: nowait postinstall skipifsilent
