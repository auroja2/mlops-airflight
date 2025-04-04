from src.logger import get_logger
from src.custom_exception import CustomException
import sys
import traceback

# ✅ Initialize logger
logger = get_logger(__name__)

# ✅ Function to divide two numbers
def divide_number(a, b):
    try:
        if b == 0:
            raise CustomException("Division by zero")

        result = a / b
        logger.info(f"Dividing {a} by {b}")
        return result

    except CustomException as ce:
        logger.error(f"CustomException occurred: {str(ce)}")
        raise
    except Exception as e:
        logger.error("An unexpected error occurred")
        raise CustomException(str(e))

# ✅ Main execution block
if __name__ == "__main__":
    print("Executing script...")  # Ensure script execution is confirmed
    try:
        logger.info("Starting main program")
        result = divide_number(10, 0)
        print(f"Result: {result}")
    except CustomException as ce:
        logger.error(f"Exception caught in main: {str(ce)}")
        print(traceback.format_exc())  # Print full traceback to terminal
