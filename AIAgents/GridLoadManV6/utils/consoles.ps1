
#Set-ExecutionPolicy RemoteSigned

$myArray = @(
    "OPENAI",
    "OPENAIMINI",
    "OPENAIO3",
    "GROK",
    "GOOGLE",
    # "OPENAI45",
    # "LAMA",
    "CLAUDE",
    "DEEPSEEK",
    "PHI",
    "NEMO",
    "QWEN",
    "BABYNEMO",
    "GEMMA",
    "BROKER"
)

$myCommand = @(
    "python .\runchatserver.py --broker ON --model OPENAI",
    "python .\runchatserver.py --broker ON --model OPENAIMINI",
    "python .\runchatserver.py --broker ON --model OPENAIO3",
    "python .\runchatserver.py --broker ON --model GROK",
    "python .\runchatserver.py --broker ON --model GOOGLE",
    # "python .\runchatserver.py --broker ON --model OPENAI45",
    # "python .\runchatserver.py --broker ON --model LAMA",
    "python .\runchatserver.py --broker ON --model CLAUDE",
    "python .\runchatserver.py --broker ON --model DEEPSEEK",
    "python .\runchatserver.py --broker ON --model PHI",
    "python .\runchatserver.py --broker ON --model NEMO",
    "python .\runchatserver.py --broker ON --model QWEN",
    "python .\runchatserver.py --broker ON --model BABYNEMO",
    "python .\runchatserver.py --broker ON --model GEMMA", 
    "python .\runbroker.py --confidence high"
)


$width=100
$lines=20

# Desired directory
$desiredPath = "C:\\C2_AIAgents\\AIAgents\\GridLoadManV6"

for ($i = 0; $i -lt $myArray.Length; $i++) {
    $title = $myArray[$i]
    $command = $myCommand[$i]
      
    Start-Process cmd.exe -ArgumentList "/k title $title && mode con: cols=$width lines=$lines && cd /d $desiredPath && echo $command"
   
}