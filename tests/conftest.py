import os

# Automatically bypass SQLAlchemy C-extensions on Windows platforms
# to prevent Application Control policy blocks.
os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"