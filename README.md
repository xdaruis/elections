# Elections Project

## Technologies
- Django
- Docker
- Django REST Framework

## Summary
This project is a backend API designed to facilitate election processes. It includes:
- Registration and login system
- Admin capabilities to create different elections
- User functionality to register as candidates and vote for others
- Election results where the candidate with the most votes wins

Currently, only the backend is implemented, with plans to work on the frontend in the future.

## Running the Project on Docker

### Install Docker (for Mac):
```sh
brew install --cask docker
```

### Build the images for the Development Server:
```sh
docker-compose build
```

### Start the Development Server:
```sh
docker-compose up
```

The backend will be available on port 8000.

### Access Swagger Docs:
- `http://localhost:8000/api/docs`

### Access Admin Panel:
- `http://localhost:8000/admin`

### Additional Scripts:
Different scripts for **production server setup**, testing, and linting are included in the `Makefile`.
