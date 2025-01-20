import time
import uvicorn
import logging
import app.namegen as ng
from fastapi import FastAPI, Request, HTTPException, Response
from typing import Dict, List

app = FastAPI()
df = ng.process_csv_data("./data/firstnames.csv")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    """
    Middleware to log incoming HTTP requests.

    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable): The next middleware or request handler.

    Returns:
        Response: The HTTP response from the next middleware or request handler.
    """
    idem = time.strftime("%Y%m%d-%H%M%S")
    logging.info(f"request id={idem} path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    formatted_process_time = '{0:.2f}'.format(process_time * 1000)
    logging.info(f"request id={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.get("/status", response_model=Dict)
def get_status() -> Dict:
    """
    Check server status.
    
    Returns:
        dict: A dictionary with the server status.
    """
    return {"status": "Server is running"}

@app.get("/countries", response_model=Dict[str, List[str]])
def get_countries() -> Dict[str, List[str]]:
    """
    Retrieve a list of valid country names.
    
    Returns:
        dict: A dictionary with a list of valid country names.
    """
    countries = ng.get_countries(df)
    return {"countries": countries}

@app.get("/random_names", response_model=Dict[str, List[str]])
def get_random_names(country: str, count: int) -> Dict[str, List[str]]:
    """
    Retrieve a list of random names for the specified country.
    
    Args:
        country (str): The country name.
        count (int): The number of random names to retrieve.
        
    Returns:
        dict: A dictionary with a list of random names.
    """
    if country not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid country name. Please provide a valid country name.")
    if count <= 0:
        raise HTTPException(status_code=400, detail="Count must be a positive integer.")
    if count > df[df[country] != 0].shape[0]:
        raise HTTPException(status_code=400, detail="Count exceeds the number of available names. Please provide a smaller count.")

    random_names = ng.get_random_names(df, country, count)
    return {"random_names": random_names}

@app.get("/random_male_names", response_model=Dict[str, List[str]])
def get_random_male_names(country: str, count: int) -> Dict[str, List[str]]:
    """
    Retrieve a list of random male names for the specified country (including unisex names).
    
    Args:
        country (str): The country name.
        count (int): The number of random male names to retrieve.
        
    Returns:
        dict: A dictionary with a list of random male names.
    """
    if country not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid country name. Please provide a valid country name.")
    if count <= 0:
        raise HTTPException(status_code=400, detail="Count must be a positive integer.")
    if count > df[df[country] != 0].shape[0]:
        raise HTTPException(status_code=400, detail="Count exceeds the number of available names. Please provide a smaller count.")

    random_male_names = ng.get_random_male_names(df, country, count)
    return {"random_male_names": random_male_names}

@app.get("/random_female_names", response_model=Dict[str, List[str]])
def get_random_female_names(country: str, count: int) -> Dict[str, List[str]]:
    """
    Retrieve a list of random female names for the specified country (including unisex names).
    
    Args:
        country (str): The country name.
        count (int): The number of random female names to retrieve.
        
    Returns:
        dict: A dictionary with a list of random female names.
    """
    if country not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid country name. Please provide a valid country name.")
    if count <= 0:
        raise HTTPException(status_code=400, detail="Count must be a positive integer.")
    if count > df[df[country] != 0].shape[0]:
        raise HTTPException(status_code=400, detail="Count exceeds the number of available names. Please provide a smaller count.")

    random_female_names = ng.get_random_female_names(df, country, count)
    return {"random_female_names": random_female_names}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
