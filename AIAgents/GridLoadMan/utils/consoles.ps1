
#Set-ExecutionPolicy RemoteSigned

# Desired directory
$desiredPath = "C:\\C2_AIAgents\\AIAgents\\GridLoadManGEN5"

$myArray = @(
    "OPENAI",
    "OPENAIMINI",
    "OPENAIO3",
    "GROK",
    "GOOGLE",
    "OPENAI45",
    "LAMA",
    "CLAUDE",
    "BROKER"
)

$myCommand = @(
    "python .\runchatserver.py --broker ON --model OPENAI",
    "python .\runchatserver.py --broker ON --model OPENAIMINI",
    "python .\runchatserver.py --broker ON --model OPENAIO3",
    "python .\runchatserver.py --broker ON --model GROK",
    "python .\runchatserver.py --broker ON --model GOOGLE",
    "python .\runchatserver.py --broker ON --model OPENAI45",
    "python .\runchatserver.py --broker ON --model LAMA",
    "python .\runchatserver.py --broker ON --model CLAUDE",
    "python .\runbroker.py --confidence high"
)

# Desired window size
$width = 120
$height = 30

for ($i = 0; $i -lt $myArray.Length; $i++) {
    $title = $myArray[$i]
    $command = $myCommand[$i]

    # Start-Process cmd.exe -ArgumentList "/k", "title $title && 
    # mode con: cols=$width lines=$height && 
    # cd /d `"$desiredPath`" && 
    # powershell -command `[Console]::Write(`"$command`")"
 Start-Process cmd.exe -ArgumentList "/k", "title $title && mode con: cols=$width lines=$height && cd /d `"$desiredPath`" && doskey PRELOADED_COMMAND=$command && echo Press UP-Arrow then Enter to run the command"
    #Start-Process cmd.exe -ArgumentList "/k", "title $title && cd /d `"$desiredPath`" && echo $command"

    # Start-Process PowerShell -ArgumentList "-NoExit", "-Command", `
    # "& {
    #     `# Change directory
    #     cd '$desiredPath';
    #     `$Host.UI.RawUI.WindowTitle = '$title';
    #     $command
    # }"
}