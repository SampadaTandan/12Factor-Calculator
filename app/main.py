from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from enum import Enum
from typing import Optional

app = FastAPI(
    title="Calculator API",
    description="A simple calculator microservice :)",
    version="1.0.0",
    openapi_tags=[{
        "name": "calculations",
        "description": "Arithmetic operations endpoints"
    }]
)

class Operation(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

class CalculationRequest(BaseModel):
    number1: float
    number2: float
    operation: Operation

class CalculationResponse(BaseModel):
    result: float
    detail: str

# @app.get("/health", tags=["health"])
# async def health_check():
#     """Service health check endpoint"""
#     return {"status": "healthy", "service": "calculator-api"}

@app.post("/calculate", 
          response_model=CalculationResponse, 
          tags=["calculations"],
          summary="Perform arithmetic calculation",
          responses={
              200: {"description": "Successful calculation"},
              400: {"description": "Invalid input or operation"}
          })
async def calculate(request: CalculationRequest):
    """
    Perform arithmetic calculations with two numbers.
    
    Supports the following operations:
    - add (+)
    - subtract (-)
    - multiply (*)
    - divide (/)
    """
    try:
        operation_detail = {
            Operation.ADD: ("+", request.number1 + request.number2),
            Operation.SUBTRACT: ("-", request.number1 - request.number2),
            Operation.MULTIPLY: ("*", request.number1 * request.number2),
            Operation.DIVIDE: ("/", request.number1 / request.number2 
                              if request.number2 != 0 
                              else None)
        }
        
        if request.operation == Operation.DIVIDE and request.number2 == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
            
        operator, result = operation_detail[request.operation]
        detail = f"{request.number1} {operator} {request.number2}"
        
        return CalculationResponse(
            result=result,
            detail=detail,
            operation=request.operation.value
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/add", 
         response_model=CalculationResponse, 
         tags=["calculations"],
         summary="Add two numbers")
async def add(number1: float, number2: float):
    """Add two numbers together"""
    result = number1 + number2
    return CalculationResponse(
        result=result,
        detail=f"{number1} + {number2}",
        operation="add"
    )

@app.get("/subtract", 
         response_model=CalculationResponse, 
         tags=["calculations"],
         summary="Subtract two numbers")
async def subtract(
    number1: float ,
    number2: float ):
    """Subtract the second number from the first"""
    result = number1 - number2
    return CalculationResponse(
        result=result,
        detail=f"{number1} - {number2}",
        operation="subtract"
    )

@app.get("/multiply", 
         response_model=CalculationResponse, 
         tags=["calculations"],
         summary="Multiply two numbers")
async def multiply(
    number1: float ,   number2: float ):
    """Multiply two numbers together"""
    result = number1 * number2
    return CalculationResponse(
        result=result,
        detail=f"{number1} * {number2}",
        operation="multiply"
    )

@app.get("/divide", 
         response_model=CalculationResponse, 
         tags=["calculations"],
         summary="Divide two numbers",
         responses={
             200: {"description": "Successful division"},
             400: {"description": "Division by zero attempted"}
         })
async def divide(
    number1: float ,
    number2: float 
):
    """Divide the first number by the second"""
    if number2 == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    
    result = number1 / number2
    return CalculationResponse(
        result=result,
        detail=f"{number1} / {number2}",
        operation="divide"
    )