# Project Documentation

This README provides a guide on how to set up and run the project, key highlights of the implementation, and potential improvements that could enhance the project in the future.

---

## Running the Project

This project is containerized with **Docker** and managed using **Docker Compose**, making it easy to set up and run across different environments.

### Requirements

- **Docker** and **Docker Compose** installed.
- **Poetry** (optional) for managing dependencies locally if you are running the project outside of Docker.

### Steps to Run the Project

**Build and Start the Project**:

In the root directory of the project, run the following command:

   ```bash
   docker-compose up --build
   ```

This command will:

- Build the Docker image for the project.
- Start the FastAPI server in a Docker container.

**Access the API**:

You can access the API via `http://localhost:8888`
    
The main endpoint /productionplan accepts a POST request with payload data, as described in the API documentation below.
    
**Running Tests**:

Just run:

```bash
docker-compose run --rm test
```


## API Endpoint Documentation

The main endpoint provided by this API is `/productionplan`.

Method: POST

Calculates the optimal power output for each power plant to meet a 
specified load (electricity demand) while minimizing costs.

**Request Payload**:

The JSON payload should include:

- `load`: The total demand for electricity in MW.
- `fuels`: Contains details on fuel prices and wind availability.
- `gas`: Cost of gas per MWh.
- `kerosine`: Cost of kerosine per MWh.
- `co2`: Cost of CO2 emission allowances per ton.
- `wind`: Wind availability as a percentage (from 0 to 100).
- `powerplants`: A list of power plants, each containing:
- `name`: The name of the power plant.
- `type`: The type of the power plant (e.g., gasfired, turbojet, windturbine).
- `efficiency`: Efficiency rate, indicating how well the plant converts fuel to energy.
- `pmin`: Minimum power output (MW) the plant can produce if it's on.
- `pmax`: Maximum power output (MW) the plant can produce.
- `include_co2` (optional): Boolean indicating whether to include CO2 costs in the calculation.


### **Example**

**Request body**:

```json
{
    "load": 480,
    "fuels": {
        "gas": 13.4,
        "kerosine": 50.8,
        "co2": 20,
        "wind": 60
    },
    "powerplants": [
        {"name": "gasfiredbig1", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
        {"name": "gasfiredbig2", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
        {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150}
    ],
    "include_co2": true
}
```

**Response body**:

```json
[
    {"name": "windpark1", "p": 90.0},
    {"name": "gasfiredbig1", "p": 390.0},
    {"name": "gasfiredbig2", "p": 0.0}
]
```

## Implementation notes

### Domain-driven design

- The project is organized using domain-driven design principles, which separate business logic (service layer) from data structures (entity layer) and API routes (controller layer).
    
- Each part of the application has a distinct role, making the code modular, easier to test, and maintainable.

### Production Plan Calculation

- The business logic is implemented in `ProductionPlanService`, which determines the optimal power output based on:
    - Merit Order: Power plants are sorted by cost-efficiency to prioritize cheaper energy sources.
    - Operational Constraints: Each plant respects its `pmin` and `pmax` limits, ensuring power output remains within the plant's capabilities.
- Wind energy is considered at zero cost, and its output is adjusted according to the wind percentage in the payload.

- CO2 Cost Inclusion
When requested, the service adds CO2 costs for gas-fired plants based on emissions per MWh generated.
- This is controlled by the `include_co2` flag in the request, providing flexibility for scenarios where CO2 costs may or may not need to be considered.

## Possible Enhancements

- Enhanced Caching
    -  Redis could be used to provide shared, persistent caching between different instances of the application.
- Extended Power Plant Support
    - Add support for more power plant types or include more advanced attributes, such as fuel consumption rates, start-up costs, and shutdown times.
- Load-Balancing and Scaling
- Detailed Documentation and Logging
    - track the cost calculation and load distribution steps

