<html>
<head>
</head>
<body>
    <h1>Location Optimization Algorithms for Facility Location Problems</h1>
    <p>This repository contains Python code that implements various heuristic algorithms for solving facility location optimization problems. These algorithms aim to find the optimal placement of facilities to minimize total costs while satisfying customer demand. The implemented algorithms include:</p>
    <ol>
        <li><strong>Add-Drop Heuristic:</strong> This class implements the Add-Drop heuristic, which iteratively adds or drops facility locations to improve the solution. It consists of methods for both adding and dropping facilities to optimize the solution.</li>
        <li><strong>Simulated Annealing:</strong> This class implements the Simulated Annealing metaheuristic, which uses a probabilistic approach to explore and optimize facility location solutions. The algorithm iteratively searches for better solutions by accepting worse solutions with a certain probability.</li>
        <li><strong>Late Acceptance:</strong> This class implements the Late Acceptance heuristic, which maintains a list of historical costs and accepts new solutions that are within the specified range of historical costs. This heuristic gradually improves the solution by accepting solutions with slightly worse costs initially.</li>
    </ol>
    <h2>Key Features:</h2>
    <ul>
        <li>Implementation of Add-Drop, Simulated Annealing, and Late Acceptance heuristics.</li>
        <li>Integration of various optimization techniques for facility location problems.</li>
        <li>Use of real-world datasets to demonstrate algorithm performance.</li>
        <li>Detailed output including computed costs, opened facilities, and computation times.</li>
    </ul>
    <h2>Usage:</h2>
    <ol>
        <li>Install the required libraries by running <code>pip install numpy pandas geopy</code>.</li>
        <li>Run the code to perform optimization using different algorithms on the provided datasets.</li>
        <li>Analyze the output to compare the performance of different algorithms in solving the facility location problem.</li>
    </ol>
    <p>Please note that this code is intended for educational and illustrative purposes and may require further customization for specific use cases.</p>
</body>
</html>
