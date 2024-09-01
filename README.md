# Vpn Service - Test Assignment for SheepFish
## Installation and Usage with Docker

Here's how to get the project up and running using docker and docker compose.

### Setup

1. Clone this repository:

    ```
    git clone git@github.com:nazya08/vpn_service_SheepFish.git
    ```

2. Copy .env file and fill environment variables
   ```
   cp .env.example .env
   ```
3. Build docker images:
   ```
   docker compose build
   ```
4. Run docker images
   ```
   docker compose up
   ```

Your application should now be running at `http://localhost:8000`

## Installation and Usage without Docker

Here's how to get the project up and running on your local machine for development and testing.

### Setup

1. Clone this repository:

    ```
    git clone git@github.com:nazya08/vpn_service_SheepFish.git
    ```

2. Create virtual env.

    ```
    python -m venv venv
    ```

3. Activate virtual env.

   on Windows:

   ```
   cd venv/Scripts
   ```

   ```
   ./activate
   ```

   on Linux or Mac:

   ```
   source venv/bin/activate
   ```

4. Install requirements:

   ```
   pip install -r requirements.txt
   ```   


## Licence

MIT License

Created by Nazar Filoniuk, email: filoniuk.nazar.dev@gmail.com
