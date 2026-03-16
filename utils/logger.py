import logging
import os

# create logs folder automatically
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/research.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("research_agent")