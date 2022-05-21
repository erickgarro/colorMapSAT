# colorMapSAT
### A SAT Solver for coloring maps

## Project description:
<img src="https://github.com/erickgarro/colorMapSAT/blob/main/project-colors.png?raw=true" alt="Project: Colors" width="80%">

## Installation:

Clone the repository:
```bash
git clone https://github.com/erickgarro/colorMapSAT.git
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

## Usage:
You can try it on your machine or on the cloud. \
View the online demo: [https://mapsat.erickgarro.com](https://mapsat.erickgarro.com)

### For local / Mac execution:
Use the `main` branch.

### For cloud / Linux execution:
Use the `digitalocean` branch.

### Execution on Mac or Linux:
Create a virtual Python3 environment:
```bash
virtualenv -p python3 env
```
Activate your virtual environment:
```bash
source env/bin/activate
```
Run the command:
```bash
flask run
```
1. Access the web app at: [http://127.0.0.1:5000](http://127.0.0.1:5000)
2. Select the map you want to solve.
3. Type the number of colors you want to use.
4. Click on the `Solve it!` button.
5. Check the (no)solution.
6. [Optional] Download the solution files or you solved map image.

### Deployment on the cloud:
The web app is tested to work on the [App Platform](https://docs.digitalocean.com/products/app-platform) on Digital Ocean.

1. Create an account
2. Create a new App (we recommend a basic plan with 1vCPU and 512MB RAM).
3. Choose the `digitalocean` branch as your source.
4. Follow their instructions.

Copyright © 2022. Brian Bronz, Erick Garro, and Lorenzo Zaniol. \
Using Z3 and SAT clause generator by Martin Blicha. ToC @[USI](https://www.usi.ch), Switzerland\
Other copyrights belong to their respective owners.

