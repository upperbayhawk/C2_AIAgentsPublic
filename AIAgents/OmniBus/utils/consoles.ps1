
#Set-ExecutionPolicy RemoteSigned

# Desired directory
$desiredPath = "C:\\C2_AIAgents\\AIAgents\\Omnibus"


# Desired window size
$width = 80
$height = 25

for ($i = 0; $i -lt 6; $i++) {
    Start-Process PowerShell -ArgumentList "-NoExit", "-Command", `
    "& {
        `# Change directory
        cd '$desiredPath'
    }"
}