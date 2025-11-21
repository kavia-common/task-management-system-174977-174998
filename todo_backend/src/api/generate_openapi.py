import json
from pathlib import Path

from src.api.main import app

def main() -> None:
    """
    Generate and write the OpenAPI schema to interfaces/openapi.json.

    This script imports the FastAPI app and uses its openapi() method
    to produce the schema, then writes it to the interfaces directory
    at the project root of this container.
    """
    # Determine container root as the parent of src/
    current_file = Path(__file__).resolve()
    src_dir = current_file.parent.parent  # .../todo_backend/src
    container_root = src_dir.parent       # .../todo_backend

    # Compute interfaces directory path under container root
    output_dir = container_root / "interfaces"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "openapi.json"

    # Build OpenAPI schema
    openapi_schema = app.openapi()

    # Write schema
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"Wrote OpenAPI schema to: {output_path}")

if __name__ == "__main__":
    main()
